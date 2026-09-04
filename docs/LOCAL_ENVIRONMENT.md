# Local training environment

Date: 2026-09-04

The supported local environment is `.venv311`, built from the official Astral CPython standalone release:

- CPython: 3.11.16
- Release: `python-build-standalone` tag `20260901`
- Platform: `aarch64-apple-darwin`
- Archive SHA-256: `50424fa409e8ae84b82a3052522f64695b47dff2158b70bb7358e0ebd6c085c9`
- Runtime, pip cache and downloaded dependencies remain inside the Git-ignored project paths.

Installed core versions at validation time:

- PyTorch 2.14.0
- SpeechBrain 1.1.1
- NumPy 2.4.6
- SciPy 1.17.1

PyTorch reports no MPS support in this standalone runtime, so current training is CPU-only. Re-evaluate a native MPS-enabled runtime before scaling training duration.

## Required preflight

Run these commands before data regeneration, training or evaluation:

```bash
.venv311/bin/python scripts/preflight.py
.venv311/bin/python -m pytest -q
.venv311/bin/python scripts/validate_manifest.py \
  data/manifests/voca_real_v1/train.jsonl \
  data/manifests/voca_real_v1/valid.jsonl \
  data/manifests/voca_real_v1/test.jsonl
git status --short --branch
```

Do not use the legacy `.venv` for new experiments: it runs Python 3.9.6 and does not satisfy `requires-python = ">=3.10"`.
