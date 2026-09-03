import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from voca_tse.dataset import ManifestTSEDataset, collate_tse
from voca_tse.losses import ContrastiveTSELoss
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator


def masked(x, lengths):
    mask = torch.arange(x.shape[-1], device=x.device)[None, :] < lengths[:, None]
    return x * mask


def main():
    parser = argparse.ArgumentParser(description="Train TSE separator from a JSONL manifest")
    parser.add_argument("manifest")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--backend", choices=["fallback", "ecapa"], default="fallback")
    parser.add_argument("--output", default="checkpoints/manifest-baseline.pt")
    args = parser.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dataset = ManifestTSEDataset(args.manifest)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, collate_fn=collate_tse)
    encoder = SpeakerEncoderAdapter(backend=args.backend).to(device).eval()
    model = DualConditioningSeparator().to(device)
    optimizer = Adam(model.parameters(), lr=1e-3)
    loss_fn = ContrastiveTSELoss(encoder, lambda_contrastive=0.0, lambda_leakage=0.0)
    for epoch in range(1, args.epochs + 1):
        model.train(); running = 0.0
        for batch in loader:
            mixture = batch["mixture"].to(device)
            target = batch["target"].to(device)
            lengths = batch["lengths"].to(device)
            mixture, target = masked(mixture, lengths), masked(target, lengths)
            with torch.no_grad():
                embedding = encoder(target)
            estimate = model(mixture, embedding)
            loss = loss_fn(target, estimate)
            optimizer.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0); optimizer.step()
            running += float(loss.detach())
        print(f"epoch={epoch} mean_loss={running / max(1, len(loader)):.4f}")
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": model.state_dict(), "encoder_backend": args.backend}, output)
    print(f"saved={output} device={device} records={len(dataset)}")


if __name__ == "__main__":
    main()
