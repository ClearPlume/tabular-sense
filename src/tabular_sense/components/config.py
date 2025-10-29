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
    batch_size: int

    min_delta: float = 1e-6
    max_len: int = 512
    max_grad_norm: float = 1.0
    device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def __str__(self):
        return (
            f"{self.d_model}d×{self.n_head}h×{self.n_encoder_layers}L | "
            f"lr={self.learning_rate} | dropout={self.dropout}→{self.max_dropout} | "
            f"batch={self.batch_size}"
        )

    @staticmethod
    # 3.1M，对应160k样本
    def micro(learning_rate=8e-5, dropout=0.2, max_dropout=0.4, batch_size=32):
        return Config(128, 2, 2, learning_rate, dropout, max_dropout, batch_size)

    @staticmethod
    # 37.3M，对应16k样本
    def small(learning_rate=8e-5, dropout=0.2, max_dropout=0.4, batch_size=32):
        return Config(512, 8, 8, learning_rate, dropout, max_dropout, batch_size)

    @staticmethod
    # 76.0M，对应160k样本
    def medium(learning_rate=5e-5, dropout=0.15, max_dropout=0.3, batch_size=32):
        return Config(768, 12, 8, learning_rate, dropout, max_dropout, batch_size)

    @staticmethod
    # 228.9M，对应960k样本
    def large(learning_rate=1e-5, dropout=0.1, max_dropout=0.2, batch_size=24):
        return Config(1024, 16, 16, learning_rate, dropout, max_dropout, batch_size)
