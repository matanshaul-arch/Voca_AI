import torch
from voca_tse.models import ComplexSTFTSeparator


def test_complex_stft_separator_shape_and_finite_values():
    torch.manual_seed(2)
    model = ComplexSTFTSeparator()
    mixture = torch.randn(2, 2048)
    embedding = torch.randn(2, 192)
    estimate = model(mixture, embedding)
    assert estimate.shape == mixture.shape
    assert torch.isfinite(estimate).all()


def test_complex_stft_separator_has_gradients():
    model = ComplexSTFTSeparator()
    estimate = model(torch.randn(1, 1024), torch.randn(1, 192))
    estimate.square().mean().backward()
    assert any(p.grad is not None for p in model.parameters())
