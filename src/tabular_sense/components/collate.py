import torch
from torch import Tensor
from torch.nn.functional import pad

from src.tabular_sense.components.dataset import TokenizedColumnSample
from src.tabular_sense.core.constants import PAD_TOKEN_ID


def collate_fn(batch: list[TokenizedColumnSample]) -> dict[str, Tensor]:
    """完成分组后批次内数据的padding"""

    # [seq_len] * batch
    input_ids = [b.input for b in batch]
    # [n_classes] * batch
    labels = [b.target for b in batch]

    # Padding
    max_input_len = max(len(input_id) for input_id in input_ids)
    # [max_input_len] * batch
    padded_inputs: list[Tensor] = []
    # [max_input_len] * batch
    attention_masks: list[Tensor] = []

    for input_id in input_ids:
        padding_length = max_input_len - len(input_id)
        # 简单的右填充
        padded = pad(input=input_id, pad=(0, padding_length), value=PAD_TOKEN_ID)
        mask = torch.cat([torch.ones(len(input_id)), torch.zeros(padding_length)])

        padded_inputs.append(padded)
        attention_masks.append(mask)

    return {
        # [batch, max_input_len]
        "input_ids": torch.stack(padded_inputs),
        # [batch, max_input_len]
        "attention_masks": torch.stack(attention_masks),
        # [batch, n_classes]
        # loss计算需要标准类型为float
        "labels": torch.stack(labels).float(),
    }
