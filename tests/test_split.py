from voca_tse.dataset import speaker_disjoint_split


def test_split_has_no_speaker_overlap():
    records = [{"target_speaker_id": f"spk-{i}", "mixture": f"{i}.wav", "target": f"{i}.wav", "interferer": "x.wav"}
               for i in range(10) for _ in range(2)]
    splits = speaker_disjoint_split(records, seed=7)
    ids = [{r["target_speaker_id"] for r in rows} for rows in splits.values()]
    assert not ids[0] & ids[1]
    assert not ids[0] & ids[2]
    assert not ids[1] & ids[2]
    assert sum(map(len, ids)) == 10


def test_split_prevents_interferer_speaker_leakage():
    records = []
    for index in range(10):
        records.append({
            "target_speaker_id": f"target-{index}",
            "interferer_speaker_id": f"interferer-{index}",
            "mixture": f"mix-{index}.wav",
            "target": f"target-{index}.wav",
            "interferer": f"interferer-{index}.wav",
        })
    splits = speaker_disjoint_split(records, seed=7)
    speaker_sets = []
    for rows in splits.values():
        speaker_sets.append({speaker for row in rows for speaker in (
            row["target_speaker_id"], row["interferer_speaker_id"]
        )})
    assert not speaker_sets[0] & speaker_sets[1]
    assert not speaker_sets[0] & speaker_sets[2]
    assert not speaker_sets[1] & speaker_sets[2]
