from dataclasses import dataclass
from typing import Callable, List, TypeVarTuple, overload


# ============ 第一层：单元素验证器（纯粹的判断） ============
def is_numeric(s: str) -> bool:
    """单个字符串是否可解析为数字"""
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_int(s: str) -> bool:
    """单个字符串是否是整数"""
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s: str) -> bool:
    """单个字符串是否是小数（带小数点）"""
    return is_numeric(s) and not is_int(s)


def is_in_range[T: float](s: str, min_value: T, max_value: T) -> bool:
    """单个值是否在范围中"""
    return is_numeric(s) and min_value <= float(s) <= max_value


def is_binary(s: str) -> bool:
    """单个值是否是0或1"""
    return s in ('0', '1')


# ============ 第二层：通用组合器（框架） ============
T = TypeVarTuple("T")


@overload
def all_satisfy(validator: Callable[[str], bool]) -> Callable[[List[str]], bool]:    ...


@overload
def all_satisfy(validator: Callable[[str, *T], bool], *args: *T) -> Callable[[List[str]], bool]:    ...


def all_satisfy(validator: Callable[..., bool], *args: *T) -> Callable[[List[str]], bool]:
    """
    将单元素验证器提升为全集验证器
    
    这是一个高阶函数：
    - 输入：单元素验证器 (str -> bool)
    - 输出：全集验证器 (List[str] -> bool)
    """

    def check_all(data: List[str]) -> bool:
        return all(validator(s, *args) for s in data)

    return check_all


# ============ 第三层：规则定义 ============
@dataclass
class TypeRule:
    name: str
    validator: Callable[[List[str]], bool]


TYPE_RULES = [
    TypeRule("AGE", all_satisfy(is_in_range, 1, 120)),
    TypeRule("AMOUNT", all_satisfy(is_numeric)),
    TypeRule("BOOLEAN", all_satisfy(is_binary)),
    TypeRule("EDUCATION", all_satisfy(is_in_range, 1, 13)),
    TypeRule("ETHNICITY", all_satisfy(is_in_range, 1, 56)),
    TypeRule("GENDER", all_satisfy(is_binary)),
    TypeRule("FLOAT", all_satisfy(is_float)),
    TypeRule("INT", all_satisfy(is_int)),
    TypeRule("PERCENT", all_satisfy(is_in_range, -50.0, 500.0)),
    TypeRule("PRIORITY", all_satisfy(is_in_range, 0, 5)),
    TypeRule("STATE", all_satisfy(is_in_range, -1, 6)),
]


# ============ 第四层：执行器 ============
def infer_possible_types(data: List[str]) -> List[str]:
    """推断数据的所有可能类型"""
    possible_types = []

    for rule in TYPE_RULES:
        if rule.validator(data):
            possible_types.append(rule.name)

    return possible_types
