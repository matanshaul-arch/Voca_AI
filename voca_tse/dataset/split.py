import random
from collections import defaultdict


def speaker_disjoint_split(records, train_ratio=0.8, valid_ratio=0.1, seed=42):
    """Split JSON records by speaker_id, never by individual utterance."""
    if not 0 < train_ratio < 1 or not 0 <= valid_ratio < 1 or train_ratio + valid_ratio >= 1:
        raise ValueError("ratios must satisfy 0 < train_ratio and train_ratio + valid_ratio < 1")
    groups = defaultdict(list)
    for record in records:
        speaker_id = record.get("target_speaker_id")
        if not speaker_id:
            raise ValueError("every record needs target_speaker_id for speaker-disjoint splitting")
        groups[speaker_id].append(record)
    speakers = list(groups)
    random.Random(seed).shuffle(speakers)
    train_count = max(1, int(len(speakers) * train_ratio))
    valid_count = int(len(speakers) * valid_ratio)
    if train_count + valid_count >= len(speakers):
        valid_count = max(0, len(speakers) - train_count - 1)
    train_ids = set(speakers[:train_count])
    valid_ids = set(speakers[train_count:train_count + valid_count])
    result = {"train": [], "valid": [], "test": []}
    for speaker_id, speaker_records in groups.items():
        split = "train" if speaker_id in train_ids else "valid" if speaker_id in valid_ids else "test"
        result[split].extend(speaker_records)
    return result
