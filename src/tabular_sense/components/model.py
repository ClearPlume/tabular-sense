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

        self.to(config.device)

        # 词嵌入，将词表中的每个token都映射到d_model维度的向量空间，初始值为随机浮点值
        # [[e0_0, e0_1, e0_2, ..., e0_{d_model-1}]  <- tokens[v0]
        #  [e1_0, e1_1, e1_2, ..., e1_{d_model-1}]  <- tokens[v1]
        #  [e2_0, e2_1, e2_2, ..., e2_{d_model-1}]  <- tokens[v2]
        #                     ...
        #  [eN_0, eN_1, eN_2, ..., eN_{d_model-1}]] <- tokens[v_{vocab_size-1}]
        # [vocab_size, d_model]
        self.embedding = Embedding(tokenizer.vocab_size, config.d_model, PAD_TOKEN_ID)
        # [CLS]分类参数，用于序列分类任务的全局表示，初始值为随机浮点值
        # [[[c_0, c_1, c_2, ..., c_{d_model-1}]]]
        # [1, 1, d_model]
        self.cls_parameter = Parameter(torch.randn(1, 1, config.d_model))
        # 位置编码
        # [1, max_len, d_model]
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
            # [batch, d_model*2]
            Linear(config.d_model, config.d_model * 2),
            ReLU(),
            Dropout(config.dropout),
            # [batch, d_model*2]
            Linear(config.d_model * 2, config.d_model * 2),
            ReLU(),
            Dropout(config.dropout),
            # [batch, n_classes]
            Linear(config.d_model * 2, len(ALL_TYPES)),
        )

    def forward(self, input_ids: Tensor, attention_masks: Tensor) -> Tensor:
        batch_size, seq_len = input_ids.shape

        # token_id映射为实际向量
        # [batch, seq_len, d_model]
        x = self.embedding(input_ids)

        # [batch, seq_len+1, d_model]
        cls_parameter = self.cls_parameter.expand(batch_size, -1, -1)
        x = torch.cat([cls_parameter, x], dim=1)

        # [batch, seq_len+1, d_model]
        x = x + self.pos_encoding[:, :seq_len + 1, :]

        # cls元素为明确不需要mask的部分，所以直接构建值为1的张量
        # [[1]  <- input_0
        #  [1]  <- input_1
        #  [1]  <- input_2
        #  ...
        #  [1]] <- input_batch-1
        # [batch, 1]
        cls_mask = torch.ones(batch_size, 1, device=x.device)
        # 在第一个维度将cls的mask和输入的mask连接
        # [[1, 1, 1, ..., 1]  <- input_0
        #  [1, 1, 1, ..., 1]  <- input_1
        #  [1, 1, 1, ..., 1]  <- input_2
        #  ...
        #  [1, 1, 1, ..., 1]] <- input_batch-1
        # [batch, seq_len+1]
        attention_masks = torch.cat([cls_mask, attention_masks], dim=1)

        # PyTorch的src_key_padding_mask约定：True表示屏蔽该位置
        # 输入的attention_masks遵循HuggingFace约定：1表示有效，0表示padding
        # 因此需要翻转：将0（padding）转为True（屏蔽）
        attention_masks = attention_masks == 0
        # 将初始向量和mask送入编码器
        # [batch, seq_len+1, d_model]
        encoded = self.encoder(x, src_key_padding_mask=attention_masks)

        # 张量切片语法，获取第一和第三维全部数据，只取第二维的第一个元素，消除第二个维度
        # 切片语法中，标量索引意味着消除对应维度；如果要保留维度，需要使用切片索引
        # [batch, d_model]
        cls_output = encoded[:, 0, :]

        # [batch, n_classes]
        return self.classifier(cls_output)

    @property
    def param_num(self) -> str:
        return f"{sum(p.numel() for p in self.parameters()) / 1e6:.1f}M"
