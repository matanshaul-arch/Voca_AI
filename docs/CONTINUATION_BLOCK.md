# Copy/paste continuation block

Copy the text below into a new Codex session to resume with the same context:

```text
We are continuing the Voca AI project from /Users/matanshaul/Projects/Voca_AI.

Hard boundary: perform all filesystem and shell work only inside /Users/matanshaul/Projects/Voca_AI. Do not read, write, delete, or execute anything outside this path without my explicit permission.

GitHub repository: https://github.com/matanshaul-arch/Voca_AI.git
Branch: main. The repository is already connected and synchronized. Preserve existing user work. Do not force-push or rewrite history.

Project objective: build an ultra-low-latency, privacy-first Target Speaker Intelligence Layer. It extracts an enrolled target speaker, suppresses nearby speakers and noise, exposes confidence/events, and improves live teaching, conferencing, broadcasting, accessibility, and voice-agent turn-taking.

Architecture decision:
- 16kHz mono MVP, later multi-microphone/spatial branch.
- ECAPA-TDNN speaker embeddings, 192/256 dimensions.
- Causal TSE separator with FiLM positive conditioning, optional multi-negative inhibition, and complex-mask upgrade.
- Low-confidence fallback/bypass; no automatic online profile adaptation until drift tests pass.
- WebRTC AEC before TSE; TSE before encoding/STT.
- Edge targets: ONNX Runtime/TensorRT, CoreML, WASM SIMD/WebGPU.

Read these files first:
- docs/PROJECT_STATUS.md
- docs/RESEARCH_360_SPEC.md
- docs/roadmap.md
- README.md

Current completed state:
- MVP source, synthetic mixer, loss, evaluation, streaming wrapper, manifest-backed mono PCM16 WAV dataset loader.
- 7 tests passed at the last validation.
- GitHub is synchronized through the latest end-of-day commit.

Most recent end-of-day report:
- Read docs/END_OF_DAY_2026-09-04.md for the 360 research, all task statuses, feature backlog, product map, and execution order.

Latest work:
- Added lazy optional SpeechBrain ECAPA backend in voca_tse/models/speaker_encoder.py.
- Installed SpeechBrain locally and verified pretrained `ecapa-voxceleb` loading, 192-d embedding, and unit norm. Weights remain outside Git.
- Added docs/DATASET_AND_MODEL_POLICY.md with dataset tiers, split rules, metadata and approval gates.

Latest real-data work:
- Owner-approved SLR12 train-clean-100/dev-clean/test-clean, SLR17 and SLR28 were downloaded locally, checksummed and extracted under Git-ignored `data/raw/`.
- `docs/DATASET_RELEASE_LOCK.md` records exact artifacts, licenses and hashes.
- `voca_real_v1` has 308 train / 40 valid / 36 test records and zero speaker overlap across target or interferer roles.
- The split utility now keeps connected target/interferer speaker groups together.
- One fallback-encoder epoch reached mean loss 0.4127. Test SI-SDR improved by 0.26 dB and interferer projection suppression was 5.40 dB. The local checkpoint and output are Git-ignored.
- The first reported +0.26 dB result used target-as-enrollment and remains pipeline evidence only; it must be replaced by the separate-enrollment ECAPA run. The standard-NS comparator is also still absent.
- A project-local CPython 3.11.16 environment now exists at `.venv311`; the legacy `.venv` is Python 3.9.6 and should not be used for new experiments.
- `voca_real_v1` was regenerated with a separate enrollment utterance for every target; loader, collate, training and evaluation now consume it.
- ECAPA is pinned to revision `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286` and configured for project-local cache/copies. Weights were not downloaded because explicit weight approval is still required.
- `scripts/preflight.py` passes under Python 3.11.16; PyTorch reports CPU-only and no MPS support in this standalone runtime.
- ECAPA smoke test and one-epoch real-speech run completed with separate enrollment. Test SI-SDR improvement was +0.515 dB and interferer projection suppression 23.61 dB, but target level delta was -19.91 dB; target-preservation calibration is required.

Current unfinished priority table:
T01 production ECAPA review and real-ECAPA training; T02 broader/product dataset review; T03 manifest scale-up and separate enrollment references; T04 quality training plus raw/standard-NS comparison; T05 complex STFT baseline; T06 strict causality; T07 confidence head; T08 ONNX FP16; T09 INT8; T10 AudioWorklet/WASM; T11 WebRTC integration; T12 human MOS; T13 WER evaluation; T14 privacy/profile lifecycle; T15 hard-negative mining; T16 multi-mic spatial branch.

Next action: add target-level preservation/anti-collapse loss, train longer with ECAPA, and add a declared standard-noise-suppression comparator. Run tests, update status documents, commit with a focused message, and push only after explicit approval.
```
