import torch
import torch.nn.functional as F


def si_sdr_loss(reference: torch.Tensor, estimate: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
    reference = reference - reference.mean(dim=-1, keepdim=True)
    estimate = estimate - estimate.mean(dim=-1, keepdim=True)
    scale = (estimate * reference).sum(-1, keepdim=True) / (reference.square().sum(-1, keepdim=True) + eps)
    target = scale * reference
    noise = estimate - target
    return -10 * torch.log10((target.square().sum(-1) + eps) / (noise.square().sum(-1) + eps)).mean()


class ContrastiveTSELoss(torch.nn.Module):
    def __init__(self, speaker_encoder, lambda_contrastive=0.1, lambda_leakage=0.1, margin=0.4):
        super().__init__()
        self.speaker_encoder = speaker_encoder
        self.lambda_contrastive = lambda_contrastive
        self.lambda_leakage = lambda_leakage
        self.margin = margin

    def forward(self, target, estimate, negative=None, return_components=False):
        total = si_sdr_loss(target, estimate)
        pos = self.speaker_encoder(estimate)
        target_e = self.speaker_encoder(target).detach()
        contrastive = torch.zeros((), device=estimate.device)
        leakage = torch.zeros((), device=estimate.device)
        if negative is not None:
            neg_e = self.speaker_encoder(negative).detach()
            pos_distance = 1 - F.cosine_similarity(pos, target_e, dim=-1)
            neg_distance = 1 - F.cosine_similarity(pos, neg_e, dim=-1)
            contrastive = F.relu(pos_distance - neg_distance + self.margin).mean()
            leakage = F.cosine_similarity(estimate, negative, dim=-1).abs().mean()
            total = total + self.lambda_contrastive * contrastive + self.lambda_leakage * leakage
        if return_components:
            return total, {"si_sdr": total.detach(), "contrastive": contrastive.detach(), "leakage": leakage.detach()}
        return total
