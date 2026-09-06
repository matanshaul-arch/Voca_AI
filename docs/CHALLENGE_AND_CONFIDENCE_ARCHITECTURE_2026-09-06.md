# Fresh unseen challenge set and Confidence Head architecture

Date: 2026-09-06

## Scope

This document defines the architecture and acceptance contract for two next
steps. It does not claim that the challenge set has been generated or that the
Confidence Head has been trained.

## 1. Fresh unseen challenge set

### Purpose

Create an immutable evaluation set that is never used for training,
hyperparameter selection, early stopping, or threshold calibration. Its role is
to estimate generalization and expose harmful processing before product demos.

### Data flow

```text
licensed sources + approved synthetic transforms
        -> source/session quarantine
        -> speaker-disjoint composition
        -> scenario metadata and QA
        -> frozen manifest + checksums
        -> evaluation only
```

### Required scenario strata

| Stratum | Examples |
|---|---|
| Target/interferer balance | -12, -6, 0, +6 dB relative level |
| Overlap | none, partial, continuous, equal-level hard case |
| Noise | fan, paper, chair, keyboard, door, music-like noise |
| Acoustics | dry, reverberant, near, 1–3 m target distance |
| Target behavior | normal, quiet, energetic, turn-away, pause, cough/laugh |
| Enrollment | short/long, normal/quiet/energetic, separate utterance |

### Split and immutability rules

- Speakers, sessions and source utterances must not overlap with train/valid or
  the historical test set.
- Product/Chen recordings remain a separate acceptance tier.
- Store only anonymous IDs in the manifest.
- Record source license, checksum, transform seed and generator version.
- Freeze the manifest hash after QA; changes create a new version.
- Never tune a model or threshold on this set.

### Manifest contract

Each row must contain the existing audio paths plus:

```json
{
  "record_id": "challenge_v1_000001",
  "target_speaker_id": "anon_target_001",
  "interferer_speaker_id": "anon_interferer_014",
  "scenario": "equal_level_overlap",
  "snr_db": 0,
  "target_interferer_db": 0,
  "overlap_ratio": 1.0,
  "reverb_id": "rir_007",
  "source_license": "approved-license-id",
  "generator_seed": 20260906,
  "split": "challenge_v1",
  "manifest_version": "v1"
}
```

### Evaluation outputs

Report per stratum and aggregate:

- SI-SDR improvement.
- Interferer projection suppression.
- Target level delta.
- Target retention and speech dropout.
- Artifact rate and harmful-processing rate.
- Confidence calibration once the head exists.
- p50/p95 latency.

Exit gate: no model is promoted unless it improves or preserves the selected
ECAPA baseline without unacceptable target attenuation, gain, or artifacts.

## 2. Confidence Head

### Purpose

Estimate whether applying TSE is safe at each segment and select between full
processing, conservative processing, crossfade, or bypass.

### Runtime architecture

```text
mixture ───────┐
enrollment ────┼─> ECAPA + separator ─> estimate
estimate ──────┘             │
                             └─> quality features
quality features + embeddings ─> Confidence Head
                                  ├─ confidence score
                                  ├─ target-present probability
                                  ├─ overlap probability
                                  └─ quality state + reasons
```

### Feature groups

- Enrollment/mixture embedding similarity.
- Target presence/VAD evidence.
- Target retention estimate and level delta.
- Residual/interferer leakage estimate.
- Mask temporal stability.
- Clipping, silence, dropout and echo indicators.
- Distance or reverberation degradation proxies.

### Outputs and policy

```json
{
  "confidence": 0.87,
  "target_present": 0.96,
  "overlap_probability": 0.22,
  "quality_state": "good",
  "reasons": [],
  "action": "process"
}
```

| State | Policy |
|---|---|
| good | full TSE |
| uncertain | conservative gain/crossfade |
| degraded | bypass or source-preserving blend |
| no_target | bypass; do not amplify noise |
| hard_overlap | process only if safe; label limitation |

### Training and calibration

- Generate labels from known synthetic mixtures plus human-reviewed difficult
  clips; do not use the frozen challenge set for training.
- Train the head after a stable separator checkpoint exists.
- Calibrate thresholds on validation data only.
- Evaluate calibration, false bypass, missed target and harmful-processing rate.
- Add temporal hysteresis and minimum state duration to prevent audible toggling.
- Default to source-preserving bypass when confidence is low.

### Acceptance gates

- Confidence must identify harmful target attenuation better than a simple RMS
  baseline.
- No severe artifacts in clean/low-interference acceptance clips.
- Bypass transitions must be click-free and bounded in latency.
- Every warning must expose a human-readable reason.
- No online enrollment adaptation until drift and impostor tests pass.

## Implementation order

1. Build and validate the challenge-set generator/schema.
2. Freeze `challenge_v1` and its checksums.
3. Implement feature extraction and a non-neural quality baseline.
4. Add the neural Confidence Head.
5. Calibrate thresholds on validation only.
6. Evaluate once on the frozen challenge set and later on consented Chen data.
