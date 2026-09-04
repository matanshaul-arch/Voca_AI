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

## Local prototype

The local-only experimental prototype accepts a target-speaker enrollment file and a mixed audio file, then produces a separated WAV on `localhost`. It never uploads audio or persists profiles; temporary outputs are stored under Git-ignored `data/cache/local-prototype/` and can be deleted in the interface.

First train or select a local checkpoint, then run:

```bash
.venv311/bin/python -m pip install -e '.[app]'
.venv311/bin/python -m voca_tse.app.api --checkpoint checkpoints/sweep-l03.pt
```

Open http://127.0.0.1:8000. This is a research prototype, not a production-quality isolation claim: it has no confidence head, live microphone/WebRTC support, or persistent profile store.
