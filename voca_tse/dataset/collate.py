import torch
from torch.nn.utils.rnn import pad_sequence


def collate_tse(batch):
    """Pad variable-length manifest records and retain original lengths."""
    lengths = torch.tensor([item["mixture"].numel() for item in batch], dtype=torch.long)
    return {
        "mixture": pad_sequence([item["mixture"] for item in batch], batch_first=True),
        "target": pad_sequence([item["target"] for item in batch], batch_first=True),
        "interferer": pad_sequence([item["interferer"] for item in batch], batch_first=True),
        "lengths": lengths,
        "metadata": [item["metadata"] for item in batch],
    }
