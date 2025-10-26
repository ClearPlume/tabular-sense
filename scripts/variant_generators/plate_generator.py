import random

# ==================== 基础数据 ====================

# 31个省份的所有简称
PROVINCES = [
    '京', '津', '冀', '晋', '蒙',
    '辽', '吉', '黑',
    '沪', '苏', '浙', '皖', '闽', '赣', '鲁',
    '豫', '鄂', '湘',
    '粤', '桂', '琼',
    '渝', '川', '蜀', '贵', '黔', '云', '滇', '藏',
    '陕', '秦', '甘', '陇', '青', '宁', '新',
]

# 排除I、O的字母
LETTERS_NO_IO = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

# 排除I、O的字母+数字
CHARS_NO_IO = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'

# 军区代码
MILITARY_CODES = ['北', '沈', '兰', '济', '南', '广', '成', '新']

# 分隔符
SEPARATORS = ['', '-', '·', ' ']  # 空字符串表示无分隔符


# ==================== 生成函数 ====================

def generate_standard():
    """标准民用车牌（蓝牌）"""
    province = random.choice(PROVINCES)
    city = random.choice(LETTERS_NO_IO)
    suffix = ''.join(random.choices(CHARS_NO_IO, k=5))
    return f"{province}{city}{suffix}"


def generate_new_energy_small():
    """新能源小型车（绿牌）- 6位，第1位是D或F"""
    province = random.choice(PROVINCES)
    city = random.choice(LETTERS_NO_IO)
    first = random.choice('DF')
    rest = ''.join(random.choices(CHARS_NO_IO, k=5))
    return f"{province}{city}{first}{rest}"


def generate_new_energy_large():
    """新能源大型车（绿牌）- 6位，最后1位是D或F"""
    province = random.choice(PROVINCES)
    city = random.choice(LETTERS_NO_IO)
    middle = ''.join(random.choices(CHARS_NO_IO, k=5))
    last = random.choice('DF')
    return f"{province}{city}{middle}{last}"


def generate_yellow_truck():
    """黄牌大型车 - 5位纯数字"""
    province = random.choice(PROVINCES)
    city = random.choice(LETTERS_NO_IO)
    suffix = ''.join(random.choices('0123456789', k=5))
    return f"{province}{city}{suffix}"


def generate_yellow_coach():
    """黄牌教练车 - 最后一位是"学"字"""
    province = random.choice(PROVINCES)
    city = random.choice(LETTERS_NO_IO)
    suffix = ''.join(random.choices(CHARS_NO_IO, k=4))
    return f"{province}{city}{suffix}学"


def generate_black_embassy():
    """黑牌外籍车 - 4位数字 + "使"或"领"字"""
    province = random.choice(PROVINCES)
    city = random.choice(LETTERS_NO_IO)
    suffix = ''.join(random.choices('0123456789', k=4))
    ending = random.choice(['使', '领'])
    return f"{province}{city}{suffix}{ending}"


def generate_white_military():
    """白牌军车"""
    military = random.choice(MILITARY_CODES)
    city = random.choice(LETTERS_NO_IO)
    suffix = ''.join(random.choices(CHARS_NO_IO, k=5))
    return f"{military}{city}{suffix}"


def generate_white_police():
    """白牌武警车"""
    province = random.choice(PROVINCES)
    suffix = ''.join(random.choices('0123456789', k=5))
    return f"WJ{province}{suffix}"


def generate_hk_macau():
    """港澳车牌"""
    region = random.choice(['港', '澳'])
    suffix = ''.join(random.choices('0123456789', k=4))
    return f"粤Z{region}{suffix}"


# ==================== 分隔符处理 ====================

def add_separator_variant(plate, sep):
    """为车牌添加分隔符变体"""
    if sep == '':
        return plate

    # 在第2位后插入分隔符（省份+城市代码 之后）
    # 特殊处理：武警车(WJ开头)、港澳车(粤Z开头)
    if plate.startswith('WJ'):
        # WJ京12345 -> WJ京-12345
        return plate[:3] + sep + plate[3:]
    elif plate.startswith('粤Z'):
        # 粤Z港1234 -> 粤Z港-1234
        return plate[:3] + sep + plate[3:]
    else:
        # 标准格式：京A12345 -> 京A-12345
        return plate[:2] + sep + plate[2:]


# ==================== 主生成器 ====================
def plates(num: int) -> list[str]:
    generators = [
        generate_standard,
        generate_new_energy_small,
        generate_new_energy_large,
        generate_yellow_truck,
        generate_yellow_coach,
        generate_black_embassy,
        generate_white_military,
        generate_white_police,
        generate_hk_macau,
    ]
    generator = random.choice(generators)
    sep = random.choice(SEPARATORS)
    samples = []

    for _ in range(num):
        plate = add_separator_variant(generator(), sep)
        samples.append(plate)

    return samples
