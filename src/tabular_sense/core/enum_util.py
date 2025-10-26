from enum import IntEnum

from src.tabular_sense.core.constants import ALL_TYPES

# TODO 为ALL_TYPES和ColumnType的一致性新增单测
ColumnType = IntEnum("ColumnType", {name.upper(): idx for idx, name in enumerate(ALL_TYPES)})


# noinspection PyTypeHints
# 莫名其妙的警告
def to_multiple_label(*types: ColumnType) -> list[int]:
    vector = [0] * len(ALL_TYPES)
    for t1 in types:
        vector[t1.value] = 1
    return vector


# noinspection PyTypeHints
# 莫名其妙的警告
def from_multiple_label(vector: list[int]) -> list[ColumnType]:
    return [ColumnType(i) for i, v in enumerate(vector) if v == 1]


ColumnType.to_multiple_label = to_multiple_label
ColumnType.from_multiple_label = from_multiple_label

if __name__ == '__main__':
    for t in ColumnType:
        print(f"\t\t{t.name} = {t.value}")
