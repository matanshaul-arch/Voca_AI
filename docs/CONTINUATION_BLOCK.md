# Copy/paste continuation block

Copy the text below into a new Codex session:

```text
We are continuing the Voca AI project from /Users/matanshaul/Projects/Voca_AI.

Hard boundary: perform all filesystem, shell, read, write, edit and execution work only inside /Users/matanshaul/Projects/Voca_AI. Do not read or write outside it without my explicit permission. Preserve all existing work. Do not force-push or rewrite Git history.

Repository: https://github.com/matanshaul-arch/Voca_AI.git
Branch: main. Latest local commit: cc1e150 Record ECAPA real-speech evaluation. The branch is three commits ahead of origin/main; push only when explicitly requested.

Objective: build Voca AI Speaker Intelligence — a privacy-first, real-time Target Speaker Extraction layer that uses an enrolled speaker profile to preserve the target, suppress interferers/noise, and emit confidence, VAD, turn-taking and interruption events for Teach, Meet, Broadcast, Agent and Accessibility modes.

Architecture decisions:
- MVP: 16kHz mono.
- ECAPA-TDNN speaker embeddings, 192/256 dimensions.
- Causal TSE separator with FiLM positive conditioning; optional multi-negative inhibition; complex STFT mask upgrade.
- Confidence-aware bypass; no online profile adaptation until drift/impostor tests pass.
- AEC before TSE; TSE before WebRTC encoding and STT.
- Edge targets: ONNX Runtime/TensorRT, CoreML, WASM SIMD/WebGPU.
- Do not promise perfect separation of equally loud overlapping speakers on one microphone; multi-mic/spatial is future work.

Read first:
- docs/END_OF_DAY_2026-09-04.md
- docs/PROJECT_STATUS.md
- docs/RESEARCH_360_SPEC.md
- docs/DATASET_INVENTORY.md
- docs/DATASET_AND_MODEL_POLICY.md
- docs/DATASET_RELEASE_LOCK.md
- docs/LOCAL_ENVIRONMENT.md
- README.md

Current completed state:
- MVP PyTorch model, synthetic mixer, SI-SDR/loss/evaluation and reference streaming wrapper.
- Manifest-backed PCM16 WAV loader, padded collate, manifest training/evaluation and speaker-disjoint split.
- Split utility now keeps connected target/interferer speaker groups together, preventing role-based speaker leakage.
- Approved local data: LibriSpeech SLR12 train-clean-100/dev-clean/test-clean, MUSAN SLR17 and SLR28 RIR/Noise. Raw data is under Git-ignored data/raw/.
- `voca_real_v1`: 308 train / 40 valid / 36 test mixtures; every record has target, interferer, separate enrollment, source metadata, SNR, overlap, RIR and license status. Cross-split speaker overlap is zero.
- Supported environment: `.venv311`, CPython 3.11.16, PyTorch 2.14.0, SpeechBrain 1.1.1, NumPy 2.4.6, SciPy 1.17.1. PyTorch reports CPU-only/no MPS in this standalone runtime. Do not use legacy `.venv` (Python 3.9.6).
- `scripts/preflight.py` is mandatory before new experiments.
- ECAPA model: SpeechBrain `speechbrain/spkrec-ecapa-voxceleb`, pinned revision `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286`, cached under Git-ignored `data/cache/ecapa-voxceleb`.
- ECAPA smoke test passed: shape (1,192), unit norm, finite output.
- One ECAPA CPU epoch using separate enrollment: loss 0.0553; test raw mixture SI-SDR -1.288 dB; estimate SI-SDR -0.773 dB; improvement +0.515 dB; interferer projection suppression 23.61 dB; target level delta -19.91 dB.
- Interpretation: identity-conditioned suppression works, but target amplitude collapses. Add target-level preservation/anti-collapse loss or calibrated post-gain before claiming product quality.
- Standard noise suppression comparator has not yet been implemented. UI/app has not yet been implemented.
- Final validation passed: preflight, manifest validation, py_compile and 7 tests.

Exact commands:
`.venv311/bin/python scripts/preflight.py`
`.venv311/bin/python -m pytest -q`
`.venv311/bin/python scripts/validate_manifest.py data/manifests/voca_real_v1/train.jsonl data/manifests/voca_real_v1/valid.jsonl data/manifests/voca_real_v1/test.jsonl`

Unfinished task table:
T01 — ECAPA production review: partially complete; revision/cache/smoke done, license/model-card review and broader validation remain; P0.
T02 — Approved real datasets: partially complete; baseline imported, broader/product datasets remain; P0.
T03 — Speaker-disjoint manifests: partially complete; v1 complete, scale-up and immutable challenge set remain; P0.
T04 — Real-speech training: partially complete; initial ECAPA run complete, longer training and target-level preservation remain; P0.
T05 — Complex STFT mask baseline: not started; compare with time-domain separator; P0.
T06 — Strict causal separator: partially complete; remove future-frame dependency and measure p95 latency; P0.
T07 — Confidence/uncertainty head: not started; calibrated bypass/attenuation policy; P0.
T08 — ONNX FP16/parity: not started; numerical parity and device benchmark; P1.
T09 — INT8 calibration/QAT: not started; quality/latency tradeoff; P1.
T10 — AudioWorklet/WASM: not started; browser audio-thread prototype; P1.
T11 — WebRTC AEC/NS/AGC: not started; end-to-end echo test; P1.
T12 — Human MOS/listening test: not started; blinded protocol/results; P0.
T13 — WER before/after TSE: not started; raw vs NS vs Voca; P1.
T14 — Privacy/profile lifecycle: not started; delete/export/encryption; P0.
T15 — Hard-negative mining: partially complete; multi-negative ablation; P1.
T16 — Multi-microphone/spatial branch: not started; DOA/neural beamforming; P2.
T17 — Turn-taking event API: not started; VAD/turn-end/interruption events; P1.
T18 — Teach/classroom mode: not started; teacher lock and event policy; P1.
T19 — Voice quality monitor: not started; clipping/echo/distance/dropout alerts; P0.
T20 — Anti-spoofing/replay detection: not started; replay evaluation; P2.
T21 — Observability/model registry: not started; versioned metrics and rollback; P1.
T22 — Consent/admin controls: not started; consent record and profile ownership; P0.

Feature table:
P0: Target Speaker Lock; Confidence-aware bypass; Voice quality monitor; Local-first privacy dashboard; Consent/profile ownership; Target retention and speech-dropout monitoring.
P1: WER improvement mode; Backchannel vs interruption; Speaker-aware captions; Teach/classroom mode; Broadcast continuity; Model/device auto-selection; Offline demo recorder; Observability/model registry.
P2: Multi-mic spatial mode; Personal auditory focus; Acoustic event labels; Anti-spoofing; Multi-device speaker profile.

Recommended next execution order:
1. Add target-level preservation/anti-collapse loss and a declared standard-NS comparator.
2. Train longer with ECAPA and separate enrollment; report target retention, SI-SDR, suppression and dropout.
3. Fix strict causality and benchmark CPU/native MPS when available.
4. Add confidence/quality monitor, then human MOS and WER evaluation.
5. Only then build a local demo UI/API; do not deploy publicly yet.

Working rules:
- Check git status before changes.
- Use apply_patch for edits.
- Run tests after meaningful changes.
- Keep audio, checkpoints, caches and secrets out of Git.
- Update PROJECT_STATUS.md and CONTINUATION_BLOCK.md at session end.
- Commit focused changes. Push only with explicit approval.
```
