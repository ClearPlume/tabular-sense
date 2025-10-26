from enum import Enum


class ResumeStrategy(Enum):
    ALL_COMPONENTS = 0  # 恢复所有组件
    EXCLUDE_OPTIMIZATION = 1  # 排除优化相关（优化器+LR调度器）
    EXCLUDE_REGULARIZATION = 2  # 排除正则化相关（Dropout调度器）
    MODEL_WEIGHTS_ONLY = 3  # 仅模型权重
