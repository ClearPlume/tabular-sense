import csv
import random
from pathlib import Path

from src.tabular_sense.path import get_data_dir


def luhn_checksum(card_number: str) -> int:
    """计算Luhn校验位"""

    def digits_of(n: str | int) -> list[int]:
        return [int(digit) for digit in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))

    return (10 - (checksum % 10)) % 10


def chunk_string(s: str, chunk_size: int = 4):
    # 用列表推导切分字符串
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]


def generate_card_from_bin(bin_info: dict[str, str]) -> str:
    """根据BIN信息生成完整银行卡号"""
    bin_code = str(bin_info['bin'])
    card_length = int(bin_info['card_length'])
    bin_length = int(bin_info['bin_length'])

    # 计算中间需要的随机数字位数
    middle_len = card_length - bin_length - 1  # -1是校验位

    if middle_len < 0:
        raise ValueError(f"卡号长度 {card_length} 小于 BIN长度 {bin_length} + 1")

    # 生成中间随机部分
    middle = ''.join([str(random.randint(0, 9)) for _ in range(middle_len)])

    # 拼接（不含校验位）
    card_without_check = bin_code + middle

    # 计算Luhn校验位
    check_digit = luhn_checksum(card_without_check)

    return card_without_check + str(check_digit)


def load_bin_data(csv_path: Path) -> list[dict[str, str]]:
    """加载BIN数据"""
    bin_infos = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            bin_infos.append({
                'bank_name': row[0],  # 银行名
                'bank_code': row[1],  # 机构代码
                'bank_abbr': row[2],  # 英文简称
                'card_name': row[3],  # 卡名
                'card_type': row[4],  # 卡类型代码
                'card_length': row[5],  # 卡号长度
                'bin': row[6],  # BIN
                'bin_length': row[7],  # BIN长度
            })

    return bin_infos


def bank_cards(num: int) -> list[str]:
    bin_infos = load_bin_data(get_data_dir() / 'seed/bank-bin.csv')
    choice = random.random()
    cards = []

    for _ in range(num):
        bin_info: dict[str, str] = random.choice(bin_infos)
        card = generate_card_from_bin(bin_info)

        # 普通连写
        if choice < 0.4:
            card = card
        # 空格分隔
        elif choice < 0.7:
            card = " ".join(chunk_string(card))
        # 连线分隔
        else:
            card = "-".join(chunk_string(card))

        cards.append(card)

    return cards
