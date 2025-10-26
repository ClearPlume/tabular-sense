import random
from typing import Callable

AGR_VARIANTS: list[Callable[[int], str]] = [
    lambda age: str(age),
    lambda age: f"{age}岁",
    lambda age: f"{age} 岁",
    lambda age: f"{age}周岁",
    lambda age: f"{age} 周岁",
    lambda age: f"{age} years old",
    lambda age: f"{age}yo",
    lambda age: f"{age}Y",
    lambda age: f"age: {age}",
    lambda age: f"age:{age}",
    lambda age: f"{age} yrs",
    lambda age: f"年龄: {age}",
    lambda age: f"年龄:{age}",
]


def ages(num: int) -> list[str]:
    variant: Callable[[int], str] = random.choice(AGR_VARIANTS)
    samples = []
    for _ in range(num):
        age = random.randint(1, 120)
        samples.append(variant(age))
    return samples
