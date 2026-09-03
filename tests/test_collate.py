import torch
from voca_tse.dataset import collate_tse


def test_collate_pads_variable_lengths():
    batch = [{"mixture": torch.ones(4), "target": torch.ones(4), "interferer": torch.ones(4), "metadata": {}},
             {"mixture": torch.ones(7), "target": torch.ones(7), "interferer": torch.ones(7), "metadata": {}}]
    result = collate_tse(batch)
    assert result["mixture"].shape == (2, 7)
    assert result["lengths"].tolist() == [4, 7]
