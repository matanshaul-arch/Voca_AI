import json
import platform
import sys
from pathlib import Path

import numpy
import scipy
import speechbrain
import torch

from voca_tse.dataset import ManifestTSEDataset
from voca_tse.dataset.manifest import read_manifest


def main():
    if sys.version_info < (3, 10):
        raise RuntimeError(f"Python 3.10+ required, found {platform.python_version()}")

    manifest_root = Path("data/manifests/voca_real_v1")
    manifests = {split: read_manifest(manifest_root / f"{split}.jsonl")
                 for split in ("train", "valid", "test")}
    speaker_sets = {
        split: {speaker for row in rows for speaker in (
            row["target_speaker_id"], row["interferer_speaker_id"]
        )}
        for split, rows in manifests.items()
    }
    overlaps = {
        "train_valid": len(speaker_sets["train"] & speaker_sets["valid"]),
        "train_test": len(speaker_sets["train"] & speaker_sets["test"]),
        "valid_test": len(speaker_sets["valid"] & speaker_sets["test"]),
    }
    if any(overlaps.values()):
        raise RuntimeError(f"speaker leakage detected: {overlaps}")

    sample = ManifestTSEDataset(manifest_root / "test.jsonl")[0]
    result = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "speechbrain": speechbrain.__version__,
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "device": "mps" if torch.backends.mps.is_available() else "cpu",
        "manifest_records": {split: len(rows) for split, rows in manifests.items()},
        "speaker_overlap": overlaps,
        "sample_shapes": {key: list(sample[key].shape) for key in (
            "mixture", "target", "interferer", "enrollment"
        )},
        "separate_enrollment": sample["metadata"]["enrollment_source"]
        != sample["metadata"]["target_source"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
