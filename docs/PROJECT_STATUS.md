# Voca AI — End-of-Day Project Status

Date: 2026-09-04
Branch: `main`  
Last known commit before this work: `56e8007`

## Completed

| Area | Status | Evidence |
|---|---|---|
| Repository initialized | Done | GitHub remote configured |
| Initial MVP source | Done | PyTorch model, mixer, loss, tests |
| Local virtual environment | Done | `.venv` with torch/numpy/pytest |
| Synthetic baseline training | Done, limited | Runs on synthetic signals only |
| Manifest dataset loader | Done | JSONL + mono PCM16 WAV loader |
| Evaluation utilities | Done, limited | SI-SDR/RMS/suppression; no speech benchmark yet |
| Streaming wrapper | Done, reference | Chunked state API; not production-causal yet |
| Tests | Done | 6 tests passing at last run |
| GitHub synchronization | Done | `main` pushed to origin |
| 360 research/specification | Done | `docs/RESEARCH_360_SPEC.md` |
| ECAPA integration | Done for local smoke test | SpeechBrain ECAPA backend loaded successfully; weights remain external cache |
| Dataset/model policy | Done | `docs/DATASET_AND_MODEL_POLICY.md` |
| Dataset acquisition plan | Done | `docs/DATASET_INVENTORY.md`; no audio downloaded |
| Manifest training path | Done, smoke-ready | `scripts/train_manifest.py`; real data still pending |
| Speaker-disjoint splitting | Done | `voca_tse/dataset/split.py` |
| End-of-day 360 report | Done | `docs/END_OF_DAY_2026-09-04.md` |
| Approved real-data acquisition | Done for baseline releases | SLR12 train-clean-100/dev-clean/test-clean, SLR17, SLR28; checksums in `docs/DATASET_RELEASE_LOCK.md` |
| Real speaker-disjoint manifests | Done for `voca_real_v1` | 308 train / 40 valid / 36 test; zero target/interferer speaker overlap |
| Initial real-speech training | Done, limited | 1 epoch, fallback encoder, 308 records; checkpoint remains local |
| Real-speech evaluation | Done, limited | test SI-SDR improvement +0.26 dB; interferer projection suppression 5.40 dB |
| Python 3.11 environment | Done | Project-local `.venv311`, CPython 3.11.16; provenance in `docs/LOCAL_ENVIRONMENT.md` |
| Separate enrollment references | Done for `voca_real_v1` | Every record uses a different source utterance from the same target speaker |
| Preflight command | Done | `scripts/preflight.py` checks runtime, manifests, leakage, sample shapes and enrollment separation |
| ECAPA real-speech run | Done, limited | Pinned revision; 1 epoch on CPU with separate enrollment; test SI-SDR improvement +0.515 dB and interferer projection suppression 23.61 dB |

## Not started

| ID | Task | Priority | Dependency |
|---|---|---:|---|
| T01 | Integrate real pretrained ECAPA-TDNN | P0 | Local integration done; production model revision/license record pending |
| T02 | Import licensed speech/noise datasets | P0 | Baseline releases imported; broader/product datasets still require review |
| T03 | Build speaker-disjoint train/validation/test manifests | P0 | `voca_real_v1` complete; scale-up pending |
| T04 | Train on real speech mixtures | P0 | Initial ECAPA run complete; target level loss requires calibration/AGC and longer training |
| T05 | Add complex STFT mask baseline | P0 | evaluation protocol |
| T06 | Make separator strictly causal | P0 | T05/model redesign |
| T07 | Add confidence/uncertainty head | P0 | T04 |
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
| T18 | Teach/classroom mode | P1 | T17 |
| T19 | Voice quality monitor | P0 | T07 |
| T20 | Anti-spoofing/replay detection | P2 | T01 |
| T21 | Observability and model registry | P1 | T04 |
| T22 | Consent/admin controls | P0 | T14 |

## Partially completed

| Area | Current gap | Required completion |
|---|---|---|
| Speaker encoder | ECAPA adapter pinned; new local cache path configured | explicit weight-download approval, smoke test and real-ECAPA training |
| TSE model | untrained reference TCN | real training and quality gates |
| Streaming | wrapper recomputes context | stateful causal layers and bounded allocations |
| Latency | synthetic CPU benchmark | declared device matrix + p95 end-to-end test |
| Dataset | approved baseline and manifests exist | scale-up, enrollment references and domain data |
| Negative conditioning | API exists | hard-negative experiments and ablation |

## Recommended next session

Next: add target-level preservation/anti-collapse loss, train longer with ECAPA, and implement a declared standard-NS comparator. The current ECAPA result improves SI-SDR but has target level delta -19.91 dB. Do not implement online adaptation or public demo deployment yet.
