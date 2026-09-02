import torch
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator
from voca_tse.dataset import mix_sources


def test_mixer_shapes():
    result = mix_sources(torch.ones(10), torch.ones(8), torch.zeros(10))
    assert all(x.shape == (10,) for x in result)


def test_encoder_and_separator_shapes():
    torch.manual_seed(1)
    encoder = SpeakerEncoderAdapter()
    audio = torch.randn(2, 3200)
    embedding = encoder(audio)
    output = DualConditioningSeparator()(audio, embedding)
    assert embedding.shape == (2, 192)
    assert output.shape == audio.shape
