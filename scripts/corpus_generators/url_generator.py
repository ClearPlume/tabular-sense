import random
from urllib.parse import urlencode

from faker import Faker

from scripts.sample_utils import corpus_constructor, corpus_saver

faker = Faker("zh_CN")

# 协议分布
PROTOCOLS = [
    'http',
    'https',
    'ftp',
    'ws',
    'wss',
    'file',
    'git',
    'ssh',
    'mailto',
]


def generate_url():
    protocol = random.choice(PROTOCOLS)

    # 特殊协议
    if protocol == 'mailto':
        return f"mailto:{faker.email()}"
    if protocol == 'file':
        return f"file:///{faker.file_path()}"
    if protocol == 'tel':
        return f"tel:+86{random.randint(13000000000, 19999999999)}"

    # 标准URL结构
    parts = [f"{protocol}://"]

    # 2. 可选：用户名密码（5%概率）
    if random.random() < 0.05:
        username = faker.user_name()
        password = faker.password(length=8, special_chars=False)
        parts.append(f"{username}:{password}@")

    # 3. Host
    host = faker.domain_name()
    parts.append(host)

    # 4. 可选：端口（10%概率）
    if random.random() < 0.10:
        ports = [80, 443, 8080, 8000, 3000, 5000, 8888]
        parts.append(f":{random.choice(ports)}")

    # 5. 可选：路径（70%概率）
    if random.random() < 0.70:
        path = generate_uri_path()
        parts.append(path)

    # 6. 可选：查询参数（30%概率）
    if random.random() < 0.30:
        query = generate_query_params()
        parts.append(f"?{query}")

    # 7. 可选：Fragment（10%概率）
    if random.random() < 0.10:
        fragment = random.choice([
            'section', 'top', 'content', 'footer',
            'comment-123', 'L42', 'user-profile'
        ])
        parts.append(f"#{fragment}")

    return ''.join(parts)


def generate_uri_path():
    """生成URI路径"""
    styles = [
        'simple',  # /about
        'nested',  # /user/profile/settings
        'restful',  # /api/v1/users/123
        'file',  # /images/photo.jpg
        'localized',  # /zh-CN/docs/guide
    ]

    style = random.choice(styles)

    if style == 'simple':
        segments = random.choice([
            ['about'], ['contact'], ['help'], ['faq'],
            ['docs'], ['blog'], ['products'], ['services']
        ])

    elif style == 'nested':
        depth = random.randint(2, 4)
        segments = [faker.word() for _ in range(depth)]

    elif style == 'restful':
        resource = random.choice(['users', 'posts', 'products', 'orders', 'comments'])
        id_val = random.randint(1, 99999)
        segments = ['api', random.choice(['v1', 'v2']), resource, str(id_val)]

        # 可能有子资源
        if random.random() < 0.3:
            sub = random.choice(['comments', 'likes', 'followers', 'settings'])
            segments.append(sub)

    elif style == 'file':
        filename = faker.file_name()
        folder = random.choice(['images', 'documents', 'downloads', 'static', 'assets'])
        segments = [folder, filename]

    elif style == 'localized':
        lang = random.choice(['zh-CN', 'en-US', 'ja-JP', 'ko-KR'])
        segments = [lang, faker.word(), faker.word()]

    return '/' + '/'.join(segments)


def generate_query_params():
    """生成查询参数"""
    num_params = random.randint(1, 4)

    param_templates = [
        # 搜索类
        ('q', lambda: faker.word()),
        ('search', lambda: '+'.join(faker.words(2))),
        ('keyword', lambda: faker.word()),

        # 分页类
        ('page', lambda: str(random.randint(1, 100))),
        ('limit', lambda: str(random.choice([10, 20, 50, 100]))),
        ('offset', lambda: str(random.randint(0, 1000))),

        # 过滤类
        ('category', lambda: random.choice(['tech', 'news', 'sports', 'entertainment'])),
        ('status', lambda: random.choice(['active', 'pending', 'completed'])),
        ('sort', lambda: random.choice(['date', 'price', 'name', 'popularity'])),
        ('order', lambda: random.choice(['asc', 'desc'])),

        # 跟踪类
        ('utm_source', lambda: random.choice(['google', 'facebook', 'twitter'])),
        ('utm_medium', lambda: random.choice(['cpc', 'email', 'social'])),
        ('ref', lambda: faker.uuid4()[:8]),

        # 其他
        ('id', lambda: str(random.randint(1, 99999))),
        ('token', lambda: faker.uuid4()[:16]),
        ('timestamp', lambda: str(random.randint(1600000000, 1700000000))),
    ]

    selected = random.sample(param_templates, min(num_params, len(param_templates)))
    params = {key: value_func() for key, value_func in selected}

    return urlencode(params)


def urls(num: int):
    samples = corpus_constructor("url", num, generate_url)
    corpus_saver("url", "\n".join(samples))
