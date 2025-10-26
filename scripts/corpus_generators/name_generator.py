from random import Random

from faker import Faker

from scripts.sample_utils import corpus_saver
from src.tabular_sense.path import get_data_dir

# 姓名生成时，复姓占比
COMPOUND_RADIO = 0.05

# 复姓列表
COMPOUND_SURNAMES = ['东方', '公冶', '太叔', '慕容', '子车', '司空', '公西', '百里', '拓跋', '诸葛', '皇甫', '轩辕',
                     '长孙', '西门', '壤驷', '巫马', '司寇', '东郭', '司马', '闻人', '第五', '宗政', '呼延', '羊舌',
                     '微生', '上官', '赫连', '段干', '商弥', '鲜卑', '东野', '公良', '端木', '左丘', '澹台', '夏侯',
                     '公羊', '司徒', '欧阳', '申屠', '梁丘', '单于', '夹谷', '尉迟', '南宫', '颛孙', '仲孙', '淳于',
                     '令狐', '东门', '独孤', '钟离', '公孙', '闾丘', '谷梁', '乐正', '宇文', '濮阳', '宰父', '鲜于',
                     '漆雕', '南门']


def names(num: int):
    data_dir = get_data_dir()
    en_radio = 0.1

    rng = Random()
    faker_zh = Faker("zh_CN")
    faker_en = Faker("en_US")

    # 初始填充复姓
    samples: list[str] = [*(data_dir / "seed/compound_names.txt").open(encoding="utf-8").read().splitlines()]
    compound_name_num = len(samples)
    # 期望中文姓名数量
    prefer_zh_name_num = num * (1 - en_radio)
    # 对于每个新的姓名，需要转换为复姓的几率
    convert_compound_radio = (prefer_zh_name_num * COMPOUND_RADIO - compound_name_num) / prefer_zh_name_num

    print(f"目标配置:")
    print(f"  总数: {num}")
    print(f"  英文比例: {en_radio * 100}%")
    print(f"  复姓比例（中文名中）: {COMPOUND_RADIO * 100}%")
    print(f"  初始复姓: {compound_name_num}")
    print(f"  转换比例: {convert_compound_radio * 100:.2f}%")
    print()

    en_count = 0
    zh_count = 0
    zh_single_count = 0
    zh_compound_count = compound_name_num

    for i in range(num - compound_name_num):
        if rng.random() < en_radio:
            en_count += 1
            samples.append(faker_en.name())
        else:
            zh_count += 1
            if rng.random() < convert_compound_radio:
                zh_compound_count += 1
                surname = rng.choice(COMPOUND_SURNAMES)
                given_name = faker_zh.name()[1:]
                samples.append(surname + given_name)
            else:
                zh_single_count += 1
                samples.append(faker_zh.name())

        if i % 1000 == 0:
            print(f"Generated {i} samples for name")

    print(f"实际生成:")
    print(f"  总数: {len(samples)}")
    print(f"  英文: {en_count} ({en_count / len(samples) * 100:.2f}%)")
    print(f"  中文: {zh_count} ({zh_count / len(samples) * 100:.2f}%)")
    print(f"  复姓: {zh_compound_count} ({zh_compound_count / zh_count * 100:.2f}% of 中文)")
    print(f"  期望复姓比例: {COMPOUND_RADIO * 100}%")
    rng.shuffle(samples)

    corpus_saver("name", "\n".join(samples))
