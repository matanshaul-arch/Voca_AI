import soundfile as sf
import torch

from voca_tse.app.service import LocalTSEService, SAMPLE_RATE
from voca_tse.models import DualConditioningSeparator


def test_local_service_preview_separate_and_delete(tmp_path):
    checkpoint = tmp_path / "model.pt"
    torch.save({"model": DualConditioningSeparator().state_dict(), "encoder_backend": "fallback",
                "lambda_level": 0.03}, checkpoint)
    enrollment = tmp_path / "enrollment.wav"
    mixture = tmp_path / "mixture.wav"
    samples = torch.randn(640).clamp(-0.5, 0.5).numpy()
    sf.write(enrollment, samples, SAMPLE_RATE)
    sf.write(mixture, samples, SAMPLE_RATE)
    service = LocalTSEService(checkpoint, tmp_path / "jobs", tmp_path / "cache")
    preview = service.preview(enrollment)
    assert preview["duration_seconds"] > 0
    result = service.separate(enrollment, mixture)
    assert result.output_path.is_file()
    assert result.realtime_factor >= 0
    assert service.delete(result.job_id)
    assert not result.output_path.exists()
