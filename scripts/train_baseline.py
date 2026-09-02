import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch.optim import Adam
from voca_tse.dataset import mix_sources
from voca_tse.losses import ContrastiveTSELoss
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator


def make_batch(batch_size, length, device):
    target = torch.randn(batch_size, length, device=device)
    interferer = torch.randn(batch_size, length, device=device)
    noise = 0.02 * torch.randn(batch_size, length, device=device)
    mixtures, targets, interferers = [], [], []
    for i in range(batch_size):
        m, t, n, _ = mix_sources(target[i], interferer[i], noise[i], snr_db=0)
        mixtures.append(m); targets.append(t); interferers.append(n)
    return torch.stack(mixtures), torch.stack(targets), torch.stack(interferers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--length", type=int, default=1600)
    parser.add_argument("--output", default="checkpoints/baseline.pt")
    args = parser.parse_args()
    torch.manual_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    encoder = SpeakerEncoderAdapter().to(device)
    model = DualConditioningSeparator().to(device)
    # Keep encoder fixed for the first baseline to isolate separator learning.
    encoder.eval()
    optimizer = Adam(model.parameters(), lr=2e-3)
    loss_fn = ContrastiveTSELoss(encoder, lambda_contrastive=0.0, lambda_leakage=0.0)
    model.train()
    for step in range(1, args.steps + 1):
        mixture, target, _ = make_batch(args.batch_size, args.length, device)
        with torch.no_grad():
            embedding = encoder(target)
        estimate = model(mixture, embedding)
        loss = loss_fn(target, estimate)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        optimizer.step()
        if step == 1 or step % 5 == 0:
            print(f"step={step} loss={loss.item():.4f}")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": model.state_dict(), "embedding_dim": 192}, output)
    print(f"saved={output} device={device}")


if __name__ == "__main__":
    main()
