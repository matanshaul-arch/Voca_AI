# Voca AI — Session Handoff (2026-09-05)

## Exact current state

- Branch: `main`; final session changes are intended to be committed and pushed to `origin/main`.
- Existing selected checkpoint remains `checkpoints/voca-real-v1-ecapa-l03-early-stop.pt` (Git-ignored).
- It remains the product-prototype checkpoint: +0.9866 dB SI-SDR improvement, 6.5960 dB interferer suppression, -1.6642 dB target level delta on 36 test records.
- Complex STFT baseline is implemented as an offline, centered-STFT model. It is not causal or production-ready.
- Complex STFT one-epoch fallback run: +0.3881 dB SI-SDR improvement, 7.6939 dB suppression, -3.1864 dB target level delta.
- Matched one-epoch ECAPA/Complex-STFT run with validation machinery: -0.0297 dB SI-SDR improvement, 0.0419 dB suppression, +3.2792 dB target level delta; currently non-competitive and shows target-level gain.
- Preflight passed and 12/12 tests passed.
- Chen recordings have not yet been supplied. When available, use `docs/CHEN_TEACHES_UX_CAPTURE.md`; store anonymous audio only under Git-ignored `data/raw/chen_teaches/`.

## Files added this session

- `voca_tse/models/complex_stft_separator.py`
- `scripts/train_complex_stft.py`
- `scripts/evaluate_complex_stft.py`
- `tests/test_complex_stft.py`
- `docs/COMPLEX_STFT_BASELINE_2026-09-05.md`

## Full unfinished task table

| ID | Task | Status | Priority | Next evidence |
|---|---|---|---:|---|
| T01 | ECAPA production review | Partial | P0 | license/model card and broader validation |
| T02 | Licensed speech/noise data expansion | Partial | P0 | approved domain data |
| T03 | Speaker-disjoint manifests/challenge set | Partial | P0 | immutable unseen challenge set |
| T04 | Real-speech training | Partial | P0 | matched experiments and quality gates |
| T05 | Complex STFT mask baseline | Partial-complete | P0 | matched ECAPA run and validation early stopping |
| T07 | Confidence/uncertainty head | Not started | P0 | calibrated bypass policy |
| T08 | ONNX FP16/parity | Not started | P1 | numerical and device parity |
| T09 | INT8 calibration/QAT | Not started | P1 | quality/latency study |
| T10 | Web AudioWorklet/WASM | Not started | P1 | browser audio-thread prototype |
| T11 | WebRTC AEC/NS/AGC | Not started | P1 | end-to-end echo test |
| T12 | Human MOS/listening protocol | Not started | P0 | blinded listening results |
| T13 | WER before/after TSE | Not started | P1 | raw/NS/Voca comparison |
| T14 | Privacy/profile lifecycle | Not started | P0 | delete/export/encryption design |
| T15 | Hard-negative mining | Partial | P1 | multi-negative ablation |
| T16 | Multi-microphone spatial branch | Not started | P2 | hardware test setup |
| T17 | Turn-taking event API | Not started | P1 | VAD/turn-end/interruption events |
| T18 | Teach/classroom mode | Not started | P1 | consented Chen UX capture |
| T19 | Voice quality monitor | Not started | P0 | clipping/echo/distance/dropout alerts |
| T20 | Anti-spoofing/replay | Not started | P2 | replay evaluation |
| T21 | Observability/model registry | Not started | P1 | versioned metrics and rollback |
| T22 | Consent/admin controls | Not started | P0 | consent and profile ownership |

## Feature and idea map

| Priority | Features and ideas | Model/product implication |
|---|---|---|
| P0 | Teacher Lock, confidence bypass, Voice Quality Monitor, local privacy dashboard, consent ownership, target retention/dropout monitoring | confidence-aware TSE, safe bypass, auditable local sessions |
| P1 | WER mode, backchannel/interruption detection, speaker-aware captions, Teach Mode, broadcast continuity, device selection, offline recorder, model registry | TSE before VAD/STT, event API, reproducible profiles |
| P2 | Multi-mic spatial mode, auditory focus, acoustic labels, anti-spoofing, multi-device profile | spatial branch, replay tests, future profile portability |
| New market-led | “Why did quality drop?” timeline, before/after evidence, overlap severity label, classroom consent receipt, per-session quality summary, safe intensity control | explainable quality head, event logging, local deletion, no silent degradation |

## Research-backed positioning

Current market products emphasize generic voice isolation/noise cancellation, low latency, and improved VAD/STT. LiveKit explicitly distinguishes voice isolation for a single speaker from background-noise suppression for multi-speaker/diarization situations; Krisp positions voice isolation before VAD/turn detection; Descript emphasizes before/after listening and adjustable intensity. Voca should therefore differentiate around enrolled Teacher Lock, explainable quality, safe bypass and privacy-first classroom review—not generic noise cancellation.

Sources: Krisp [Voice Isolation](https://sdk-docs.krisp.ai/docs/models-for-conversational-ai), LiveKit [Noise and echo cancellation](https://docs.livekit.io/home/cloud/noise-cancellation), Descript [Audio Enhancer](https://www.descript.com/tools/voice-enhancer), VoiceFilter [targeted voice separation](https://arxiv.org/abs/1810.04826).

## Recommended next session order

1. Review Complex STFT objective/target-level behavior; either run one validation-gated improved spectral experiment or freeze this path.
2. Create the fresh unseen challenge set.
3. If Chen recordings arrive, run the nine-scenario local UX/quality capture.
4. Build Confidence Head and safe bypass policy.
5. Build Voice Quality Monitor and human/MOS/UX validation.
6. Decide between Teach Mode, quality monitoring, or additional model/data work.

## Session quality review

This session had good scope discipline: the baseline was re-measured before implementation, the new architecture was isolated from the existing checkpoint, tests were added, and the first result was interpreted with its limitations. The main improvement for future sessions is to use matched encoder, loss, training budget and validation protocol before treating architectures as comparable. Keep experiment artifacts and decisions explicit, and do not let a higher suppression number override target preservation.

## Copy this exact block into a new session

```text
אנחנו ממשיכים את Voca AI מתוך /Users/matanshaul/Projects/Voca_AI בלבד. קרא קודם את docs/SESSION_HANDOFF_2026-09-05.md, docs/PROJECT_STATUS.md, docs/COMPLEX_STFT_BASELINE_2026-09-05.md, docs/CHEN_TEACHES_UX_CAPTURE.md ו-docs/LOCAL_ENVIRONMENT.md.

גבול קשיח: כל shell, קריאה, כתיבה, עריכה והרצה רק בתוך /Users/matanshaul/Projects/Voca_AI. שמור על העבודה. אין force-push ואין שינוי היסטוריית Git.

מצב: checkpoint נבחר מקומי checkpoints/voca-real-v1-ecapa-l03-early-stop.pt; תוצאה על 36 test records: +0.9866 dB SI-SDR improvement, 6.5960 dB suppression, -1.6642 dB target level delta. Complex STFT offline baseline הוטמע ונבדק. ה-run המותאם עם ECAPA, validation ו-early stopping השיג -0.0297 dB SI-SDR improvement, 0.0419 dB suppression, +3.2792 dB target level delta ולכן אינו תחרותי כרגע. 12/12 בדיקות ו-preflight עברו. Chen recordings עדיין לא סופקו.

משימות פתוחות/חלקיות: T01 ECAPA production review; T02 הרחבת datasets; T03 challenge set ו-manifests; T04 real-speech training; T05 Complex STFT matched validation; T07 Confidence Head; T08 ONNX; T09 INT8; T10 WASM; T11 WebRTC; T12 MOS; T13 WER; T14 privacy/profile lifecycle; T15 hard negatives; T16 multi-mic; T17 turn-taking API; T18 Teach Mode; T19 Voice Quality Monitor; T20 anti-spoofing; T21 observability/model registry; T22 consent/admin.

פיצ'רים מרכזיים: P0 Teacher Lock, confidence-aware bypass, Voice Quality Monitor, local privacy, consent/profile ownership, target retention/dropout. P1 WER mode, interruption detection, captions, Teach Mode, broadcast continuity, device selection, offline recorder, registry. P2 multi-mic spatial, auditory focus, acoustic labels, anti-spoofing, multi-device profile. רעיונות חדשים: quality timeline, before/after evidence, overlap severity, consent receipt, per-session quality summary, safe intensity control.

סדר המשך: matched STFT/ECAPA validation → fresh unseen challenge set → Chen UX capture אם ההקלטות הגיעו → Confidence Head → Voice Quality Monitor → MOS/UX/WER → החלטת Teach Mode מול quality monitoring מול model improvement.

התחל תמיד ב-git status --short --branch וב-git log -1 --oneline. המשימה הבאה: לבדוק objective/target-level של Complex STFT; לבצע לכל היותר ניסוי validation-gated משופר אחד, או להקפיא את הכיוון ולעבור ל-Confidence Head. בסיום עדכן את מסמכי הסטטוס וה-handoff, הרץ preflight ו-pytest, ושמור audio/checkpoints/cache מחוץ ל-Git.
```
