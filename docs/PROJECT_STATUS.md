# Voca AI — End-of-Day Project Status

Date: 2026-09-05
Branch: `main`  
Latest recorded commit: see `git log -1 --oneline`

## Completed

| Area | Status | Evidence |
|---|---|---|
| Repository initialized | Done | GitHub remote configured |
| Initial MVP source | Done | PyTorch model, mixer, loss, tests |
| Local virtual environment | Done | Supported `.venv311` with CPython 3.11.16; legacy `.venv` is Python 3.9.6 |
| Synthetic baseline training | Done, limited | Runs on synthetic signals only |
| Manifest dataset loader | Done | JSONL + mono PCM16 WAV loader |
| Evaluation utilities | Done, limited | SI-SDR/RMS/suppression; no speech benchmark yet |
| Streaming wrapper | Done, causal reference | Causal context validation and offline/streaming parity test |
| Tests | Done | 8 tests passing at final validation |
| GitHub synchronization | Done | `main` pushed to origin |
| 360 research/specification | Done | `docs/RESEARCH_360_SPEC.md` |
| ECAPA integration | Done for local smoke test and baseline | SpeechBrain ECAPA loaded from pinned revision; weights cached under Git-ignored `data/cache` |
| Dataset/model policy | Done | `docs/DATASET_AND_MODEL_POLICY.md` |
| Dataset acquisition plan | Done | `docs/DATASET_INVENTORY.md`; approved baseline audio downloaded locally |
| Manifest training path | Done, smoke-ready | `scripts/train_manifest.py`; real data still pending |
| Speaker-disjoint splitting | Done | `voca_tse/dataset/split.py` |
| End-of-day 360 report | Done | `docs/END_OF_DAY_2026-09-04.md` |
| Approved real-data acquisition | Done for baseline releases | SLR12 train-clean-100/dev-clean/test-clean, SLR17, SLR28; checksums in `docs/DATASET_RELEASE_LOCK.md` |
| Real speaker-disjoint manifests | Done for `voca_real_v1` | 308 train / 40 valid / 36 test; zero target/interferer speaker overlap |
| Initial real-speech training | Done, limited | 1 epoch, fallback encoder, 308 records; checkpoint remains local |
| Real-speech evaluation | Done, limited | fallback: +0.262 dB; ECAPA: +0.515 dB SI-SDR improvement |
| Python 3.11 environment | Done | Project-local `.venv311`, CPython 3.11.16; provenance in `docs/LOCAL_ENVIRONMENT.md` |
| Separate enrollment references | Done for `voca_real_v1` | Every record uses a different source utterance from the same target speaker |
| Preflight command | Done | `scripts/preflight.py` checks runtime, manifests, leakage, sample shapes and enrollment separation |
| ECAPA real-speech run | Done, limited | Pinned revision; 1 epoch on CPU with separate enrollment; test SI-SDR improvement +0.515 dB and interferer projection suppression 23.61 dB |
| Causal/level-loss review | Done | Causal padding and future-looking normalization fixed; enrollment/output padding masked; level-loss reporting corrected |
| Level-loss calibration | Done, limited | Fixed-seed 1-epoch sweep selected `lambda_level=0.03` on validation: +0.624 dB SI-SDR, 5.67 dB suppression, -1.52 dB target level delta |
| Local product prototype | Done, experimental | Localhost API/UI for enrollment, separation, playback/download and temporary-result deletion |
| Validation early stopping | Done | Training saves the lowest validation-loss checkpoint and stops after configurable patience |
| Standard NS comparator | Done, limited | Declared offline spectral-subtraction baseline; test SI-SDR change -0.722 dB, suppression 0.06 dB |
| Controlled ECAPA training | Done, limited | Early stopping selected epoch 2/4: test +0.987 dB SI-SDR, 6.60 dB suppression, -1.66 dB target level delta |
| Market positioning refresh | Done | Generic NC/BVC is table stakes; Voca differentiates through consented Teacher Lock, explainable quality and local-first classroom workflow |
| Quantitative baseline refresh | Done | 36-record test evaluation of selected ECAPA checkpoint: +0.9866 dB SI-SDR improvement, 6.5960 dB suppression, -1.6642 dB target level delta |
| Complex STFT baseline | Done, limited | Offline speaker-conditioned complex mask; one-epoch fallback run: +0.3881 dB SI-SDR improvement, 7.6939 dB suppression, -3.1864 dB target level delta; details in `docs/COMPLEX_STFT_BASELINE_2026-09-05.md` |
| Matched Complex STFT validation | Done, limited | ECAPA + validation/early stopping run: -0.0297 dB SI-SDR improvement, 0.0419 dB suppression, +3.2792 dB target level delta; objective review required |
| Final session validation | Done | Preflight passed; 12 tests passed; new scripts compile successfully |
| Challenge set architecture | Done, design only | Immutable unseen challenge-set schema, strata, split rules and evaluation gates documented |
| Confidence Head architecture | Done, design only | Feature groups, outputs, bypass policy, calibration and acceptance gates documented |

## Not started

| ID | Task | Priority | Dependency |
|---|---|---:|---|
| T01 | Integrate real pretrained ECAPA-TDNN | P0 | Local integration done; production model revision/license record pending |
| T02 | Import licensed speech/noise datasets | P0 | Baseline releases imported; broader/product datasets still require review |
| T03 | Build speaker-disjoint train/validation/test manifests | Partial | `voca_real_v1` complete; fresh immutable challenge-set implementation pending |
| T04 | Train on real speech mixtures | P0 | Controlled early-stopped ECAPA candidate complete; fresh unseen challenge set and broader training remain |
| T05 | Add complex STFT mask baseline | Done, limited | Offline baseline implemented; matched ECAPA/validation run is non-competitive and needs objective/loss review |
| T06 | Make separator strictly causal | Done | CausalConv1d + per-timestep LayerNorm; parity test and streaming benchmark pass |
| T07 | Add confidence/uncertainty head | Design complete, implementation pending | T04 + stable checkpoint |
| T08 | ONNX FP16 export and parity tests | P1 | T06 |
| T09 | INT8 calibration/QAT study | P1 | T08 |
| T10 | Web AudioWorklet/WASM integration | P1 | T08 |
| T11 | WebRTC AEC/NS/AGC integration | P1 | T10 |
| T12 | Human listening/MOS test protocol | P0 | T04 |
| T13 | WER evaluation before/after TSE | P1 | T04 + STT engine |
| T14 | Privacy/profile lifecycle implementation | P0 | product API decision |
| T15 | Hard-negative mining and multi-negative conditioning | P1 | T04 |
| T16 | Multi-microphone spatial branch | P2 | hardware test setup |
| T17 | Turn-taking event API | P1 | T07 |
| T18 | Teach/classroom mode | P1 | Capture protocol ready; consented UX/quality capture pending |
| T19 | Voice quality monitor | P0 | T07 |
| T20 | Anti-spoofing/replay detection | P2 | T01 |
| T21 | Observability and model registry | P1 | T04 |
| T22 | Consent/admin controls | P0 | T14 |

## Partially completed

| Area | Current gap | Required completion |
|---|---|---|
| Speaker encoder | ECAPA adapter pinned and cached | license/model-card production review and broader validation |
| TSE model | calibrated 1-epoch research candidate | validation-based early stopping, stronger architecture and quality gates |
| Streaming | causal reference wrapper | stateful internal layers and bounded allocations |
| Latency | synthetic CPU benchmark | declared device matrix + p95 end-to-end test |
| Dataset | approved baseline and manifests exist | scale-up, more domain data and immutable challenge set |
| Negative conditioning | API exists | hard-negative experiments and ablation |

## Recommended next session

Next: implement and freeze the fresh unseen challenge set, then implement and calibrate the Confidence Head. When consented "Chen teaches" recordings arrive, run the UX/quality capture using `docs/CHEN_TEACHES_UX_CAPTURE.md`. Before any public deployment, require confidence controls and the frozen challenge set.
