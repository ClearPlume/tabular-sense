import math

import torch
from torch.nn.parameter import Parameter


def positional_encoding(max_len: int, d_model: int):
    # [CLS]
    max_len = max_len + 1
    
    # [[0, 0, 0, ..., 0]   <- 位置0
    #  [0, 0, 0, ..., 0]   <- 位置1
    #  [0, 0, 0, ..., 0]   <- 位置2
    #         ...
    #  [0, 0, 0, ..., 0]]  <- 位置max_len-1
    #   ↑  ↑  ↑       ↑
    #   0  1  2    d_model-1
    pos_e = torch.zeros(max_len, d_model)
    # [0, 1, 2, 3, ..., max_len-1]
    # [[0], [1], [2], [3], ..., [max_len-1]]
    position = torch.arange(0, max_len).unsqueeze(1).float()
    # 个人理解: 等待被sin/cos转化的，间隔为1的『运算占位符』
    # 正式术语: 频率项/相位参数
    # 数学本质: 正弦函数的自变量
    div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))

    # 使用sin计算占位符，为0、2、4、6、d_model-2 维设置位置编码
    pos_e[:, 0::2] = torch.sin(position * div_term)
    # 使用cos计算占位符，为1、3、5、7、d_model-1 维设置位置编码
    pos_e[:, 1::2] = torch.cos(position * div_term)

    # [[sin(0*f0), cos(0*f0), sin(0*f1), ..., cos(0*fn)]   <- 位置0
    #  [sin(1*f0), cos(1*f0), sin(1*f1), ..., cos(1*fn)]   <- 位置1
    #  [sin(2*f0), cos(2*f0), sin(2*f1), ..., cos(2*fn)]   <- 位置2
    #                   ...
    #  [sin(n*f0), cos(n*f0), sin(n*f1), ..., cos(0*fn)]]  <- 位置max_len-1
    #     ↑          ↑          ↑               ↑
    #     0          1          2            d_model-1

    # 这是绝对位置编码，无需学习
    # [[[sin(0*f0), cos(0*f0), sin(0*f1), ..., cos(0*fn)]    <- 位置0
    #   [sin(1*f0), cos(1*f0), sin(1*f1), ..., cos(1*fn)]    <- 位置1
    #   [sin(2*f0), cos(2*f0), sin(2*f1), ..., cos(2*fn)]    <- 位置2
    #                    ...
    #   [sin(n*f0), cos(n*f0), sin(0*f1), ..., cos(n*fn)]]]  <- 位置max_len-1
    #      ↑          ↑          ↑               ↑
    #      0          1          2            d_model-1
    return Parameter(pos_e.unsqueeze(0), requires_grad=False)
