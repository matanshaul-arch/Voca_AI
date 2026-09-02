import wave
from pathlib import Path
import torch


def load_wav(path, expected_sample_rate=16000):
    path = Path(path)
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_rate = handle.getframerate()
        sample_width = handle.getsampwidth()
        frames = handle.readframes(handle.getnframes())
    if channels != 1:
        raise ValueError(f"expected mono WAV, got {channels} channels: {path}")
    if sample_rate != expected_sample_rate:
        raise ValueError(f"expected {expected_sample_rate}Hz, got {sample_rate}Hz: {path}")
    if sample_width != 2:
        raise ValueError(f"expected 16-bit PCM WAV, got {sample_width * 8}-bit: {path}")
    audio = torch.frombuffer(bytearray(frames), dtype=torch.int16).clone().float() / 32768.0
    return audio
