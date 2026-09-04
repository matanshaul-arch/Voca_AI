import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch.utils.data import DataLoader

from voca_tse.dataset import ManifestTSEDataset, collate_tse
from voca_tse.evaluation import si_sdr
from voca_tse.models import DualConditioningSeparator, SpeakerEncoderAdapter


def masked(audio, lengths):
    mask = torch.arange(audio.shape[-1], device=audio.device)[None, :] < lengths[:, None]
    return audio * mask


def projection_power(signal, source, eps=1e-8):
    coefficient = (signal * source).sum(-1) / (source.square().sum(-1) + eps)
    return coefficient.square() * source.square().sum(-1)


def main():
    parser = argparse.ArgumentParser(description="Evaluate a trained TSE checkpoint on a manifest")
    parser.add_argument("manifest")
    parser.add_argument("checkpoint")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--output")
    args = parser.parse_args()

    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    backend = checkpoint.get("encoder_backend", "fallback")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    encoder = SpeakerEncoderAdapter(backend=backend).to(device).eval()
    model = DualConditioningSeparator().to(device).eval()
    model.load_state_dict(checkpoint["model"])
    dataset = ManifestTSEDataset(args.manifest)
    loader = DataLoader(dataset, batch_size=args.batch_size, collate_fn=collate_tse)

    raw_scores, estimate_scores, retention, suppression = [], [], [], []
    with torch.no_grad():
        for batch in loader:
            lengths = batch["lengths"].to(device)
            mixture = masked(batch["mixture"].to(device), lengths)
            target = masked(batch["target"].to(device), lengths)
            interferer = masked(batch["interferer"].to(device), lengths)
            embedding = encoder(target)
            estimate = masked(model(mixture, embedding), lengths)
            raw_scores.extend(si_sdr(target, mixture).cpu().tolist())
            estimate_scores.extend(si_sdr(target, estimate).cpu().tolist())
            target_rms = target.square().mean(-1).sqrt().clamp_min(1e-8)
            estimate_rms = estimate.square().mean(-1).sqrt().clamp_min(1e-8)
            retention.extend((20 * torch.log10(estimate_rms / target_rms)).cpu().tolist())
            before = projection_power(mixture, interferer)
            after = projection_power(estimate, interferer)
            suppression.extend((10 * torch.log10((before + 1e-8) / (after + 1e-8))).cpu().tolist())

    result = {
        "manifest": args.manifest,
        "checkpoint": args.checkpoint,
        "encoder_backend": backend,
        "records": len(dataset),
        "raw_mixture_si_sdr_db": sum(raw_scores) / len(raw_scores),
        "estimate_si_sdr_db": sum(estimate_scores) / len(estimate_scores),
        "si_sdr_improvement_db": sum(e - r for e, r in zip(estimate_scores, raw_scores)) / len(raw_scores),
        "target_level_delta_db": sum(retention) / len(retention),
        "interferer_projection_suppression_db": sum(suppression) / len(suppression),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
