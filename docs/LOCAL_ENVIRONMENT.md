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

The ECAPA cache is pinned to SpeechBrain `spkrec-ecapa-voxceleb` revision `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286`. Cached file hashes are recorded locally below; the cache itself is Git-ignored.

```text
classifier.ckpt       fd9e3634fe68bd0a427c95e354c0c677374f62b3f434e45b78599950d860d535
embedding_model.ckpt  0575cb64845e6b9a10db9bcb74d5ac32b326b8dc90352671d345e2ee3d0126a2
label_encoder.ckpt    e13c3a167bb4112685670ee896d20e2b565af16b3a4ceeaa8689fa4d22adb8b9
mean_var_norm_emb.ckpt cd70225b05b37be64fc5a95e24395d804231d43f74b2e1e5a513db7b69b34c33
hyperparams.yaml      6f78854fa04ba59e761437b76a2575d3aba5e5016de3e9b69f0c9a5077fb1a41
```

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
