from enum import Enum
from random import Random
from typing import Optional


class PhoneFormat(Enum):
    """手机号格式"""

    STANDARD = "{prefix}{middle}{suffix}"
    SPACE = "{prefix} {middle} {suffix}"
    DASH = "{prefix}-{middle}-{suffix}"
    COUNTRY = "+86{prefix}{middle}{suffix}"
    COUNTRY_SPACE = "+86 {prefix} {middle} {suffix}"
    BRACE = "({prefix}){middle}{suffix}"
    COUNTRY_DASH = "+86-{prefix}-{middle}-{suffix}"
    BRACE_SPACE = "({prefix}) {middle} {suffix}"
    TWO_PART = "{prefix} {suffix}"
    LONG_DISTANCE = "0{prefix}{middle}{suffix}"

    def format(self, prefix: str, middle: str, suffix: str) -> str:
        return self.value.format(prefix=prefix, middle=middle, suffix=suffix)


class PhoneGenerator:
    """手机号生成"""

    rng: Optional[Random] = None

    def __init__(self):
        if self.rng is None:
            self.rng = Random()

    def __call__(self, fmt: PhoneFormat) -> str:

        carrier = self._carrier_code()

        if fmt == PhoneFormat.TWO_PART:
            if self.rng.random() < 0.5:
                # 138 00001111
                prefix = f"1{carrier}{self._random_digit()}"
                middle = ""
                suffix = self._random_digits(8)
            else:
                # 1380 1111222
                prefix = f"1{carrier}{self._random_digits(2)}"
                middle = ""
                suffix = self._random_digits(7)
        else:
            prefix = f"1{carrier}{self._random_digit()}"
            middle = self._random_digits(4)
            suffix = self._random_digits(4)

        return fmt.format(prefix, middle, suffix)

    def _carrier_code(self) -> str:
        """运营商代码（第2位）"""
        return str(self.rng.choice([3, 4, 5, 6, 7, 8, 9]))

    def _random_digit(self) -> str:
        """单个随机数字"""
        return str(self.rng.randint(0, 9))

    def _random_digits(self, n: int) -> str:
        """n位随机数字"""
        return ''.join(self._random_digit() for _ in range(n))


def phones(num: int) -> list[str]:
    generator = PhoneGenerator()
    fmt = generator.rng.choice(list(PhoneFormat))
    samples = []

    for _ in range(num):
        samples.append(generator(fmt))

    return samples
