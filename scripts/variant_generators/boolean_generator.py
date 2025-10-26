import random

# Boolean的53种变体
BOOLEAN_DATA = [
    # 中文语义（15种）
    ['是', '否'],
    ['对', '错'],
    ['真', '假'],
    ['有', '无'],
    ['启用', '禁用'],
    ['开启', '关闭'],
    ['激活', '未激活'],
    ['通过', '不通过'],
    ['成功', '失败'],
    ['正常', '异常'],
    ['可用', '不可用'],
    ['允许', '禁止'],
    ['同意', '不同意'],
    ['接受', '拒绝'],
    ['可', '否'],

    # 英文大小写（20种）
    ['True', 'False'],
    ['true', 'false'],
    ['TRUE', 'FALSE'],
    ['Yes', 'No'],
    ['yes', 'no'],
    ['YES', 'NO'],
    ['Y', 'N'],
    ['y', 'n'],
    ['On', 'Off'],
    ['on', 'off'],
    ['ON', 'OFF'],
    ['Enable', 'Disable'],
    ['enable', 'disable'],
    ['enabled', 'disabled'],
    ['Active', 'Inactive'],
    ['active', 'inactive'],
    ['Valid', 'Invalid'],
    ['valid', 'invalid'],
    ['Pass', 'Fail'],
    ['pass', 'fail'],

    # 英文语义（10种）
    ['Success', 'Failure'],
    ['OK', 'NG'],
    ['Accept', 'Reject'],
    ['Approved', 'Rejected'],
    ['Allowed', 'Denied'],
    ['Granted', 'Refused'],
    ['Confirmed', 'Cancelled'],
    ['Available', 'Unavailable'],
    ['Present', 'Absent'],
    ['Open', 'Closed'],

    # 数字/符号（5种）
    ['1', '0'],
    ['T', 'F'],
    ['t', 'f'],
    ['✓', '✗'],
    ['√', '×'],

    # 拼音/缩写（3种）
    ['shi', 'fou'],
    ['dui', 'cuo'],
    ['S', 'F'],
]


def booleans(num: int) -> list[str]:
    variant = random.choice(BOOLEAN_DATA)
    return [random.choice(variant) for _ in range(num)]
