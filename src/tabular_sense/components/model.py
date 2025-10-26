import torch
from torch import Tensor
from torch.nn import Embedding, TransformerEncoderLayer, TransformerEncoder, Sequential, Linear, ReLU, Dropout, Module
from torch.nn.parameter import Parameter

from src.tabular_sense.components.config import Config
from src.tabular_sense.components.positional_encoding import positional_encoding
from src.tabular_sense.components.tokenizer import Tokenizer
from src.tabular_sense.core.constants import PAD_TOKEN_ID, ALL_TYPES


class Model(Module):
    embedding: Embedding
    cls_parameter: Parameter
    pos_encoding: Parameter
    encoder: TransformerEncoder
    classifier: Sequential

    def __init__(self, tokenizer: Tokenizer, config: Config):
        super().__init__()

        # 词嵌入
        self.embedding = Embedding(tokenizer.vocab_size, config.d_model, PAD_TOKEN_ID)
        # [CLS]分类参数
        self.cls_parameter = Parameter(torch.randn(1, 1, config.d_model))
        # 位置编码
        self.pos_encoding = positional_encoding(config.max_len, config.d_model)

        # Transformer编码器
        encoder_layer = TransformerEncoderLayer(
            d_model=config.d_model,
            nhead=config.n_head,
            dim_feedforward=config.d_model * 4,
            dropout=config.dropout,
            batch_first=True,
            norm_first=True,
        )
        self.encoder = TransformerEncoder(encoder_layer, config.n_encoder_layers, enable_nested_tensor=False)

        # 分类器
        self.classifier = Sequential(
            Linear(config.d_model, config.d_model * 2),
            ReLU(),
            Dropout(config.dropout),
            Linear(config.d_model * 2, config.d_model * 2),
            ReLU(),
            Dropout(config.dropout),
            Linear(config.d_model * 2, len(ALL_TYPES)),
        )

    def forward(self, input_ids: Tensor, attention_masks: Tensor) -> Tensor:
        batch_size, seq_len = input_ids.shape

        x = self.embedding(input_ids)

        cls_parameter = self.cls_parameter.expand(batch_size, -1, -1)
        x = torch.cat([cls_parameter, x], dim=1)

        x = x + self.pos_encoding[:, :seq_len + 1, :]

        cls_mask = torch.ones(batch_size, 1, device=x.device)
        attention_masks = torch.cat([cls_mask, attention_masks], dim=1)
        # src_key_padding_mask对mask的要求是1为屏蔽，这是torch的定义；但我的mask创建时按照HuggingFace的定义来，所以需要翻转语义
        attention_masks = (attention_masks == 0)
        encoded = self.encoder(x, src_key_padding_mask=attention_masks)

        cls_output = encoded[:, 0, :]

        return self.classifier(cls_output)

    @property
    def param_num(self) -> str:
        return f"{sum(p.numel() for p in self.parameters()) / 1e6:.1f}M"
