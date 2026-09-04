import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from voca_tse.dataset.manifest import read_manifest, validate_record


def main():
    parser = argparse.ArgumentParser(description="Validate and split a TSE JSONL manifest")
    parser.add_argument("manifest", nargs="+")
    args = parser.parse_args()
    required_metadata = {
        "target_speaker_id", "interferer_speaker_id", "source_dataset", "split",
        "snr_db", "overlap_ratio", "rir_id", "license_status",
    }
    manifests = {}
    for manifest in args.manifest:
        records = read_manifest(manifest)
        for record in records:
            validate_record(record)
            missing = required_metadata - set(record)
            if missing:
                raise ValueError(f"manifest record missing metadata: {sorted(missing)}")
            root = Path(record.get("root", "."))
            for field in ("mixture", "target", "interferer"):
                if not (root / record[field]).is_file():
                    raise FileNotFoundError(root / record[field])
        manifests[Path(manifest).stem] = records

    speaker_sets = {
        name: {speaker for row in rows for speaker in (
            row["target_speaker_id"], row["interferer_speaker_id"]
        )}
        for name, rows in manifests.items()
    }
    names = list(speaker_sets)
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            overlap = speaker_sets[left] & speaker_sets[right]
            if overlap:
                raise ValueError(f"speaker leakage between {left} and {right}: {sorted(overlap)[:5]}")
    print({name: {"records": len(manifests[name]), "speakers": len(speaker_sets[name])}
           for name in names})


if __name__ == "__main__":
    main()
