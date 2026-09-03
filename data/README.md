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
