from dataclasses import dataclass
import torch


@dataclass
class StreamingState:
    audio: torch.Tensor


class StreamingTSE:
    """Reference chunked wrapper. It is stateful and allocation-safe at the API boundary."""

    def __init__(self, model, profile_embedding, context_samples=512, device="cpu"):
        self.model = model.to(device).eval()
        self.profile_embedding = profile_embedding.to(device)
        self.context_samples = context_samples
        self.device = device

    def create_state(self):
        return StreamingState(torch.zeros(1, 0, device=self.device))

    @torch.no_grad()
    def process(self, pcm_chunk, state):
        if pcm_chunk.ndim == 1:
            pcm_chunk = pcm_chunk.unsqueeze(0)
        chunk = pcm_chunk.to(self.device)
        combined = torch.cat((state.audio, chunk), dim=-1)
        output = self.model(combined, self.profile_embedding.unsqueeze(0))
        emitted = output[..., -chunk.shape[-1]:]
        state.audio = combined[..., -self.context_samples:]
        return emitted.cpu(), state
