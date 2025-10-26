import random
import re
from random import randint


def generate_ipv4_variants(variant: int):
    """生成IPv4及其变体"""
    base_ip = f"{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"

    variants = [
        base_ip,  # 192.168.1.1
        f"{base_ip}/{randint(0, 32)}",  # 192.168.1.0/24
        f"{base_ip}:{randint(1, 65535)}",  # 192.168.1.1:8080
    ]

    # 可选：通配符（较少见）
    if random.random() < 0.1:
        parts = base_ip.split('.')
        parts[randint(0, 3)] = '*'
        variants.append('.'.join(parts))

    return variants[variant]


def generate_ipv6_variants(variant: int):
    """生成IPv6及其变体"""
    # 1. 生成各段（长度随机1-4位）
    segments = []
    for _ in range(8):
        length = random.choice([1, 2, 3, 4])
        max_val = 16 ** length - 1
        min_val = 16 ** (length - 1) if length > 1 else 0
        segments.append(f"{randint(min_val, max_val):x}")

    base_ip = ':'.join(segments)

    # 2. 30%概率压缩连续的0段
    if random.random() < 0.3:
        # 替换连续的 :0: 或开头的 0: 或结尾的 :0 为 ::
        base_ip = re.sub(r'(:0)+:', '::', base_ip, count=1)
        # 处理边界情况
        base_ip = re.sub(r'^0::', '::', base_ip)
        base_ip = re.sub(r'::0$', '::', base_ip)

    # 3. 生成变体
    variants = [
        base_ip,  # 标准
        f"{base_ip}/{randint(0, 128)}",  # CIDR
        f"[{base_ip}]:{randint(1, 65535)}",  # 带端口
    ]

    # IPv4映射格式（较少见）
    if random.random() < 0.1:
        ipv4_mapped = f"::ffff:{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"
        variants.append(ipv4_mapped)

    return variants[variant]


def ips(num: int) -> list[str]:
    variant = random.randint(0, 2)
    samples = []

    if random.random() < 0.5:
        for _ in range(num):
            samples.append(generate_ipv4_variants(variant))
    else:
        for _ in range(num):
            samples.append(generate_ipv6_variants(variant))

    return samples
