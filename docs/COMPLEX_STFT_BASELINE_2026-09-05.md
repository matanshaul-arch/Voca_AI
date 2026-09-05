# Complex STFT baseline — 2026-09-05

## Scope

This is an offline research baseline. It uses a centered STFT (`n_fft=256`,
`hop_length=64`, `win_length=256`) and a speaker-conditioned two-channel
complex mask. It is not causal and is not a production or streaming claim.

## Baseline reference

The existing calibrated ECAPA checkpoint was evaluated first on the fixed
`voca_real_v1` test manifest (36 records):

| Metric | Existing ECAPA checkpoint |
|---|---:|
| SI-SDR improvement | +0.9866 dB |
| Interferer projection suppression | 6.5960 dB |
| Target level delta | -1.6642 dB |

Checkpoint: `checkpoints/voca-real-v1-ecapa-l03-early-stop.pt`.

## Complex STFT run

The model was trained for one epoch on the 308-record training manifest with
the fallback encoder. The checkpoint is local and Git-ignored:
`checkpoints/complex-stft-baseline.pt`.

| Metric | Complex STFT baseline |
|---|---:|
| SI-SDR improvement | +0.3881 dB |
| Interferer projection suppression | 7.6939 dB |
| Target level delta | -3.1864 dB |

## Interpretation

This first run suppresses the interferer more strongly, but has lower overall
SI-SDR improvement and worse target-level preservation than the selected ECAPA
checkpoint. The comparison is directional rather than final because the
encoder backend, training duration and loss differ. Do not promote this model
without an ECAPA, validation-based, matched-training comparison and human
listening checks.

## Reproduction

```bash
.venv311/bin/python scripts/train_complex_stft.py \
  data/manifests/voca_real_v1/train.jsonl \
  --epochs 1 --batch-size 2 --backend fallback \
  --output checkpoints/complex-stft-baseline.pt

.venv311/bin/python scripts/evaluate_complex_stft.py \
  data/manifests/voca_real_v1/test.jsonl \
  checkpoints/complex-stft-baseline.pt \
  --batch-size 2
```

## Decision

Keep the implementation as a comparison baseline. Continue model improvement
on the existing ECAPA path first, then run a matched Complex STFT experiment
with validation early stopping before making an architecture decision.
