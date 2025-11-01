"""
表格列语义分类推理接口
"""
import random

import torch
from torch import Tensor

from src.tabular_sense.components.config import Config
from src.tabular_sense.components.model import Model
from src.tabular_sense.components.tokenizer import Tokenizer
from src.tabular_sense.core.constants import RAW_CORPUS_PER_INPUT
from src.tabular_sense.core.enum_util import ColumnType


class ColumnClassifier:
    """表格列语义分类器"""

    tokenizer: Tokenizer
    model: Model
    device: torch.device

    def __init__(self, checkpoint_name: str = "2025-10-30"):
        """
        初始化分类器
        
        Args:
            checkpoint_name: 模型checkpoint名称，默认使用最新训练的模型
        """

        config = Config.final()
        self.tokenizer = Tokenizer()
        self.model = Model(self.tokenizer.vocab_size, config)
        self.model.load(checkpoint_name)
        self.device = config.device

    def predict(self, column_name: str, samples: list[str], threshold: float = 0.5) -> list[str]:
        """
        用于识别表格列的语义类型（日期、金额、姓名等32种类型）
        
        Args:
            column_name: 列名
            samples: 列的样本值
            threshold: 置信度阈值，默认0.5

        Returns:
            预测的类型标签列表
        
        Examples:
            >>> classifier = ColumnClassifier("2025-10-30")
            >>> result = classifier.predict(
            ...     column_name="phone",
            ...     samples=["13812345678", "13998765432"]*5
            ... )
            >>> print(result)
            ['PHONE']
        """

        logits = self._get_logits(column_name, samples)
        probabilities = torch.sigmoid(logits)
        predictions = (probabilities > threshold).float()

        return list(map(lambda t: t.name, ColumnType.from_multiple_label(predictions[0].tolist())))

    def predict_proba(self, column_name: str, samples: list[str], top_k: int = 5) -> dict[str, float]:
        """
        预测各类型的概率，返回最可能的前k个类型
        
        Args:
            column_name: 列名
            samples: 列的样本值
            top_k: 返回概率最高的前k个类型，默认为5

        Returns:
            dict[类型名, 概率]，按概率降序排列
        
        Examples:
            >>> classifier = ColumnClassifier("2025-10-30")
            >>> result = classifier.predict_proba(
            ...     column_name="phone",
            ...     samples=["13812345678", "13998765432"]
            ... )
            >>> print(result)  # doctest: +SKIP
            {'PHONE': 0.999955415725708, 'INT': 0.000799537927377969, 'DATETIME': 4.6166331912900205e-07, 'AMOUNT': 1.7105857841315242e-09, 'ID_CARD': 3.202490139395109e-12}
            >>> list(result.keys())[0]
            'PHONE'
            >>> result['PHONE'] > 0.99
            True
            >>> len(result)
            5
        """

        logits = self._get_logits(column_name, samples)
        probabilities = torch.sigmoid(logits)
        column_types = list(ColumnType)
        type_probabilities = {column_type.name: float(probabilities[0][idx]) for idx, column_type in
                              enumerate(column_types)}

        return dict(sorted(type_probabilities.items(), key=lambda x: x[1], reverse=True)[:top_k])

    @torch.no_grad()
    def _get_logits(self, column_name: str, samples: list[str]) -> Tensor:
        data = f"{column_name}|{"<sep>".join(random.choices(samples, k=RAW_CORPUS_PER_INPUT))}"
        encoded_data = self.tokenizer.encode(data)
        input_ = torch.tensor(encoded_data, device=self.device).unsqueeze(0)
        mask = torch.ones(len(encoded_data), device=self.device).unsqueeze(0)

        return self.model(input_, mask)
