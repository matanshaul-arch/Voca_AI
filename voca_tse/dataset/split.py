import random
from collections import defaultdict


def speaker_disjoint_split(records, train_ratio=0.8, valid_ratio=0.1, seed=42):
    """Split records by connected speaker groups.

    Target/interferer pairs form connected components so a speaker cannot leak
    into another split through the interferer role.
    """
    if not 0 < train_ratio < 1 or not 0 <= valid_ratio < 1 or train_ratio + valid_ratio >= 1:
        raise ValueError("ratios must satisfy 0 < train_ratio and train_ratio + valid_ratio < 1")
    parent = {}

    def find(speaker_id):
        parent.setdefault(speaker_id, speaker_id)
        while parent[speaker_id] != speaker_id:
            parent[speaker_id] = parent[parent[speaker_id]]
            speaker_id = parent[speaker_id]
        return speaker_id

    def union(left, right):
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for record in records:
        target_id = record.get("target_speaker_id")
        if not target_id:
            raise ValueError("every record needs target_speaker_id for speaker-disjoint splitting")
        find(target_id)
        interferer_id = record.get("interferer_speaker_id")
        if interferer_id:
            union(target_id, interferer_id)

    groups = defaultdict(list)
    for record in records:
        groups[find(record["target_speaker_id"])].append(record)

    components = list(groups.values())
    random.Random(seed).shuffle(components)
    total = len(records)
    train_limit = total * train_ratio
    valid_limit = total * valid_ratio
    result = {"train": [], "valid": [], "test": []}
    for component in components:
        if len(result["train"]) < train_limit:
            split = "train"
        elif len(result["valid"]) < valid_limit:
            split = "valid"
        else:
            split = "test"
        result[split].extend(component)
    return result
