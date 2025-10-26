import random

from scripts.sample_utils import load_seed_type


def recreations(num: int) -> list[str]:
    return random.sample(load_seed_type("recreation"), num)
