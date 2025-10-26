import random


def generate_percentage(representation: str, explicit_format: int):
    # 1. 生成数值（真实的百分比值，比如50代表50%）
    value_strategies = [
        lambda: random.uniform(0, 100),  # 常规 0-100%
        lambda: random.uniform(100, 500),  # 超过100%
        lambda: random.uniform(-50, 0),  # 负值
        lambda: random.uniform(0, 1),  # 小于1%
        lambda: random.uniform(0.01, 0.1),  # 极小值
    ]
    percentage_value = random.choice(value_strategies)()

    if representation == 'explicit':
        # 形式A：显式百分比（带%符号）
        return generate_explicit_format(percentage_value, explicit_format)

    elif representation == 'decimal':
        # 形式B：小数形式（0.50 = 50%）
        return generate_decimal_format(percentage_value, explicit_format)

    else:  # numeric
        # 形式C：数值形式（50 = 50%，不带%）
        return generate_numeric_format(percentage_value, explicit_format)


def generate_explicit_format(value, strategy):
    """显式百分比：50.5%"""
    decimal_places = random.choice([0, 1, 2, 3])

    formats = [
        # 标准格式
        f"{value:.{decimal_places}f}%",

        # 空格变体
        f"{value:.{decimal_places}f} %",

        # 符号变体
        f"+{abs(value):.{decimal_places}f}%",
        f"-{abs(value):.{decimal_places}f}%",

        # 英文变体
        f"{value:.{decimal_places}f} percent",
        f"{value:.{decimal_places}f}pct",
        f"{value:.{decimal_places}f} pc",

        # 范围变体
        f"{value:.{decimal_places}f}%-{value + random.uniform(5, 20):.{decimal_places}f}%",
        f"{value:.{decimal_places}f}~{value + random.uniform(5, 20):.{decimal_places}f}%",
    ]

    return formats[strategy]


def generate_decimal_format(value, strategy):
    """小数形式：0.505 = 50.5%"""
    decimal_value = value / 100  # 50% → 0.50

    decimal_places = random.choice([2, 3, 4, 5, 6])

    formats = [
        f"{decimal_value:.{decimal_places}f}",  # 0.505000
        f"{decimal_value:g}",  # 0.505（自动去除多余0）
    ]

    # 符号变体
    if value > 0:
        formats.append(f"+{decimal_value:.{decimal_places}f}")
    elif value < 0:
        formats.append(f"{decimal_value:.{decimal_places}f}")  # 已经带负号

    return formats[strategy]


def generate_numeric_format(value, strategy):
    """数值形式：50.5 = 50.5%（不带%符号）"""
    decimal_places = random.choice([0, 1, 2, 3])

    formats = [
        f"{value:.{decimal_places}f}",  # 50.5
        f"{value:g}",  # 50.5（自动格式）
    ]

    # 符号变体
    if value > 0:
        formats.append(f"+{value:.{decimal_places}f}")
    else:
        formats.append(f"{value:.{decimal_places}f}")

    # 整数形式
    if value == int(value):
        formats.append(str(int(value)))
    else:
        formats.append(str(float(value)))

    return formats[strategy]


def percents(num: int) -> list[str]:
    representations = [('explicit', 8), ('decimal', 2), ('numeric', 3)]
    samples = []

    representation, format_num = random.choice(representations)
    explicit_format = random.randint(0, format_num)

    for _ in range(num):
        samples.append(generate_percentage(representation, explicit_format))

    return samples
