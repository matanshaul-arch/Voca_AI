from pathlib import Path
import torch
from torch.utils.data import Dataset
from .audio_io import load_wav
from .manifest import read_manifest, validate_record


class ManifestTSEDataset(Dataset):
    """Loads aligned mixture/target/interferer WAV triples from a JSONL manifest."""

    def __init__(self, manifest_path, sample_rate=16000):
        self.records = read_manifest(manifest_path)
        for record in self.records:
            validate_record(record)
        self.sample_rate = sample_rate

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        record = self.records[index]
        root = Path(record.get("root", "."))
        return {
            "mixture": load_wav(root / record["mixture"], self.sample_rate),
            "target": load_wav(root / record["target"], self.sample_rate),
            "interferer": load_wav(root / record["interferer"], self.sample_rate),
            "enrollment": load_wav(root / record.get("enrollment", record["target"]), self.sample_rate),
            "metadata": record,
        }
