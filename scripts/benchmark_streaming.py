import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from voca_tse.inference import StreamingTSE
from voca_tse.models import SpeakerEncoderAdapter, DualConditioningSeparator


def main():
    torch.manual_seed(3)
    encoder, model = SpeakerEncoderAdapter(), DualConditioningSeparator()
    profile = encoder.enroll(torch.randn(1, 3200))
    engine = StreamingTSE(model, profile.embedding, context_samples=512)
    state = engine.create_state()
    chunks = [torch.randn(160) for _ in range(50)]
    start = time.perf_counter()
    for chunk in chunks:
        _, state = engine.process(chunk, state)
    elapsed = time.perf_counter() - start
    per_chunk_ms = elapsed / len(chunks) * 1000
    print(f"chunks={len(chunks)} per_chunk_ms={per_chunk_ms:.3f} realtime_budget_ms=10.000")
    if per_chunk_ms >= 10:
        raise SystemExit("streaming benchmark exceeded the 10ms processing budget")


if __name__ == "__main__":
    main()
