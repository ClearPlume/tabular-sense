from random import Random

from faker import Faker

from scripts.sample_utils import corpus_saver, corpus_constructor

faker = Faker("zh_CN")
rng = Random()

EMAIL_DOMAINS = [
    'qq.com',
    'vip.qq.com',
    'foxmail.com',
    '163.com',
    '126.com',
    'yeah.net',
    '188.com',
    'sina.com',
    'sina.cn',
    'sohu.com',
    'aliyun.com',
    '139.com',
    '189.cn',
    'tom.com',
    '21cn.com',
    'wo.cn',
    'sogou.com',
    'gmail.com',
    'outlook.com',
    'hotmail.com',
    'live.com',
    'yahoo.com',
    'yahoo.co.jp',
    'icloud.com',
    'me.com',
    'mac.com',
    'aol.com',
    'mail.com',
    'protonmail.com',
    'yandex.com',
    'gmx.com',
    'zoho.com',
    'company.com',
    'corp.com',
    'enterprise.cn',
    'edu.cn',
    'university.edu.cn',
    'student.edu.cn',
    'tempmail.com',
    'guerrillamail.com',
    '10minutemail.com',
]


def emails(num: int):
    samples = corpus_constructor("email", num, lambda: f"{faker.user_name()}@{rng.choice(EMAIL_DOMAINS)}")
    corpus_saver("email", "\n".join(samples))
