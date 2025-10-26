from random import Random


def calculate_id_card_checksum(id_17: str) -> str:
    """
    计算18位身份证的校验码
    id_17: 前17位字符串
    """
    # 加权因子
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

    # 校验码映射
    checksum_map = ['1', '0', ['X', 'x'], '9', '8', '7', '6', '5', '4', '3', '2']

    # 计算加权和
    total = sum(int(id_17[i]) * weights[i] for i in range(17))

    # 模11取余，映射到校验码
    checksum = total % 11
    if checksum == 2:
        return Random().choice(checksum_map[checksum])
    else:
        return checksum_map[checksum]
