from dataclasses import dataclass
import torch
from torch import nn
import torch.nn.functional as F


@dataclass
class SpeakerProfile:
    embedding: torch.Tensor
    sample_rate: int = 16000
    encoder_version: str = "fallback-v0"
    quality_score: float = 0.0


class SpeakerEncoderAdapter(nn.Module):
    """Encoder interface. Replace the fallback frontend with ECAPA/ResNet in Phase 1."""

    def __init__(self, embedding_dim: int = 192, sample_rate: int = 16000):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.sample_rate = sample_rate
        self.frontend = nn.Sequential(
            nn.Conv1d(1, 32, 5, stride=2, padding=2), nn.ReLU(),
            nn.Conv1d(32, 64, 5, stride=2, padding=2), nn.ReLU(),
            nn.Conv1d(64, embedding_dim, 3, stride=2, padding=1), nn.ReLU(),
        )

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        if audio.ndim == 2:
            audio = audio.unsqueeze(1)
        if audio.ndim != 3 or audio.shape[1] != 1:
            raise ValueError("audio must have shape [B, T] or [B, 1, T]")
        features = self.frontend(audio)
        embedding = F.adaptive_avg_pool1d(features, 1).squeeze(-1)
        return F.normalize(embedding, p=2, dim=-1)

    @torch.no_grad()
    def enroll(self, audio: torch.Tensor) -> SpeakerProfile:
        embedding = self(audio).mean(dim=0, keepdim=True)
        embedding = F.normalize(embedding, p=2, dim=-1).squeeze(0)
        quality = float(audio.abs().mean().clamp(0, 1))
        return SpeakerProfile(embedding, self.sample_rate, "fallback-v0", quality)
