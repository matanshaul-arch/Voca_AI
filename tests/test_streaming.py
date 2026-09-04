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


def test_separator_is_causal_and_streaming_matches_offline():
    torch.manual_seed(0)
    model = DualConditioningSeparator(embedding_dim=8, channels=8, blocks=4).eval()
    embedding = torch.randn(1, 8)
    signal = torch.randn(1, 640)
    changed = signal.clone()
    changed[:, 320:] += 10.0
    with torch.no_grad():
        first = model(signal, embedding)
        second = model(changed, embedding)
    assert torch.allclose(first[:, :320], second[:, :320], atol=1e-6)

    engine = StreamingTSE(model, embedding[0], context_samples=model.receptive_field)
    # Process sequentially so each chunk receives the preceding context.
    state = engine.create_state()
    chunks = []
    for i in range(0, 640, 160):
        output, state = engine.process(signal[0, i:i + 160], state)
        chunks.append(output)
    streamed = torch.cat(chunks, dim=-1)
    assert torch.allclose(streamed, first[0], atol=1e-5)
