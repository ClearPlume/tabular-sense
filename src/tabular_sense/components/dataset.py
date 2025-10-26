import pickle
from dataclasses import dataclass
from pathlib import Path

import torch
from torch import Tensor, Generator
from torch.utils.data import Dataset, Subset, random_split

from src.tabular_sense.components.config import Config
from src.tabular_sense.components.tokenizer import Tokenizer
from src.tabular_sense.core.constants import VAL_RATIO, TEST_RATIO, RANDOM_SEED
from src.tabular_sense.core.enum_util import ColumnType


@dataclass
class ColumnSample:
    """
    单个原始列训练样本
    
    Attributes:
        input: 列名|样本1<sep>样本2<sep>样本3
        target: [1, 0, 1]
    """

    input: str
    target: list[int]


@dataclass
class TokenizedColumnSample:
    """
    单个列训练样本，已tokenized
    
    Attributes:
        input: 编码后的输入tokens
        target: 编码后的输出tokens
    """
    input: Tensor
    target: Tensor


class ColumnDataset(Dataset):
    """列数据集"""

    sample_file: Path
    tokenizer: Tokenizer
    config: Config
    offsets: list[int]

    def __init__(self, sample_file: Path, tokenizer: Tokenizer, config: Config):
        self.sample_file = sample_file
        self.tokenizer = tokenizer
        self.config = config
        self._prepare_offset()

    def _prepare_offset(self):
        _file = self.sample_file.open("r", encoding="utf-8")
        cache_file = self.sample_file.with_suffix(".offset.pkl")

        if cache_file.exists() and cache_file.stat().st_mtime > self.sample_file.stat().st_mtime:
            with open(cache_file, "rb") as cache:
                self.offsets = pickle.load(cache)
            return
        else:
            self.offsets = []

        self.offsets.append(_file.tell())
        while _file.readline():
            self.offsets.append(_file.tell())
        self.offsets.pop()

        cache_file.write_bytes(pickle.dumps(self.offsets))
        _file.close()

    def __len__(self):
        return len(self.offsets)

    # 样本文件结构为：可能类型,可能类型|列名|数据<sep>数据<sep>数据
    def __getitem__(self, idx) -> TokenizedColumnSample:
        _file = self.sample_file.open("r", encoding="utf-8")
        _file.seek(self.offsets[idx])
        sample = _file.readline().strip()
        _file.close()

        types, column_name, data = sample.split("|", maxsplit=2)
        encoded = self.tokenizer.encode(f"{column_name}|{data}")

        if len(encoded) > self.config.max_len:
            encoded = encoded[:self.config.max_len]

        return TokenizedColumnSample(
            torch.tensor(encoded),
            torch.tensor(ColumnType.to_multiple_label(*map(ColumnType.__getitem__, types.split(",")))),
        )

    def split(self) -> list[Subset["ColumnDataset"]]:
        total = len(self.offsets)
        val_size = int(total * VAL_RATIO)
        test_size = int(total * TEST_RATIO)
        train_size = total - val_size - test_size

        return random_split(self, [train_size, val_size, test_size], Generator().manual_seed(RANDOM_SEED))
