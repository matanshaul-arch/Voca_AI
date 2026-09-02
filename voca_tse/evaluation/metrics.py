import torch


def _center(x):
    return x - x.mean(dim=-1, keepdim=True)


def si_sdr(reference, estimate, eps=1e-8):
    reference, estimate = _center(reference), _center(estimate)
    scale = (estimate * reference).sum(-1, keepdim=True) / (reference.square().sum(-1, keepdim=True) + eps)
    target = scale * reference
    residual = estimate - target
    return 10 * torch.log10((target.square().sum(-1) + eps) / (residual.square().sum(-1) + eps))


def rms(audio, eps=1e-8):
    return audio.square().mean(dim=-1).sqrt().clamp_min(eps)


def suppression_db(interferer, estimate, eps=1e-8):
    return 20 * torch.log10(rms(interferer, eps) / rms(estimate, eps))
