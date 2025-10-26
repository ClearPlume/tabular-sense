import random


class GenderVariantGenerator:
    def __init__(self):
        # 按类型分类基础值
        self.chinese = {
            'male': ['男', '男性', '先生'],
            'female': ['女', '女性', '女士']
        }

        self.pinyin = {
            'male': ['nan', 'nanxing', 'N'],
            'female': ['nv', 'nvxing', 'V']
        }

        self.english = {
            'male': ['male', 'Male', 'MALE', 'M', 'm', 'man', 'Man'],
            'female': ['female', 'Female', 'FEMALE', 'F', 'f', 'woman', 'Woman']
        }

        self.numeric = {
            'male': ['1', '01', '001'],
            'female': ['0', '00', '000']
        }

        self.symbol = {
            'male': ['♂'],
            'female': ['♀']
        }

        self.separators = ['', ' ', '/', '-', '_']
        self.paired_seps = [('(', ')'), ('[', ']'), ('{', '}')]

    def __call__(self):
        variants = []

        # 1. 单一类型（不组合）
        for type_dict in [self.chinese, self.pinyin, self.english, self.numeric, self.symbol]:
            for m, f in zip(type_dict['male'], type_dict['female']):
                variants.append([m, f])

        # 2. 跨类型组合
        type_pairs = [
            (self.chinese, self.english),  # 中+英
            (self.chinese, self.pinyin),  # 中+拼音
            (self.chinese, self.numeric),  # 中+数
            (self.english, self.numeric),  # 英+数
            (self.pinyin, self.numeric),  # 拼音+数
            (self.symbol, self.chinese),  # 符号+中
            (self.symbol, self.english),  # 符号+英
        ]

        for type1, type2 in type_pairs:
            # 简单分隔符组合
            for sep in self.separators:
                for m1, f1 in zip(type1['male'][:3], type1['female'][:3]):  # 只取前3个代表
                    for m2, f2 in zip(type2['male'][:3], type2['female'][:3]):
                        variants.append([f"{m1}{sep}{m2}", f"{f1}{sep}{f2}"])

            # 括号形式组合（主+注）
            for open_sep, close_sep in self.paired_seps:
                for m1, f1 in zip(type1['male'][:2], type1['female'][:2]):
                    for m2, f2 in zip(type2['male'][:2], type2['female'][:2]):
                        variants.append([f"{m1}{open_sep}{m2}{close_sep}",
                                         f"{f1}{open_sep}{f2}{close_sep}"])

        return variants


def genders(num: int) -> list[str]:
    variant = random.choice(GenderVariantGenerator()())
    return [random.choice(variant) for _ in range(num)]
