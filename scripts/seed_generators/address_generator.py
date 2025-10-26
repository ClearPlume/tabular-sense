import random

from scripts.sample_utils import load_seed_type


def addresses(num: int) -> list[str]:
    return random.sample(load_seed_type("address"), num)
