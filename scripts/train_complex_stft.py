import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from voca_tse.dataset import ManifestTSEDataset, collate_tse
from voca_tse.models import ComplexSTFTSeparator, SpeakerEncoderAdapter


def masked(x, lengths):
    mask = torch.arange(x.shape[-1], device=x.device)[None, :] < lengths[:, None]
    return x * mask


def main():
    parser = argparse.ArgumentParser(description="Train the offline Complex STFT baseline")
    parser.add_argument("manifest")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--backend", choices=["fallback", "ecapa"], default="fallback")
    parser.add_argument("--ecapa-cache", default="data/cache/ecapa-voxceleb")
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=20260905)
    parser.add_argument("--output", default="checkpoints/complex-stft-baseline.pt")
    args = parser.parse_args()
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dataset = ManifestTSEDataset(args.manifest)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, collate_fn=collate_tse)
    encoder = SpeakerEncoderAdapter(backend=args.backend, cache_dir=args.ecapa_cache if args.backend == "ecapa" else None).to(device).eval()
    model = ComplexSTFTSeparator().to(device)
    optimizer = Adam(model.parameters(), lr=args.learning_rate)
    for epoch in range(1, args.epochs + 1):
        model.train(); total = 0.0
        for batch in loader:
            lengths = batch["lengths"].to(device)
            mixture = masked(batch["mixture"].to(device), lengths)
            target = masked(batch["target"].to(device), lengths)
            enrollment = masked(batch["enrollment"].to(device), batch["enrollment_lengths"].to(device))
            with torch.no_grad():
                embedding = encoder(enrollment)
            estimate = masked(model(mixture, embedding), lengths)
            loss = (estimate - target).square().sum() / lengths.sum().clamp_min(1)
            optimizer.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0); optimizer.step()
            total += float(loss.detach())
        print(f"epoch={epoch} waveform_mse={total / max(1, len(loader)):.6f}")
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": model.state_dict(), "encoder_backend": args.backend, "seed": args.seed,
                "n_fft": model.n_fft, "hop_length": model.hop_length, "win_length": model.win_length}, output)
    print(f"saved={output} device={device} records={len(dataset)}")


if __name__ == "__main__":
    main()
