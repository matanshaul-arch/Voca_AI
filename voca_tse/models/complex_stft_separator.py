import torch
from torch import nn
import torch.nn.functional as F


class ComplexSTFTSeparator(nn.Module):
    """Offline, speaker-conditioned complex STFT mask baseline.

    This is intentionally an offline reference: the centered STFT looks ahead
    by half a window and is not a streaming/causal implementation.
    """

    def __init__(self, embedding_dim=192, channels=32, n_fft=256,
                 hop_length=64, win_length=256):
        super().__init__()
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.win_length = win_length
        self.register_buffer("window", torch.hann_window(win_length), persistent=False)
        self.condition = nn.Linear(embedding_dim, channels * 2)
        self.backbone = nn.Sequential(
            nn.Conv2d(2, channels, 3, padding=1), nn.PReLU(),
            nn.Conv2d(channels, channels, 3, padding=1), nn.PReLU(),
            nn.Conv2d(channels, 2, 1),
        )

    def forward(self, mixture, e_pos):
        if mixture.ndim != 2:
            raise ValueError("mixture must have shape [B, T]")
        spec = torch.stft(
            mixture, self.n_fft, self.hop_length, self.win_length,
            window=self.window.to(mixture), return_complex=True, center=True,
        )
        features = torch.stack((spec.real, spec.imag), dim=1)
        # Conditioning is broadcast over time/frequency while preserving the
        # compact 2-channel complex representation.
        gamma, beta = self.condition(F.normalize(e_pos, dim=-1)).chunk(2, dim=-1)
        scale = torch.tanh(gamma[:, :2]).unsqueeze(-1).unsqueeze(-1)
        bias = beta[:, :2].unsqueeze(-1).unsqueeze(-1)
        mask = torch.tanh(self.backbone(features) * (1 + scale) + bias)
        complex_mask = torch.complex(mask[:, 0], mask[:, 1])
        estimate = torch.istft(
            spec * complex_mask, self.n_fft, self.hop_length, self.win_length,
            window=self.window.to(mixture), center=True, length=mixture.shape[-1],
        )
        return estimate
