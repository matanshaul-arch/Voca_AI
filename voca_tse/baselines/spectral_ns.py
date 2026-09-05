import torch


def spectral_noise_suppress(audio: torch.Tensor, n_fft: int = 512, hop_length: int = 128,
                            oversubtraction: float = 1.2, gain_floor: float = 0.08) -> torch.Tensor:
    """Offline spectral-subtraction baseline; it is not speaker conditioned."""
    if audio.ndim == 1:
        audio = audio.unsqueeze(0)
    window = torch.hann_window(n_fft, device=audio.device, dtype=audio.dtype)
    spectrum = torch.stft(audio, n_fft=n_fft, hop_length=hop_length, window=window,
                          return_complex=True, center=True)
    power = spectrum.abs().square()
    noise = torch.quantile(power, 0.15, dim=-1, keepdim=True)
    gain = ((power - oversubtraction * noise).clamp_min(0) / power.clamp_min(1e-8)).clamp(gain_floor, 1)
    return torch.istft(spectrum * gain, n_fft=n_fft, hop_length=hop_length, window=window,
                       length=audio.shape[-1], center=True)
