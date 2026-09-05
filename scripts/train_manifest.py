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
    parser.add_argument("--ecapa-cache", default="data/cache/ecapa-voxceleb")
    parser.add_argument("--lambda-level", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260904)
    parser.add_argument("--validation-manifest")
    parser.add_argument("--patience", type=int, default=3)
    parser.add_argument("--output", default="checkpoints/manifest-baseline.pt")
    args = parser.parse_args()
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dataset = ManifestTSEDataset(args.manifest)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, collate_fn=collate_tse)
    validation_loader = None if not args.validation_manifest else DataLoader(
        ManifestTSEDataset(args.validation_manifest), batch_size=args.batch_size, collate_fn=collate_tse)
    encoder = SpeakerEncoderAdapter(
        backend=args.backend,
        cache_dir=args.ecapa_cache if args.backend == "ecapa" else None,
    ).to(device).eval()
    model = DualConditioningSeparator().to(device)
    optimizer = Adam(model.parameters(), lr=1e-3)
    loss_fn = ContrastiveTSELoss(
        encoder, lambda_contrastive=0.0, lambda_leakage=0.0,
        lambda_level=args.lambda_level,
    )
    best_loss, best_epoch, stale_epochs = float("inf"), 0, 0
    for epoch in range(1, args.epochs + 1):
        model.train(); running = 0.0
        for batch in loader:
            mixture = batch["mixture"].to(device)
            target = batch["target"].to(device)
            enrollment = batch["enrollment"].to(device)
            enrollment = masked(enrollment, batch["enrollment_lengths"].to(device))
            lengths = batch["lengths"].to(device)
            mixture, target = masked(mixture, lengths), masked(target, lengths)
            with torch.no_grad():
                embedding = encoder(enrollment)
            estimate = model(mixture, embedding)
            estimate = masked(estimate, lengths)
            loss = loss_fn(target, estimate)
            optimizer.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0); optimizer.step()
            running += float(loss.detach())
        mean_loss = running / max(1, len(loader))
        validation_loss = mean_loss
        if validation_loader is not None:
            model.eval(); validation_total = 0.0
            with torch.no_grad():
                for batch in validation_loader:
                    lengths = batch["lengths"].to(device)
                    mixture, target = masked(batch["mixture"].to(device), lengths), masked(batch["target"].to(device), lengths)
                    enrollment = masked(batch["enrollment"].to(device), batch["enrollment_lengths"].to(device))
                    validation_total += float(loss_fn(target, masked(model(mixture, encoder(enrollment)), lengths)))
            validation_loss = validation_total / max(1, len(validation_loader))
        print(f"epoch={epoch} train_loss={mean_loss:.4f} validation_loss={validation_loss:.4f}")
        if validation_loss < best_loss:
            best_loss, best_epoch, stale_epochs = validation_loss, epoch, 0
            output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
            torch.save({"model": model.state_dict(), "encoder_backend": args.backend, "lambda_level": args.lambda_level,
                        "seed": args.seed, "best_epoch": best_epoch, "validation_loss": best_loss}, output)
        else:
            stale_epochs += 1
            if validation_loader is not None and stale_epochs >= args.patience:
                print(f"early_stop=epoch_{epoch} best_epoch={best_epoch}")
                break
    output = Path(args.output)
    if not output.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
        torch.save({"model": model.state_dict(), "encoder_backend": args.backend,
                    "lambda_level": args.lambda_level, "seed": args.seed}, output)
    print(f"saved={output} device={device} records={len(dataset)}")


if __name__ == "__main__":
    main()
