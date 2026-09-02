import torch
from torch import nn
import torch.nn.functional as F
from typing import Optional


class FiLM(nn.Module):
    def __init__(self, embedding_dim: int, channels: int):
        super().__init__()
        self.to_gamma_beta = nn.Linear(embedding_dim, channels * 2)

    def forward(self, x: torch.Tensor, embedding: torch.Tensor) -> torch.Tensor:
        gamma, beta = self.to_gamma_beta(embedding).chunk(2, dim=-1)
        return x * (1 + gamma.unsqueeze(-1)) + beta.unsqueeze(-1)


class DualConditioningSeparator(nn.Module):
    """Causal time-domain mask separator; negative embeddings are optional."""

    def __init__(self, embedding_dim: int = 192, channels: int = 64, blocks: int = 4):
        super().__init__()
        self.in_proj = nn.Conv1d(1, channels, 1)
        self.film = FiLM(embedding_dim, channels)
        layers = []
        for i in range(blocks):
            dilation = 2 ** i
            layers.extend([
                nn.Conv1d(channels, channels, 3, padding=2 * dilation, dilation=dilation),
                nn.GroupNorm(1, channels), nn.PReLU(),
            ])
        self.backbone = nn.Sequential(*layers)
        self.mask_head = nn.Conv1d(channels, 1, 1)
        self.neg_gate = nn.Linear(embedding_dim, channels)

    def forward(self, mixture: torch.Tensor, e_pos: torch.Tensor,
                e_neg: Optional[torch.Tensor] = None, negative_strength: float = 0.25) -> torch.Tensor:
        if mixture.ndim == 2:
            mixture = mixture.unsqueeze(1)
        x = self.in_proj(mixture)
        x = self.film(x, F.normalize(e_pos, dim=-1))
        if e_neg is not None:
            if e_neg.ndim == 2:
                e_neg = e_neg.unsqueeze(1)
            neg = F.normalize(e_neg, dim=-1).mean(dim=1)
            inhibition = torch.sigmoid(self.neg_gate(neg)).unsqueeze(-1)
            x = x * (1.0 - negative_strength * inhibition)
        # Cropping restores strict causality after dilated same-length convolutions.
        x = self.backbone(x)
        x = x[..., :mixture.shape[-1]]
        mask = torch.sigmoid(self.mask_head(x))
        return (mixture * mask).squeeze(1)
