import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from voca_tse.dataset.manifest import read_manifest, validate_record
from voca_tse.dataset.split import speaker_disjoint_split


def main():
    parser = argparse.ArgumentParser(description="Validate and split a TSE JSONL manifest")
    parser.add_argument("manifest")
    args = parser.parse_args()
    records = read_manifest(args.manifest)
    for record in records:
        validate_record(record)
        if not record.get("target_speaker_id"):
            raise ValueError("target_speaker_id is required")
        if not record.get("license_status"):
            raise ValueError("license_status is required")
    splits = speaker_disjoint_split(records)
    print({key: {"records": len(value), "speakers": len({r['target_speaker_id'] for r in value})}
           for key, value in splits.items()})


if __name__ == "__main__":
    main()
