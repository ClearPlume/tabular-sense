"""
表格列语义分类推理接口
"""
from pathlib import Path
from typing import Union

import torch


class ColumnClassifier:
    """表格列语义分类器
    
    用于识别表格列的语义类型（日期、金额、姓名等32种类型）
    
    Examples:
        >>> classifier = ColumnClassifier()
        >>> result = classifier.predict(
        ...     column_name="phone",
        ...     samples=["13812345678", "13998765432"]
        ... )
        >>> print(result)
        ['手机号']
    """

    def __init__(self, model_path: Union[str | Path] = None, device: Union[str | torch.device] = None):
        """
        初始化分类器
        
        :param model_path: 模型checkpoint路径，默认使用最新训练的模型
        :param device: 运行设备，默认自动选择
        """

        raise NotImplementedError("推理接口正在开发中，将在v1.0版本提供。")

    def predict(self, column_name: str, samples: list[str], threshold=0.5) -> list[str]:
        """
        预测列的语义类型
        
        :param column_name: 列名
        :param samples: 列的样本值
        :param threshold: 置信度阈值，默认0.5

        :return: 预测的类型标签列表
        """

        raise NotImplementedError("开发中")

    def predict_proba(self, column_name: str, samples: list[str]) -> dict[str, float]:
        """
        预测各类型的概率
        
        :return: dict[类型名, 概率]
        """
        raise NotImplementedError("开发中")
