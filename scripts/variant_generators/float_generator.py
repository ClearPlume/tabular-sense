import math
import random
import sys


def generate_random_float_literal(strategy: int):
    if strategy == 1:
        # 普通小数 - 扩大范围和位数
        decimal_places = random.randint(1, 15)  # 增加小数位
        num = random.uniform(-10 ** 15, 10 ** 15)  # 扩大整数部分
        return f"{num:.{decimal_places}f}"

    elif strategy == 2:
        # 科学计数法 - 扩大指数范围
        base = random.uniform(0.1, 10)
        exp = random.randint(-50, 50)  # 从-20扩大到-50~50
        e_char = random.choice(['e', 'E'])
        sign = random.choice(['-', '+', ''])
        base_decimals = random.randint(1, 10)
        return f"{base:.{base_decimals}f}{e_char}{sign}{abs(exp)}"

    elif strategy == 3:
        # 带f/F后缀 - 增加位数
        num = random.uniform(-10 ** 12, 10 ** 12)
        suffix = random.choice(['f', 'F'])
        return f"{num:.{random.randint(1, 12)}f}{suffix}"

    elif strategy == 4:
        # 带d/D后缀
        num = random.uniform(-10 ** 12, 10 ** 12)
        suffix = random.choice(['d', 'D'])
        return f"{num:.{random.randint(1, 12)}f}{suffix}"

    elif strategy == 5:
        # 科学计数法 + 后缀
        base = random.uniform(0.1, 10)
        exp = random.randint(-50, 50)
        e_char = random.choice(['e', 'E'])
        suffix = random.choice(['f', 'F', 'd', 'D', ''])
        return f"{base:.{random.randint(1, 8)}f}{e_char}{exp}{suffix}"

    elif strategy == 6:
        # 十六进制浮点
        integer_part = random.randint(0, 15)
        frac_part = ''.join(random.choices('0123456789abcdef', k=random.randint(1, 12)))
        exp = random.randint(-20, 20)
        p_char = random.choice(['p', 'P'])
        return f"0x{integer_part:x}.{frac_part}{p_char}{exp}"

    elif strategy == 7:
        # 十六进制浮点 + 后缀
        integer_part = random.randint(0, 15)
        frac_part = ''.join(random.choices('0123456789ABCDEF', k=random.randint(1, 12)))
        exp = random.randint(-20, 20)
        suffix = random.choice(['f', 'F', 'd', 'D'])
        return f"0x{integer_part:X}.{frac_part}p{exp}{suffix}"

    elif strategy == 8:
        # 超多小数位
        frac = random.uniform(0, 1)
        return f"{frac:.{random.randint(10, 20)}f}"

    elif strategy == 9:
        # 大整数部分 + 多位小数
        integer = random.randint(-10 ** 15, 10 ** 15)
        frac = random.random()
        decimals = random.randint(5, 15)
        return f"{integer + frac:.{decimals}f}"

    else:
        # 特殊值
        special_numbers = [
            0.0,
            1.0,
            -1.0,
            0.5,
            math.pi,
            math.e,
            math.inf,
            -math.inf,
            math.nan,
            math.tau,
            math.sqrt(2),
            math.sqrt(3),
            math.sqrt(5),
            math.cbrt(2),
            math.cbrt(3),
            math.log(2),
            math.log10(2),
            math.exp(2),
            math.pi / 2,
            (1 + math.sqrt(5)) / 2,
            sys.float_info.max,
            sys.float_info.min,
            sys.float_info.min / 2,
            sys.float_info.epsilon,
            sys.float_info.min * sys.float_info.epsilon,
            sys.float_info.min_exp,
            sys.float_info.min_10_exp,
            sys.float_info.max_exp,
            sys.float_info.max_10_exp,
        ]
        return str(round(random.choice(special_numbers), random.randint(1, 10)))


def floats(num: int) -> list[str]:
    strategy = random.randint(1, 10)
    samples = []

    for _ in range(num):
        samples.append(generate_random_float_literal(strategy))

    return samples
