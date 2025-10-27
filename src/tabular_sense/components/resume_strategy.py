from enum import Enum


class ResumeStrategy(Enum):
    """
    训练恢复策略枚举
      
    定义从检查点恢复训练时需要加载哪些组件的策略。
    用于控制模型权重、优化器状态、学习率调度器和Dropout调度器等组件的恢复行为。
    
    Attributes:
        ALL_COMPONENTS: 恢复所有组件
        EXCLUDE_OPTIMIZATION: 排除优化相关（优化器+LR调度器）
        EXCLUDE_REGULARIZATION: 排除正则化相关（Dropout调度器）
        MODEL_WEIGHTS_ONLY: 仅模型权重
    """

    ALL_COMPONENTS = 0
    EXCLUDE_OPTIMIZATION = 1
    EXCLUDE_REGULARIZATION = 2
    MODEL_WEIGHTS_ONLY = 3
