# Voca AI — Session Handoff (2026-09-04)

## Current state

- Git remote: `https://github.com/matanshaul-arch/Voca_AI.git`; branch `main`.
- The local prototype was added in commit `fca7abe`; run `git log -1 --oneline` before continuing to confirm the current tip.
- The prototype is local-only at `http://127.0.0.1:8000`; it accepts enrollment and mixture audio, creates a temporary output WAV under Git-ignored `data/cache/local-prototype/`, and supports deletion.
- To start it: `.venv311/bin/python -m voca_tse.app.api --checkpoint checkpoints/sweep-l03.pt`.
- It is an experimental research tool. It does not have confidence estimation, live microphone input, cloud upload, persistent profiles, WebRTC, or public-deployment readiness.
- Model selection: a fixed-seed one-epoch validation sweep selected `lambda_level=0.03` (+0.624 dB SI-SDR improvement, 5.67 dB interferer suppression, -1.52 dB target-level delta). A 3-epoch run regressed target level to -8.63 dB; do not use longer training without validation-based early stopping.
- Causality is now verified by test; streaming benchmark was 0.677 ms/chunk on CPU. Last validation passed: preflight and 10 tests.
- Training supports `--validation-manifest` and `--patience`; it saves the best validation-loss checkpoint. A fallback smoke run stopped after epoch 2 and retained epoch 1. `scripts/evaluate_standard_ns.py` is the declared offline spectral-subtraction comparator; it is not speaker-conditioned and performed poorly on the current test set (-0.722 dB SI-SDR improvement, 0.06 dB suppression).
- Controlled ECAPA run: `lambda_level=0.03`, 8-epoch cap, patience 2; early stopping selected epoch 2 of 4 (`validation_loss=0.1138`). Exploratory test result: +0.987 dB SI-SDR improvement, 6.60 dB interferer suppression, -1.66 dB target-level delta. Use local checkpoint `checkpoints/voca-real-v1-ecapa-l03-early-stop.pt` for the Chen capture.

## Chen teaches — recording plan

Obtain consent from every identifiable speaker before recording. Do not upload recordings to third parties. Record uncompressed WAV where possible, 16 kHz or 48 kHz, and log device, room and distances.

1. **Enrollment (3 takes):** Chen alone, 20–30 seconds each: normal teaching voice, quiet voice, and energetic voice. No other speech, music or processing.
2. **Clean lesson reference:** Chen alone for 60 seconds, natural material, to judge target preservation. Keep it separate from enrollment.
3. **Adjacent student speech:** Chen teaches while one student speaks nearby at low, medium and equal loudness. Record 30 seconds per condition.
4. **Overlap:** Chen continues speaking while a student interrupts for 5–10 seconds; repeat with 2 students and with a seated/far student.
5. **Classroom noise:** Chen teaches with chair movement, paper, keyboard, ventilation and brief door noise; 30–60 seconds.
6. **Echo/device conditions:** optional speaker playback or remote student audio, only with participant consent; clearly label the source and volume.
7. **Failure cases:** Chen turns away, moves 1–3 m from microphone, laughs/coughs, and pauses while others speak.

For every clip log: clip id, scenario, speakers, approximate distances, microphone/device, room, target/interferer loudness, overlap duration, consent status, and subjective outcome (target preserved / target attenuated / interferer leaked / artifacts). Do not record student names in filenames; use anonymous IDs.

## Immediate next task

Run the local prototype against the consented Chen capture set and create a short UX-quality review: whether enrollment is understandable, whether the output is useful, which failure cases matter, processing wait time, and whether temporary-file deletion is clear. This is product discovery, not a quality benchmark or deployment test.

## Required commands

```bash
.venv311/bin/python scripts/preflight.py
.venv311/bin/python -m pytest -q
.venv311/bin/python -m voca_tse.app.api --checkpoint checkpoints/sweep-l03.pt
```

## Guardrails

- Work only in `/Users/matanshaul/Projects/Voca_AI` unless explicitly authorized otherwise.
- Keep audio, checkpoints, caches and secrets out of Git.
- Preserve history; never force-push. Commit focused changes and push only with explicit approval.
- Stop the local server after testing.
