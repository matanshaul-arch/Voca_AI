import argparse
import json
import random
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly

from voca_tse.dataset import speaker_disjoint_split


SAMPLE_RATE = 16000


def load_mono(path, length, rng):
    audio, sample_rate = sf.read(path, dtype="float32", always_2d=True)
    audio = audio.mean(axis=1)
    if sample_rate != SAMPLE_RATE:
        audio = resample_poly(audio, SAMPLE_RATE, sample_rate).astype(np.float32)
    if len(audio) < length:
        repeats = int(np.ceil(length / max(1, len(audio))))
        audio = np.tile(audio, repeats)
    start = rng.randrange(max(1, len(audio) - length + 1))
    return audio[start:start + length].astype(np.float32)


def apply_rir(audio, rir):
    rir = rir / max(1e-8, np.sqrt(np.mean(rir * rir)))
    reverberant = fftconvolve(audio, rir, mode="full")[:len(audio)]
    scale = max(1e-8, np.sqrt(np.mean(reverberant * reverberant)))
    return (reverberant * (np.sqrt(np.mean(audio * audio)) / scale)).astype(np.float32)


def write_pcm16(path, audio):
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(pcm.tobytes())


def collect_speakers(librispeech_root):
    speakers = {}
    for path in sorted(librispeech_root.glob("*/*/*/*.flac")):
        speaker_id = f"librispeech-{path.parts[-3]}"
        speakers.setdefault(speaker_id, []).append(path)
    return speakers


def main():
    parser = argparse.ArgumentParser(description="Prepare a reproducible real-speech TSE baseline")
    parser.add_argument("--records", type=int, default=384)
    parser.add_argument("--duration-seconds", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=20260904)
    parser.add_argument("--output-root", default="data/prepared/voca_real_v1")
    parser.add_argument("--manifest-root", default="data/manifests/voca_real_v1")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    length = int(args.duration_seconds * SAMPLE_RATE)
    project_root = Path(__file__).resolve().parents[1]
    libri_root = project_root / "data/raw/librispeech/LibriSpeech"
    noise_root = project_root / "data/raw/musan/musan/noise/free-sound"
    rir_root = project_root / "data/raw/slr28/RIRS_NOISES/simulated_rirs"
    output_root = project_root / args.output_root
    manifest_root = project_root / args.manifest_root

    speakers = collect_speakers(libri_root)
    speaker_ids = sorted(speakers)
    rng.shuffle(speaker_ids)
    if len(speaker_ids) < 6:
        raise RuntimeError("at least six LibriSpeech speakers are required")
    if len(speaker_ids) % 2:
        speaker_ids.pop()
    speaker_pairs = list(zip(speaker_ids[::2], speaker_ids[1::2]))
    noises = sorted(noise_root.glob("*.wav"))
    rirs = sorted(rir_root.rglob("*.wav"))
    if not noises or not rirs:
        raise RuntimeError("approved MUSAN noise and SLR28 RIR files are required")

    records = []
    for index in range(args.records):
        target_id, interferer_id = speaker_pairs[index % len(speaker_pairs)]
        if rng.random() < 0.5:
            target_id, interferer_id = interferer_id, target_id
        target_path = rng.choice(speakers[target_id])
        enrollment_candidates = [path for path in speakers[target_id] if path != target_path]
        if not enrollment_candidates:
            raise RuntimeError(f"speaker {target_id} has no separate enrollment utterance")
        enrollment_path = rng.choice(enrollment_candidates)
        interferer_path = rng.choice(speakers[interferer_id])
        noise_path = rng.choice(noises)
        rir_path = rng.choice(rirs)
        target = load_mono(target_path, length, rng)
        enrollment = load_mono(enrollment_path, length, rng)
        interferer = load_mono(interferer_path, length, rng)
        noise = load_mono(noise_path, length, rng)
        rir = load_mono(rir_path, min(length, SAMPLE_RATE), rng)

        target = apply_rir(target, rir)
        overlap_ratio = rng.uniform(0.5, 1.0)
        shift = int((1.0 - overlap_ratio) * length)
        interferer = np.pad(interferer[:length - shift], (shift, 0))
        snr_db = rng.uniform(-5.0, 5.0)
        target_rms = max(1e-8, np.sqrt(np.mean(target * target)))
        interferer_rms = max(1e-8, np.sqrt(np.mean(interferer * interferer)))
        interferer *= target_rms / interferer_rms * 10 ** (-snr_db / 20.0)
        noise_rms = max(1e-8, np.sqrt(np.mean(noise * noise)))
        noise *= target_rms / noise_rms * 10 ** (-rng.uniform(10.0, 25.0) / 20.0)
        mixture = target + interferer + noise
        peak = max(1.0, float(np.max(np.abs(mixture))))
        target, interferer, mixture = target / peak, interferer / peak, mixture / peak

        record_id = f"mix-{index:06d}"
        relative_dir = Path(args.output_root) / "all" / record_id
        write_pcm16(project_root / relative_dir / "mixture.wav", mixture)
        write_pcm16(project_root / relative_dir / "target.wav", target)
        write_pcm16(project_root / relative_dir / "interferer.wav", interferer)
        write_pcm16(project_root / relative_dir / "enrollment.wav", enrollment)
        records.append({
            "root": ".",
            "mixture": str(relative_dir / "mixture.wav"),
            "target": str(relative_dir / "target.wav"),
            "interferer": str(relative_dir / "interferer.wav"),
            "enrollment": str(relative_dir / "enrollment.wav"),
            "enrollment_source": str(enrollment_path.relative_to(libri_root)),
            "target_source": str(target_path.relative_to(libri_root)),
            "interferer_source": str(interferer_path.relative_to(libri_root)),
            "target_speaker_id": target_id,
            "interferer_speaker_id": interferer_id,
            "source_dataset": "LibriSpeech SLR12",
            "source_release_target": target_path.parts[-4],
            "source_release_interferer": interferer_path.parts[-4],
            "snr_db": round(snr_db, 3),
            "overlap_ratio": round(overlap_ratio, 4),
            "rir_id": str(rir_path.relative_to(project_root / "data/raw/slr28")),
            "noise_id": str(noise_path.relative_to(project_root / "data/raw/musan")),
            "license_status": "owner-approved: LibriSpeech CC-BY-4.0; MUSAN free-sound public-domain subset; SLR28 Apache-2.0",
        })

    splits = speaker_disjoint_split(records, seed=args.seed)
    manifest_root.mkdir(parents=True, exist_ok=True)
    for split, rows in splits.items():
        for row in rows:
            row["split"] = split
        path = manifest_root / f"{split}.jsonl"
        path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
        speakers_in_split = {speaker for row in rows for speaker in (
            row["target_speaker_id"], row["interferer_speaker_id"]
        )}
        print(f"split={split} records={len(rows)} speakers={len(speakers_in_split)} manifest={path}")


if __name__ == "__main__":
    main()
