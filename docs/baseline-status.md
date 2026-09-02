# Baseline status

The initial baseline is trained on synthetic Gaussian waveforms only. This validates the training loop and interfaces, not speech quality. Real speech/noise manifests are required before drawing quality conclusions.

## Reproducible commands

```bash
./.venv/bin/python scripts/train_baseline.py --steps 20
./.venv/bin/python scripts/evaluate_random_mix.py
./.venv/bin/python scripts/benchmark_streaming.py
./.venv/bin/python -m pytest -q
```

## GitHub readiness gate

The repository is ready for its first GitHub push after the commands above pass, provided no raw audio or checkpoints are committed. The first public/private repository should include the source, tests, docs, and configuration only.
