import torch
from voca_tse.baselines import spectral_noise_suppress


def test_spectral_noise_suppress_preserves_shape_and_finite_values():
    audio = torch.randn(2, 2048)
    output = spectral_noise_suppress(audio)
    assert output.shape == audio.shape
    assert torch.isfinite(output).all()
