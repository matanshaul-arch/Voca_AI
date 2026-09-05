import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch.utils.data import DataLoader
from voca_tse.dataset import ManifestTSEDataset, collate_tse
from voca_tse.evaluation import si_sdr
from voca_tse.models import ComplexSTFTSeparator, SpeakerEncoderAdapter


def masked(x, lengths):
    return x * (torch.arange(x.shape[-1], device=x.device)[None, :] < lengths[:, None])


def projection_power(signal, source):
    coefficient = (signal * source).sum(-1) / (source.square().sum(-1) + 1e-8)
    return coefficient.square() * source.square().sum(-1)


def main():
    parser = argparse.ArgumentParser(description="Evaluate an offline Complex STFT checkpoint")
    parser.add_argument("manifest"); parser.add_argument("checkpoint")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--ecapa-cache", default="data/cache/ecapa-voxceleb")
    parser.add_argument("--output")
    args = parser.parse_args()
    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    encoder = SpeakerEncoderAdapter(backend=checkpoint.get("encoder_backend", "fallback"), cache_dir=args.ecapa_cache).to(device).eval()
    model = ComplexSTFTSeparator(n_fft=checkpoint.get("n_fft", 256), hop_length=checkpoint.get("hop_length", 64), win_length=checkpoint.get("win_length", 256)).to(device).eval()
    model.load_state_dict(checkpoint["model"])
    loader = DataLoader(ManifestTSEDataset(args.manifest), batch_size=args.batch_size, collate_fn=collate_tse)
    raw_scores, estimate_scores, retention, suppression = [], [], [], []
    with torch.no_grad():
        for batch in loader:
            lengths = batch["lengths"].to(device)
            mixture = masked(batch["mixture"].to(device), lengths); target = masked(batch["target"].to(device), lengths)
            interferer = masked(batch["interferer"].to(device), lengths)
            enrollment = masked(batch["enrollment"].to(device), batch["enrollment_lengths"].to(device))
            estimate = masked(model(mixture, encoder(enrollment)), lengths)
            raw = si_sdr(target, mixture); score = si_sdr(target, estimate)
            raw_scores.extend(raw.cpu().tolist()); estimate_scores.extend(score.cpu().tolist())
            target_rms = target.square().mean(-1).sqrt().clamp_min(1e-8); estimate_rms = estimate.square().mean(-1).sqrt().clamp_min(1e-8)
            retention.extend((20 * torch.log10(estimate_rms / target_rms)).cpu().tolist())
            suppression.extend((10 * torch.log10((projection_power(mixture, interferer) + 1e-8) / (projection_power(estimate, interferer) + 1e-8))).cpu().tolist())
    result = {"manifest": args.manifest, "checkpoint": args.checkpoint, "records": len(raw_scores),
              "encoder_backend": checkpoint.get("encoder_backend", "fallback"),
              "raw_mixture_si_sdr_db": sum(raw_scores) / len(raw_scores), "estimate_si_sdr_db": sum(estimate_scores) / len(estimate_scores),
              "si_sdr_improvement_db": sum(e-r for e, r in zip(estimate_scores, raw_scores)) / len(raw_scores),
              "target_level_delta_db": sum(retention) / len(retention), "interferer_projection_suppression_db": sum(suppression) / len(suppression)}
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.output:
        output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
