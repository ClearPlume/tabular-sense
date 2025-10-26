from dataclasses import dataclass

import torch
from torch import Tensor


@dataclass
class Metrics:
    """多标签指标结构"""
    precision: float
    recall: float
    f1: float
    hamming_loss: float
    em: float

    @property
    def score(self) -> float:
        return (
                0.5 * self.f1 +
                0.2 * self.precision +
                0.2 * self.recall +
                0.1 * self.em
        )


class MultiLabelMetrics:
    """多标签指标计算算法"""

    def __call__(self, all_predictions: list[Tensor], all_labels: list[Tensor]) -> Metrics:
        # 模型预测结果
        # [[1, 0, 1]
        #  [0, 1, 0]]
        predictions = torch.cat(all_predictions)  # 使用1减去结果，得到『模型预测为错误的结果』
        # 真实结果
        # [[1, 1, 0]
        #  [0, 1, 1]]
        labels = torch.cat(all_labels)  # 使用1减去结果，得到『实际为错误的结果』

        # 预测正确且真实正确的结果数
        # [[1*1, 0*1, 1*0]
        #  [0*0, 1*1, 0*1]]
        # [[1, 0, 0]
        #  [0, 1, 0]]
        tp = (predictions * labels).sum()  # 2
        # 预测为错误且真实错误的结果数
        # [[1-1, 1-0, 1-1]
        #  [1-0, 1-1, 1-0]]
        # [[1-1, 1-1, 1-0]
        #  [1-0, 1-1, 1-1]]
        # [[0*0, 1*0, 0*1]
        #  [1*1, 0*0, 1*0]]
        # [[0, 0, 0]
        #  [1, 0, 0]]
        tn = ((1 - predictions) * (1 - labels)).sum()  # 1
        # 预测正确但真实错误的结果数
        # [[1, 0, 1]
        #  [0, 1, 0]]
        # [[1-1, 1-1, 1-0]
        #  [1-0, 1-1, 1-1]]
        # [[1*0, 0*0, 1*1]
        #  [0*0, 1*0, 0*0]]
        # [[0, 0, 1]
        #  [0, 0, 0]]
        fp = (predictions * (1 - labels)).sum()  # 1
        # 预测错误但真实正确的结果数
        # [[1-1, 1-0, 1-1]
        #  [1-0, 1-1, 1-0]]
        # [[1, 1, 0]
        #  [0, 1, 1]]
        # [[0*1, 1*1, 0*0]
        #  [1*0, 0*1, 1*1]]
        # [[0, 1, 0]
        #  [0, 0, 1]]
        fn = ((1 - predictions) * labels).sum()  # 2

        total = predictions.numel()
        assert tp + tn + fp + fn == total, f"四类统计结果之和应为{total}，实际得到{tp + fp + fn + tn}，存在重复计数或漏统计"

        # 精确率，预测为正的样本中，真正为正的比例
        precision = tp / (tp + fp + 1e-10)

        # 召回率，真实为正的样本中，被预测出来的比例
        recall = tp / (tp + fn + 1e-10)

        # F1-Score，Precision 和 Recall 的调和平均
        f1 = 2 * precision * recall / (precision + recall + 1e-10)

        # Hamming Loss，平均每个标签位置上预测错误的比例
        incorrect = (predictions != labels).float()
        hamming_loss = incorrect.mean()  # incorrect.sum() / predictions.numel()

        # EM，所有标签完全预测正确的样本比例
        exact_match = (predictions == labels).all(1).float()
        em = exact_match.mean()  # exact_match.sum() / exact_match.shape[0]

        return Metrics(precision.item(), recall.item(), f1.item(), hamming_loss.item(), em.item())
