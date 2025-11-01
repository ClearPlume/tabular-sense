import math


def d_model_calculator(
        vocab_size: int,
        total_token: int,
        token_per_param: int,
        n_encoder_layers: int,
        n_decoder_layers: int = 0
) -> int:
    """
    依据层数反推对应维度
    
    :param vocab_size: 词表大小
    :param total_token: 总token数(样本数 * 样本平均token长度)
    :param token_per_param: token参数比(5/10/20/50/100)，每参数从多少token处学习
    :param n_encoder_layers: 基于任务复杂度推断层数
    :param n_decoder_layers: 基于任务复杂度推断层数

    :return: 对齐到64倍数的维度
    """

    # 二次方程系数
    if n_decoder_layers > 0:
        # encoder-decoder架构
        a = 12 * n_encoder_layers + 16 * n_decoder_layers
        b = 2 * vocab_size  # 两个embedding
    else:
        # encoder-only架构
        a = 12 * n_encoder_layers
        b = vocab_size

    c = -(total_token / token_per_param)

    # 求根公式
    discriminant = b ** 2 - 4 * a * c
    d_model_raw = (-b + math.sqrt(discriminant)) / (2 * a)

    # 对齐到64倍
    if d_model_raw < 32:
        raise ValueError("任务可能不适合transformer，考虑更简单的架构")
    elif d_model_raw < 64:
        print("警告：接近transformer下限，建议检查配置")
        d_model = 64
    else:
        d_model = math.ceil(d_model_raw / 64) * 64

    return d_model
