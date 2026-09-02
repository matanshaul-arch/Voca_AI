import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from voca_tse.dataset import mix_sources
from voca_tse.evaluation import si_sdr
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator


def main():
    torch.manual_seed(11)
    target, interferer = torch.randn(16000), torch.randn(16000)
    mixture, target, _, _ = mix_sources(target, interferer, snr_db=0)
    encoder = SpeakerEncoderAdapter()
    profile = encoder.enroll(target.unsqueeze(0))
    estimate = DualConditioningSeparator()(mixture.unsqueeze(0), profile.embedding.unsqueeze(0))
    print({"mixture_si_sdr": float(si_sdr(target.unsqueeze(0), mixture.unsqueeze(0)).mean().detach()),
           "estimate_si_sdr": float(si_sdr(target.unsqueeze(0), estimate).mean().detach())})


if __name__ == "__main__":
    main()
