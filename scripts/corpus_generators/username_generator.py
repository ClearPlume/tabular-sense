import random

from faker import Faker

from scripts.sample_utils import corpus_constructor, corpus_saver


def generate_username() -> str:
    if random.random() > 0.5:
        faker = Faker("zh")
    else:
        faker = Faker("en")

    return faker.user_name()


def usernames(num: int):
    samples = corpus_constructor("username", num, generate_username)
    corpus_saver("username", "\n".join(samples))
