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
python -m pytest -q
python scripts/smoke_test.py
```

The first implementation is intentionally dependency-light. Production speaker encoders and ONNX export are subsequent milestones.
