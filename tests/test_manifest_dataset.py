import json
import wave
import torch
from voca_tse.dataset import ManifestTSEDataset


def _write_wav(path, samples, rate=16000):
    pcm = (samples.clamp(-1, 1) * 32767).short().numpy().tobytes()
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1); handle.setsampwidth(2); handle.setframerate(rate)
        handle.writeframes(pcm)


def test_manifest_dataset_loads_mono_pcm(tmp_path):
    samples = torch.linspace(-0.2, 0.2, 160)
    for name in ("mix.wav", "target.wav", "interferer.wav", "enrollment.wav"):
        _write_wav(tmp_path / name, samples)
    manifest = tmp_path / "manifest.jsonl"
    record = {"root": str(tmp_path), "mixture": "mix.wav", "target": "target.wav", "interferer": "interferer.wav", "enrollment": "enrollment.wav"}
    manifest.write_text(json.dumps(record) + "\n")
    item = ManifestTSEDataset(manifest)[0]
    assert item["mixture"].shape == (160,)
    assert torch.allclose(item["target"], samples, atol=1e-4)
    assert torch.allclose(item["enrollment"], samples, atol=1e-4)
