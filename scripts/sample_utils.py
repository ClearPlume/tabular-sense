from contextlib import contextmanager
from functools import lru_cache
from typing import Callable

from src.tabular_sense.path import get_data_dir


def corpus_constructor[S](name: str, num: int, supplier: Callable[[], S]) -> list[S]:
    """语料构建"""
    samples = []

    for i in range(num):
        samples.append(supplier())

        if i % 1000 == 0:
            print(f"Generated {i} samples for {name}")

    return samples


def corpus_saver(corpus_name: str, content: str):
    """语料保存"""
    samples_dir = get_data_dir() / "corpus"

    if not samples_dir.exists():
        samples_dir.mkdir(parents=True, exist_ok=True)

    with open(samples_dir / f"{corpus_name}.txt", "w", encoding="utf-8") as file:
        file.write(content)


@contextmanager
def load_corpus(type_name: str):
    """加载语料"""
    loader = lambda: (get_data_dir() / f"corpus/{type_name}.txt").read_text(encoding="utf-8").splitlines()
    data = loader()
    try:
        yield data
    finally:
        del data


@lru_cache(maxsize=None)
def load_seed_type(type_name: str) -> list[str]:
    seed_dir = get_data_dir() / "seed"
    return (seed_dir / f"{type_name}.txt").read_text(encoding="utf-8").splitlines()
