# Local data directory

Raw and prepared audio belongs here locally, but is intentionally ignored by Git.

Expected local layout:

```text
data/
  raw/<dataset-name>/
  prepared/<dataset-name>/
  manifests/train.jsonl
  manifests/valid.jsonl
  manifests/test.jsonl
  manifests/acquisition.jsonl
```

Use `scripts/validate_manifest.py` before training. Do not place personal or consent-restricted recordings in the repository.

## Reproducible real-speech baseline

After the approved SLR12, SLR17 and SLR28 artifacts are extracted into the layout documented in `docs/DATASET_RELEASE_LOCK.md`:

```bash
./.venv/bin/python scripts/prepare_real_baseline.py --records 384 --duration-seconds 2.0
./.venv/bin/python scripts/validate_manifest.py data/manifests/voca_real_v1/train.jsonl
./.venv/bin/python scripts/train_manifest.py data/manifests/voca_real_v1/train.jsonl \
  --epochs 1 --batch-size 4 --backend fallback \
  --output checkpoints/voca-real-v1-fallback.pt
./.venv/bin/python scripts/evaluate_manifest.py \
  data/manifests/voca_real_v1/test.jsonl \
  checkpoints/voca-real-v1-fallback.pt
```

The preparation seed defaults to `20260904`. Both target and interferer identities are included in the speaker-disjoint split constraint.
