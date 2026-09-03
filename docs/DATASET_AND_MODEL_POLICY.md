# Dataset and model policy

## Speaker encoder

The code supports a lazy `backend="ecapa"` adapter for SpeechBrain's pretrained `speechbrain/spkrec-ecapa-voxceleb` model. The weights are external artifacts and must be downloaded into a local cache or approved model registry; they must not be committed to this repository. The default `backend="fallback"` is retained for tests.

Before production use, record the exact model revision, license, checksum, sample-rate behavior, and enrollment quality thresholds in the experiment manifest.

## Dataset tiers

| Tier | Purpose | Candidate sources | Status |
|---|---|---|---|
| A | Unit/smoke tests | Generated waveforms | Available |
| B | Reproducible research baseline | LibriMix/WHAM-style mixtures | Manifest loader ready; license review pending |
| C | Speaker embedding | VoxCeleb or approved equivalent | License/access review pending |
| D | Real-world robustness | Room impulse responses, DNS noises, far-field recordings | Collection/consent pending |
| E | Product acceptance | Consent-based recordings from target use cases | Not started |

## Required metadata

Every training/evaluation record must include target speaker ID, interferer speaker ID, source dataset, license/access status, sample rate, SNR, overlap ratio, reverberation parameters, and split name.

## Split rules

- No speaker may appear across train and validation/test splits.
- No recording session may cross a split.
- Product acceptance recordings must remain separate from model development data.
- Keep a fixed, immutable challenge set for regression measurements.

## Approval gates

No external dataset is imported until its license, redistribution terms, consent status, and allowed commercial use are documented. No pretrained weight is shipped until its model card and license are recorded.
