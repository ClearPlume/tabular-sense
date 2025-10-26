import random


def generate_random_int_literal(strategy: int):
    if strategy == 1:
        # 普通十进制整数
        digits = random.randint(1, 19)
        return str(random.randint(-10 ** digits, 10 ** digits))

    elif strategy == 2:
        # 十六进制
        num = random.randint(0, 2 ** 32)
        prefix = random.choice(['0x', '0X'])
        return f"{prefix}{num:X}"

    elif strategy == 3:
        # 八进制
        num = random.randint(0, 2 ** 20)
        prefix = random.choice(['0o', '0O'])
        return f"{prefix}{num:o}"

    elif strategy == 4:
        # 二进制
        num = random.randint(0, 2 ** 20)
        prefix = random.choice(['0b', '0B'])
        return f"{prefix}{num:b}"

    elif strategy == 5:
        # 带后缀
        num = random.randint(-10 ** 10, 10 ** 10)
        suffix = random.choice(['L', 'U', 'UL', 'LL', 'l', 'u'])
        return f"{num}{suffix}"

    elif strategy == 6:
        # 带下划线分隔符
        num = random.randint(-10 ** 12, 10 ** 12)
        s = str(abs(num))
        # 每3位插入下划线
        parts = []
        for i in range(len(s) - 1, -1, -3):
            parts.append(s[max(0, i - 2):i + 1])
        result = '_'.join(reversed(parts))
        return f"{'-' if num < 0 else ''}{result}"

    elif strategy == 7:
        # 十六进制带下划线
        num = random.randint(0, 2 ** 32)
        hex_str = f"{num:X}"
        if len(hex_str) > 4:
            parts = [hex_str[i:i + 4] for i in range(0, len(hex_str), 4)]
            hex_str = '_'.join(parts)
        return f"0x{hex_str}"

    else:
        # 小数字
        return str(random.randint(-1000, 1000))


def ints(num: int) -> list[str]:
    strategy = random.randint(1, 8)
    samples = []

    for _ in range(num):
        samples.append(generate_random_int_literal(strategy))

    return samples
