# Voca AI — Target Speaker Extraction MVP

Initial MVP for an offline-first, streaming-ready target speaker extraction pipeline.

## Scope

- 16 kHz mono audio.
- Optional speaker encoder adapter with deterministic fallback for smoke tests.
- Synthetic target/interferer/noise mixture generation.
- Causal TCN-style mask separator conditioned by a target embedding.
- Optional hard-negative conditioning and combined SI-SDR/contrastive/leakage loss.

## Quick start

```bash
.venv311/bin/python scripts/preflight.py
.venv311/bin/python -m pytest -q
.venv311/bin/python scripts/smoke_test.py
```

See `docs/LOCAL_ENVIRONMENT.md` for the pinned local Python runtime and required checks before training.

The first implementation is intentionally dependency-light. Production speaker encoders and ONNX export are subsequent milestones.
