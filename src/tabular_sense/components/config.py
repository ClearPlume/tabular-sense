from dataclasses import dataclass

import torch


@dataclass
class Config:
    """模型配置信息"""

    d_model: int
    n_head: int
    n_encoder_layers: int
    learning_rate: float
    dropout: float
    max_dropout: float

    batch_size: int = 24
    max_len: int = 512
    max_grad_norm: float = 1.0
    device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def small(learning_rate=8e-5, dropout=0.2, max_dropout=0.4):
        return Config(512, 8, 8, learning_rate, dropout, max_dropout)

    @staticmethod
    def medium(learning_rate=5e-5, dropout=0.15, max_dropout=0.3):
        return Config(768, 12, 8, learning_rate, dropout, max_dropout)

    @staticmethod
    def large(learning_rate=5e-5, dropout=0.1, max_dropout=0.2):
        return Config(1024, 16, 16, learning_rate, dropout, max_dropout)
