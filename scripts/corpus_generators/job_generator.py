import random

from faker import Faker

from scripts.sample_utils import corpus_constructor, corpus_saver


def generate_job() -> str:
    if random.random() > 0.5:
        faker = Faker("zh")
    else:
        faker = Faker("en")

    return faker.job()


def jobs(num: int):
    samples = corpus_constructor("job", num, generate_job)
    corpus_saver("job", "\n".join(samples))
