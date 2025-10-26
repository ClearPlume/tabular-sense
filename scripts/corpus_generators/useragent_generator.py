import random

from faker import Faker

from scripts.sample_utils import corpus_constructor, corpus_saver


def generate_useragent() -> str:
    if random.random() > 0.5:
        faker = Faker("zh")
    else:
        faker = Faker("en")

    return faker.user_agent()


def useragent(num: int):
    samples = corpus_constructor("useragent", num, generate_useragent)
    corpus_saver("useragent", "\n".join(samples))
