# Voca AI — 360 Research and Product Specification

Date: 2026-09-02  
Status: End-of-day architecture baseline  
Repository: `matanshaul-arch/Voca_AI`

## Executive decision

Voca AI should not be positioned as a generic noise suppressor. The differentiated product is a privacy-first, real-time **Target Speaker Intelligence Layer** for live teaching, conferencing, broadcasting, and voice agents.

It combines target-speaker extraction with:

1. speaker identity confidence;
2. background-speaker attribution and suppression;
3. turn-taking and interruption classification;
4. classroom/broadcast audio modes;
5. quality telemetry and explainable audio states;
6. local-first deployment with a server fallback.

## Research findings

VoiceFilter established enrollment-conditioned target speech extraction using a reference utterance. VoiceFilter-Lite demonstrated the relevance of streaming, on-device targeted separation. Recent TSE work continues to combine speaker verification embeddings with advanced separation backbones such as TF-GridNet and SepFormer.

SpeechBrain provides an established ECAPA-TDNN implementation and a pretrained VoxCeleb speaker-verification model. This supports using ECAPA as the enrollment/profile baseline rather than training a speaker encoder from zero.

WebRTC's Audio Processing Module covers AEC, NS and AGC, while browser AudioWorklet runs custom processing on a dedicated audio thread. Voca AI should therefore place itself after AEC and before encoding/STT, with a native/ONNX path for desktop and an AudioWorklet/WASM path for browsers.

Commercial benchmarks validate the product direction: Krisp markets real-time voice isolation, background-voice cancellation, VAD, turn prediction and interruption prediction; it reports a 15ms CPU voice-isolation path. NVIDIA Maxine demonstrates the adjacent value of real-time enhancement, voice restoration and telepresence effects. Voca AI's opportunity is to combine these capabilities around an enrolled speaker, transparent confidence, education workflows, and a local-first privacy model.

## Proposed product modes

| Mode | Target user | Core behavior | Differentiator |
|---|---|---|---|
| Teach | Online teacher/student | Preserve enrolled teacher, suppress household/classroom voices | Teacher-specific voice lock plus interruption insights |
| Meet | Conference participant | Clean microphone and expose speaker confidence | Target voice plus backchannel-aware turn events |
| Broadcast | Presenter/streamer | Preserve voice under room noise and nearby speech | Voice continuity and artifact guardrails |
| Agent | Voice AI pipeline | Clean input before VAD/STT/LLM | Fewer false interruptions and better transcription |
| Accessibility | Hearing/attention support | Target-only listening and adjustable residual mix | Personal auditory focus without hard mute |

## New system architecture

```text
Microphone(s)
  -> WebRTC AEC / calibration
  -> input quality + device classifier
  -> target VAD and speaker embedding
  -> causal TSE separator
  -> confidence and uncertainty head
  -> background speaker / event classifier
  -> adaptive gain policy
  -> optional residual noise enhancer
  -> audio output + STT lane + events lane
```

The output is not just audio. It is a synchronized pair:

```text
Clean PCM stream
Audio intelligence events:
  target_active
  interferer_active
  backchannel_detected
  turn_end_probability
  confidence
  quality_warning
```

## Technical design changes

### Model

- Phase 1: ECAPA-TDNN embedding adapter + causal TCN/complex-mask separator.
- Phase 2: multi-negative conditioning; use attention/max inhibition rather than a single negative centroid.
- Phase 3: compare compact causal TF-GridNet against the TCN baseline.
- Optional multi-microphone branch: spatial features, DOA, and neural beamforming.

### Confidence and safety

The model must expose uncertainty. Low confidence triggers bypass or gentle attenuation. Online profile adaptation is disabled until drift and impostor tests pass.

### Privacy

- Store embeddings, not raw enrollment audio, by default.
- Encrypt profile storage.
- Make profile deletion explicit and auditable.
- Keep inference local when possible.
- Do not send raw audio or embeddings to a server without an explicit product mode.

## Product differentiation opportunities

| Opportunity | User value | Difficulty | Priority |
|---|---|---:|---:|
| Target Speaker Lock | Only enrolled voice is emitted | High | P0 |
| Confidence-aware audio | Prevents robotic muting and dropouts | Medium | P0 |
| Backchannel vs interruption | Better agent turn-taking | High | P1 |
| Speaker-aware captions | Attribute target/interferer states | High | P1 |
| Classroom mode | Teacher voice, student questions, bell/ring detection | Medium | P1 |
| Broadcast continuity | Prevents timbre pumping and vocal artifacts | High | P1 |
| Personal auditory focus | User-controlled residual mix | Medium | P2 |
| Acoustic event labels | Keyboard, door, siren, applause, alarm | Medium | P2 |
| Voice quality monitor | Detect clipping, mic distance, room echo | Low | P0 |
| Privacy dashboard | Explain what is stored and where | Low | P0 |
| Multi-device profile | Same speaker profile across devices | Medium | P2 |
| Anti-spoofing | Detect replayed/enrolled voice attacks | High | P2 |

## Recommended KPIs

| KPI | Initial gate |
|---|---:|
| Target retention | >= 95% on target-only speech |
| Interferer attenuation | >= 20dB in standard overlap cases |
| Speech dropout | < 1–2% |
| Clean-speech harm | no material degradation versus bypass |
| Processing p95 | < 10ms per 10ms chunk on target CPU |
| End-to-end latency | < 25–30ms |
| Enrollment rejection accuracy | no low-quality profile silently accepted |
| STT WER impact | measured against raw and standard NS baselines |

## Sources

- [VoiceFilter paper](https://arxiv.org/abs/1810.04826)
- [VoiceFilter-Lite paper](https://arxiv.org/abs/2009.04323)
- [Target Speaker Extraction research overview](https://www.mdpi.com/2076-3417/16/13/6420)
- [SpeechBrain ECAPA-TDNN documentation](https://speechbrain.readthedocs.io/en/v0.5.15/API/speechbrain.lobes.models.ECAPA_TDNN.html)
- [Pretrained ECAPA VoxCeleb model](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)
- [WebRTC Audio Processing Module](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/g3doc/audio_processing_module.md)
- [MDN AudioWorklet](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet)
- [Krisp VIVA SDK](https://krisp.ai/developers/viva/)
- [Krisp SDK documentation](https://sdk-docs.krisp.ai/docs/getting-started)
- [NVIDIA Maxine](https://developer.nvidia.com/maxine/)
- [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)
- [LibriMix paper](https://arxiv.org/abs/2005.11262)
- [WHAM! paper](https://arxiv.org/abs/1907.01160)

## Research caveat

Vendor latency and quality claims are not directly comparable to our measurements. They are useful for positioning and target-setting, not as independent validation. Voca AI must reproduce all KPI measurements on a declared hardware/device matrix.
