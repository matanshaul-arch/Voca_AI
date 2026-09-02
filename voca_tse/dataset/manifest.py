import json
from pathlib import Path


def read_manifest(path):
    """Read JSONL records without loading audio into memory."""
    records = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def validate_record(record):
    required = {"mixture", "target", "interferer"}
    missing = required - set(record)
    if missing:
        raise ValueError(f"manifest record missing fields: {sorted(missing)}")
    return True
