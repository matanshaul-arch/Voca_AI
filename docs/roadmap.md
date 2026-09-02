# MVP Roadmap

## Current milestone

Offline positive-only TSE baseline with optional negative conditioning.

## Next milestones

1. Replace fallback speaker encoder with a verified ECAPA-TDNN adapter.
2. Add real speech/noise manifests and speaker-disjoint evaluation.
3. Add complex STFT mask baseline and compare against the time-domain model.
4. Implement stateful chunked inference and latency benchmarks.
5. Export to ONNX FP16, then evaluate INT8.
6. Integrate with WebRTC AudioWorklet/native audio.
7. Add confidence-gated online adaptation only after drift tests.

## Acceptance gates

- No target-only speech dropout in regression tests.
- P95 model processing below 10 ms on target hardware.
- End-to-end interactive latency below 25–30 ms.
- Quantized model quality degradation is measured before deployment.
