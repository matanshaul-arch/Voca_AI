import torch


def _fit(x, length):
    if x.numel() < length:
        x = torch.nn.functional.pad(x, (0, length - x.numel()))
    return x[:length]


def mix_sources(target, interferer, noise=None, snr_db=0.0):
    """Create a deterministic-length mixture and return mixture plus aligned sources."""
    length = max(target.numel(), interferer.numel(), noise.numel() if noise is not None else 0)
    target, interferer = _fit(target, length), _fit(interferer, length)
    if noise is None:
        noise = torch.zeros_like(target)
    else:
        noise = _fit(noise, length)
    target_rms = target.square().mean().sqrt().clamp_min(1e-8)
    interferer = interferer * (target_rms / interferer.square().mean().sqrt().clamp_min(1e-8)) * 10 ** (-snr_db / 20)
    mixture = target + interferer + noise
    peak = mixture.abs().max().clamp_min(1.0)
    return mixture / peak, target / peak, interferer / peak, noise / peak
