from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import numpy as np
import soundfile as sf
import torch
from scipy.signal import resample_poly

from voca_tse.inference import StreamingTSE
from voca_tse.models import DualConditioningSeparator, SpeakerEncoderAdapter

SAMPLE_RATE = 16000
MAX_SECONDS = 300


def load_audio(path: Path) -> torch.Tensor:
    audio, sample_rate = sf.read(path, always_2d=True, dtype="float32")
    if not len(audio):
        raise ValueError("audio file is empty")
    if len(audio) > sample_rate * MAX_SECONDS:
        raise ValueError(f"audio must be at most {MAX_SECONDS} seconds")
    mono = audio.mean(axis=1)
    if sample_rate != SAMPLE_RATE:
        divisor = np.gcd(sample_rate, SAMPLE_RATE)
        mono = resample_poly(mono, SAMPLE_RATE // divisor, sample_rate // divisor).astype(np.float32)
    return torch.from_numpy(np.clip(mono, -1.0, 1.0).copy())


@dataclass
class Result:
    job_id: str
    output_path: Path
    duration_seconds: float
    processing_seconds: float
    realtime_factor: float
    encoder_backend: str
    lambda_level: float | None


class LocalTSEService:
    def __init__(self, checkpoint: Path, work_dir: Path, ecapa_cache: Path):
        self.checkpoint = checkpoint
        self.work_dir = work_dir
        self.ecapa_cache = ecapa_cache
        self.work_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_data = torch.load(checkpoint, map_location="cpu", weights_only=True)
        self.backend = checkpoint_data.get("encoder_backend", "fallback")
        self.lambda_level = checkpoint_data.get("lambda_level")
        self.encoder = SpeakerEncoderAdapter(
            backend=self.backend,
            cache_dir=str(ecapa_cache) if self.backend == "ecapa" else None,
        ).eval()
        self.model = DualConditioningSeparator().eval()
        self.model.load_state_dict(checkpoint_data["model"])

    def preview(self, enrollment_path: Path) -> dict:
        audio = load_audio(enrollment_path)
        peak = float(audio.abs().max())
        return {"duration_seconds": round(audio.numel() / SAMPLE_RATE, 3), "peak": peak,
                "warnings": (["very short enrollment; use at least 3 seconds"] if audio.numel() < 3 * SAMPLE_RATE else []) +
                            (["audio appears clipped"] if peak >= 0.999 else [])}

    def separate(self, enrollment_path: Path, mixture_path: Path) -> Result:
        enrollment, mixture = load_audio(enrollment_path), load_audio(mixture_path)
        profile = self.encoder.enroll(enrollment.unsqueeze(0))
        stream = StreamingTSE(self.model, profile.embedding, context_samples=512)
        started = perf_counter()
        state, chunks = stream.create_state(), []
        for offset in range(0, mixture.numel(), 320):
            output, state = stream.process(mixture[offset:offset + 320], state)
            chunks.append(output.squeeze(0))
        elapsed = perf_counter() - started
        result = torch.cat(chunks).numpy()
        job_id = uuid4().hex
        output_path = self.work_dir / f"{job_id}.wav"
        sf.write(output_path, result, SAMPLE_RATE, subtype="PCM_16")
        duration = mixture.numel() / SAMPLE_RATE
        return Result(job_id, output_path, duration, elapsed, elapsed / max(duration, 1e-6),
                      self.backend, self.lambda_level)

    def delete(self, job_id: str) -> bool:
        path = self.work_dir / f"{job_id}.wav"
        if not path.is_file():
            return False
        path.unlink()
        return True
