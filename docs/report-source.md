# Voca AI — market and technical research source record

Date: 2026-09-05

## Scope and decision

Scope: current positioning of target-speaker extraction, voice isolation and voice-quality workflows, with implications for Voca's next model and product work. Decision: do not compete on generic noise cancellation alone; prioritize enrolled Teacher Lock, explainable quality, safe bypass and local-first review.

## Claim-to-source ledger

| Claim | Source | Confidence |
|---|---|---|
| Voice isolation is positioned before VAD/turn detection for cleaner agent interaction | Krisp, Voice Isolation | High |
| Voice isolation and background-noise suppression serve different conditions; single-speaker isolation is distinct from multi-speaker/noise suppression | LiveKit, Noise and echo cancellation | High |
| Before/after comparison and adjustable intensity are important voice-cleanup controls | Descript, Audio Enhancer / Studio Sound | High |
| Speaker-conditioned spectrogram masking is an established target-speaker-extraction approach | Wang et al., VoiceFilter | High |

## Sources

- https://sdk-docs.krisp.ai/docs/models-for-conversational-ai
- https://docs.livekit.io/home/cloud/noise-cancellation
- https://www.descript.com/tools/voice-enhancer
- https://arxiv.org/abs/1810.04826

## Limitations

This is a focused product/technical scan, not a complete competitor census or pricing study. Vendor claims are first-party positioning claims and should not be treated as independent quality benchmarks. Equal-level single-microphone overlap remains an explicit Voca limitation until validated on fresh data.
