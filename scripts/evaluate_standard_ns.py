import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
from torch.utils.data import DataLoader
from voca_tse.baselines import spectral_noise_suppress
from voca_tse.dataset import ManifestTSEDataset, collate_tse
from voca_tse.evaluation import si_sdr
from scripts.evaluate_manifest import masked, projection_power

parser = argparse.ArgumentParser(description="Evaluate declared spectral noise-suppression comparator")
parser.add_argument("manifest"); parser.add_argument("--batch-size", type=int, default=4); parser.add_argument("--output")
args = parser.parse_args()
scores=[]; raw=[]; retention=[]; suppression=[]
for batch in DataLoader(ManifestTSEDataset(args.manifest), batch_size=args.batch_size, collate_fn=collate_tse):
    lengths=batch["lengths"]; mixture=masked(batch["mixture"], lengths); target=masked(batch["target"], lengths); interferer=masked(batch["interferer"], lengths)
    estimate=masked(spectral_noise_suppress(mixture), lengths)
    raw.extend(si_sdr(target, mixture).tolist()); scores.extend(si_sdr(target, estimate).tolist())
    retention.extend((20*torch.log10(estimate.square().mean(-1).sqrt().clamp_min(1e-8)/target.square().mean(-1).sqrt().clamp_min(1e-8))).tolist())
    suppression.extend((10*torch.log10((projection_power(mixture,interferer)+1e-8)/(projection_power(estimate,interferer)+1e-8))).tolist())
result={"comparator":"offline spectral subtraction (15th-percentile noise PSD)","records":len(raw),"raw_mixture_si_sdr_db":sum(raw)/len(raw),"estimate_si_sdr_db":sum(scores)/len(scores),"si_sdr_improvement_db":sum(a-b for a,b in zip(scores,raw))/len(raw),"target_level_delta_db":sum(retention)/len(retention),"interferer_projection_suppression_db":sum(suppression)/len(suppression)}
print(json.dumps(result,indent=2,sort_keys=True))
if args.output: Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
