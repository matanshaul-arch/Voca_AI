from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator
from voca_tse.losses import ContrastiveTSELoss
from voca_tse.dataset import mix_sources


def main():
    torch.manual_seed(7)
    target = torch.randn(16000)
    interferer = torch.randn(16000)
    noise = 0.02 * torch.randn(16000)
    mixture, target, interferer, _ = mix_sources(target, interferer, noise, snr_db=0)
    encoder = SpeakerEncoderAdapter()
    profile = encoder.enroll(target.unsqueeze(0))
    model = DualConditioningSeparator()
    estimate = model(mixture.unsqueeze(0), profile.embedding.unsqueeze(0))
    loss = ContrastiveTSELoss(encoder)(target.unsqueeze(0), estimate, interferer.unsqueeze(0))
    assert estimate.shape == target.unsqueeze(0).shape
    assert torch.isfinite(loss)
    print(f"smoke test passed; output={tuple(estimate.shape)} loss={loss.item():.3f}")


if __name__ == "__main__":
    main()
