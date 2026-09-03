from dataclasses import dataclass
import torch
from torch import nn
import torch.nn.functional as F
from typing import Optional


@dataclass
class SpeakerProfile:
    embedding: torch.Tensor
    sample_rate: int = 16000
    encoder_version: str = "fallback-v0"
    quality_score: float = 0.0


class SpeakerEncoderAdapter(nn.Module):
    """Speaker encoder interface with an optional SpeechBrain ECAPA backend.

    The fallback remains available for tests and development without downloaded
    weights. The production backend is intentionally lazy-loaded because model
    weights are external artifacts and should never be committed to Git.
    """

    def __init__(self, embedding_dim: int = 192, sample_rate: int = 16000,
                 backend: str = "fallback", pretrained_source: Optional[str] = None):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.sample_rate = sample_rate
        self.backend = backend
        self.pretrained_source = pretrained_source or "speechbrain/spkrec-ecapa-voxceleb"
        self.ecapa = None
        if backend == "ecapa":
            self._load_ecapa()
        elif backend != "fallback":
            raise ValueError("backend must be 'fallback' or 'ecapa'")
        self.frontend = nn.Sequential(
            nn.Conv1d(1, 32, 5, stride=2, padding=2), nn.ReLU(),
            nn.Conv1d(32, 64, 5, stride=2, padding=2), nn.ReLU(),
            nn.Conv1d(64, embedding_dim, 3, stride=2, padding=1), nn.ReLU(),
        )

    def _load_ecapa(self):
        try:
            from speechbrain.inference.speaker import EncoderClassifier
        except ImportError as exc:
            raise ImportError(
                "ECAPA backend requires optional dependency 'speechbrain'. "
                "Install it in the project venv; fallback backend remains available."
            ) from exc
        self.ecapa = EncoderClassifier.from_hparams(source=self.pretrained_source)
        self.ecapa.eval()

    def _encode_ecapa(self, audio: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            embedding = self.ecapa.encode_batch(audio).squeeze(1)
        return F.normalize(embedding, p=2, dim=-1)

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        if audio.ndim == 2:
            audio = audio.unsqueeze(1)
        if audio.ndim != 3 or audio.shape[1] != 1:
            raise ValueError("audio must have shape [B, T] or [B, 1, T]")
        if self.backend == "ecapa":
            return self._encode_ecapa(audio.squeeze(1))
        features = self.frontend(audio)
        embedding = F.adaptive_avg_pool1d(features, 1).squeeze(-1)
        return F.normalize(embedding, p=2, dim=-1)

    @torch.no_grad()
    def enroll(self, audio: torch.Tensor) -> SpeakerProfile:
        embedding = self(audio).mean(dim=0, keepdim=True)
        embedding = F.normalize(embedding, p=2, dim=-1).squeeze(0)
        quality = float(audio.abs().mean().clamp(0, 1))
        version = "ecapa-voxceleb" if self.backend == "ecapa" else "fallback-v0"
        return SpeakerProfile(embedding, self.sample_rate, version, quality)
