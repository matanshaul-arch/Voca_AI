import torch
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator
from voca_tse.inference import StreamingTSE


def test_streaming_output_is_continuous_in_shape():
    torch.manual_seed(2)
    encoder = SpeakerEncoderAdapter()
    model = DualConditioningSeparator()
    profile = encoder.enroll(torch.randn(1, 3200))
    engine = StreamingTSE(model, profile.embedding, context_samples=256)
    state = engine.create_state()
    chunks = [torch.randn(160) for _ in range(4)]
    outputs = []
    for chunk in chunks:
        output, state = engine.process(chunk, state)
        outputs.append(output)
    assert all(x.shape == (1, 160) for x in outputs)
    assert state.audio.shape[-1] <= 256
