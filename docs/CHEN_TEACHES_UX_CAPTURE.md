# Chen Teaches — UX and Quality Capture

## Purpose and boundary

This is a local, consent-based product-discovery capture. It identifies useful and harmful behavior in the experimental prototype; it is not a public benchmark, model claim, or classroom deployment.

Use anonymous clip IDs only. Store the audio under Git-ignored `data/raw/chen_teaches/`; do not commit it. Obtain consent from every identifiable speaker before recording.

## Setup

1. Use the same microphone and room for a complete scenario set.
2. Record WAV at 16 kHz or 48 kHz when possible. Keep raw files unprocessed.
3. Start the prototype with the selected local checkpoint:

   ```bash
   .venv311/bin/python -m voca_tse.app.api --checkpoint checkpoints/sweep-l03.pt
   ```

4. Open `http://127.0.0.1:8000`; use one enrollment clip and one scenario clip for each run.
5. Delete the temporary result in the interface after listening. Stop the server after the session.

## Minimum capture set

| Clip ID pattern | Scenario | Duration | Pass observation |
|---|---|---:|---|
| `chen_enroll_01..03` | Chen alone: normal, quiet, energetic | 20–30 s each | Clear, unclipped enrollment |
| `chen_clean_01` | Chen teaches alone | 60 s | Target preservation reference |
| `chen_student_low_01` | One nearby student, low volume | 30 s | Student attenuation without damaging Chen |
| `chen_student_equal_01` | One nearby student, equal volume | 30 s | Hard isolation case |
| `chen_overlap_01` | 5–10 s student interruption | 30 s | Chen remains intelligible through overlap |
| `chen_overlap_02` | Two students overlap/interruption | 30 s | Failure behavior is understandable |
| `chen_noise_01` | Chairs, paper, keyboard, ventilation | 30–60 s | Noise reduction without speech damage |
| `chen_movement_01` | Chen turns away / moves 1–3 m | 30 s | Degradation is detectable and explainable |
| `chen_pause_01` | Chen pauses while students speak | 30 s | Residual student leakage is understood |

## Review protocol

For every run, listen to the original and result once with headphones. Record:

- **Target preservation:** 1 (unusable) to 5 (natural and clear).
- **Interferer attenuation:** 1 (unchanged) to 5 (not perceptible).
- **Artifacts:** none / mild / noticeable / severe.
- **Usefulness:** would a teacher use this result? yes / maybe / no.
- **UX clarity:** were file selection, processing state, playback, download and deletion clear? yes / no plus note.
- **Failure category:** target attenuation, interferer leakage, musical/noisy artifact, delay, input error, unclear UI, or other.

A candidate Teach Mode is useful only if Chen's target-preservation median is at least 4/5 on clean and low-interference clips, and no severe artifact occurs in those clips. Equal-level overlap remains a known hard case and must be labeled as such.

## Exit criteria and next decision

- Complete at least the nine rows in the minimum set.
- Fill one row per prototype run in `docs/templates/chen_teaches_capture_log.csv` (copy it outside Git before adding real data).
- Summarize the top three failure modes and the top three UX requests.
- If target attenuation dominates, prioritize confidence/quality monitoring and early stopping.
- If student leakage dominates, prioritize the standard-NS comparator and model/data work.
- If operators are confused despite acceptable audio, prioritize Teach Mode UX before more model work.
