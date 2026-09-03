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
- 4 tests passed at the last validation.
- GitHub is synchronized through the latest end-of-day commit.

Most recent end-of-day report:
- Read docs/END_OF_DAY_2026-09-04.md for the 360 research, all task statuses, feature backlog, product map, and execution order.

Latest work:
- Added lazy optional SpeechBrain ECAPA backend in voca_tse/models/speaker_encoder.py.
- Installed SpeechBrain locally and verified pretrained `ecapa-voxceleb` loading, 192-d embedding, and unit norm. Weights remain outside Git.
- Added docs/DATASET_AND_MODEL_POLICY.md with dataset tiers, split rules, metadata and approval gates.

Current unfinished priority table:
T01 real pretrained ECAPA-TDNN; T02 licensed speech/noise datasets; T03 speaker-disjoint manifests; T04 real-speech training; T05 complex STFT baseline; T06 strict causality; T07 confidence head; T08 ONNX FP16; T09 INT8; T10 AudioWorklet/WASM; T11 WebRTC integration; T12 human MOS; T13 WER evaluation; T14 privacy/profile lifecycle; T15 hard-negative mining; T16 multi-mic spatial branch.

Next action: approve exact dataset releases and terms, then generate real speaker-disjoint manifests and start real-speech training. Run tests, update docs/PROJECT_STATUS.md and docs/CONTINUATION_BLOCK.md, commit with a focused message, and push only after explicit approval if the session requires a new push.
```
