import random


class EducationVariantGenerator:
    """学历变体生成器：20种粒度 × 11种表示方式"""

    # 维度1：粒度定义（20种）
    GRANULARITIES = {
        'ultra_fine_12': ['学前', '小学', '初中', '职业初中', '普通高中', '职业高中', '中专', '技校', '大专', '本科',
                          '硕士', '博士', '博士后'],
        'fine_9': ['小学', '初中', '高中', '中专', '大专', '本科', '硕士', '博士', '博士后'],
        'medium_7a': ['小学', '初中', '高中', '中专', '专科', '本科', '研究生'],
        'medium_7b': ['小学', '初中', '职高/中专', '普高', '专科', '本科', '研究生'],
        'medium_6a': ['初中及以下', '高中', '中专', '大专', '本科', '研究生'],
        'medium_6b': ['小学', '初中', '高中/中专', '专科', '本科', '研究生'],
        'coarse_5a': ['初中及以下', '高中/中专', '大专', '本科', '研究生'],
        'coarse_5b': ['小学', '初中', '高中/中专', '本科', '研究生'],
        'coarse_4a': ['高中及以下', '大专', '本科', '研究生'],
        'coarse_4b': ['初中及以下', '高中/中专', '本科', '研究生'],
        'coarse_4c': ['高中及以下', '专科', '本科', '硕士及以上'],
        'ultra_coarse_3a': ['高中及以下', '本科', '研究生'],
        'ultra_coarse_3b': ['高中及以下', '大专/本科', '研究生'],
        'ultra_coarse_3c': ['专科及以下', '本科', '硕士及以上'],
        'binary_2a': ['本科以下', '本科及以上'],
        'binary_2b': ['大专及以下', '本科及以上'],
        'degree_3': ['学士', '硕士', '博士'],
        'degree_4': ['无学位', '学士', '硕士', '博士'],
        'stage_2': ['基础教育', '高等教育'],
        'stage_3': ['基础教育', '职业教育', '高等教育'],
    }

    # 维度2：表示方式映射（11种）
    REPRESENTATIONS = {
        'cn_full': {  # 中文全称
            '学前': '学前教育', '小学': '小学', '初中': '初级中学', '职业初中': '职业初级中学',
            '普通高中': '普通高级中学', '职业高中': '职业高级中学', '高中': '高级中学',
            '中专': '中等专业学校', '技校': '技工学校', '大专': '专科', '专科': '专科',
            '本科': '本科', '硕士': '硕士研究生', '博士': '博士研究生', '博士后': '博士后',
            '研究生': '研究生', '高中/中专': '高中/中专', '职高/中专': '职高/中专',
            '初中及以下': '初中及以下', '高中及以下': '高中及以下', '大专/本科': '大专/本科',
            '专科及以下': '专科及以下', '硕士及以上': '硕士及以上', '本科以下': '本科以下',
            '本科及以上': '本科及以上', '大专及以下': '大专及以下', '学士': '学士学位',
            '无学位': '无学位', '基础教育': '基础教育', '职业教育': '职业教育', '高等教育': '高等教育',
            '普高': '普通高中',
        },

        'cn_short': {  # 中文简称（保持原样）
            # 直接使用原始值
        },

        'en_full': {  # 英文全称
            '学前': 'Preschool Education', '小学': 'Elementary School', '初中': 'Middle School',
            '职业初中': 'Vocational Middle School', '普通高中': 'Regular High School',
            '职业高中': 'Vocational High School', '高中': 'High School',
            '中专': 'Technical Secondary School', '技校': 'Technical School',
            '大专': 'Associate Degree', '专科': 'Associate Degree', '本科': "Bachelor's Degree",
            '硕士': "Master's Degree", '博士': 'Doctoral Degree', '博士后': 'Postdoctoral',
            '研究生': 'Graduate', '高中/中专': 'High School/Technical',
            '职高/中专': 'Vocational/Technical', '初中及以下': 'Middle School or Below',
            '高中及以下': 'High School or Below', '大专/本科': 'Associate/Bachelor',
            '专科及以下': 'Associate or Below', '硕士及以上': 'Master or Above',
            '本科以下': 'Below Bachelor', '本科及以上': 'Bachelor or Above',
            '大专及以下': 'Associate or Below', '学士': "Bachelor's Degree",
            '无学位': 'No Degree', '基础教育': 'Basic Education',
            '职业教育': 'Vocational Education', '高等教育': 'Higher Education',
            '普高': 'Regular High School',
        },

        'en_short': {  # 英文简化
            '学前': 'Preschool', '小学': 'Elementary', '初中': 'Middle', '职业初中': 'Vocational Middle',
            '普通高中': 'Regular High', '职业高中': 'Vocational High', '高中': 'High',
            '中专': 'Technical Secondary', '技校': 'Technical', '大专': 'Associate', '专科': 'Associate',
            '本科': 'Bachelor', '硕士': 'Master', '博士': 'Doctor', '博士后': 'Postdoc',
            '研究生': 'Graduate', '高中/中专': 'High/Tech', '职高/中专': 'Voc/Tech',
            '初中及以下': 'Middle-', '高中及以下': 'High-', '大专/本科': 'Assoc/Bach',
            '专科及以下': 'Assoc-', '硕士及以上': 'Master+', '本科以下': 'Bach-',
            '本科及以上': 'Bach+', '大专及以下': 'Assoc-', '学士': 'Bachelor',
            '无学位': 'None', '基础教育': 'Basic', '职业教育': 'Vocational',
            '高等教育': 'Higher', '普高': 'Regular High',
        },

        'en_abbr': {  # 英文缩写
            '学前': 'PS', '小学': 'ES', '初中': 'MS', '职业初中': 'VMS',
            '普通高中': 'RHS', '职业高中': 'VHS', '高中': 'HS',
            '中专': 'TS', '技校': 'TS', '大专': 'AD', '专科': 'AD',
            '本科': 'BA', '硕士': 'MA', '博士': 'PhD', '博士后': 'PD',
            '研究生': 'GR', '高中/中专': 'HS/TS', '职高/中专': 'VHS/TS',
            '初中及以下': 'MS-', '高中及以下': 'HS-', '大专/本科': 'AD/BA',
            '专科及以下': 'AD-', '硕士及以上': 'MA+', '本科以下': 'BA-',
            '本科及以上': 'BA+', '大专及以下': 'AD-', '学士': 'BS',
            '无学位': 'ND', '基础教育': 'BE', '职业教育': 'VE',
            '高等教育': 'HE', '普高': 'RHS',
        },

        'en_abbr_alt': {  # 英文缩写变体
            '小学': 'ELEM', '初中': 'MID', '高中': 'HIGH',
            '大专': 'ASSOC', '专科': 'ASSOC', '本科': 'BS', '硕士': 'MS',
            '博士': 'Dr.', '博士后': 'PostDoc', '研究生': 'GRAD',
            '学士': 'BSc', '无学位': 'N/A',
        },

        'pinyin_full': {  # 拼音全拼
            '学前': 'xueqian', '小学': 'xiaoxue', '初中': 'chuzhong', '职业初中': 'zhiyechuzhong',
            '普通高中': 'putonggaozhong', '职业高中': 'zhiyegaozhong', '高中': 'gaozhong',
            '中专': 'zhongzhuan', '技校': 'jixiao', '大专': 'dazhuan', '专科': 'zhuanke',
            '本科': 'benke', '硕士': 'shuoshi', '博士': 'boshi', '博士后': 'boshihou',
            '研究生': 'yanjiusheng', '高中/中专': 'gaozhong/zhongzhuan',
            '职高/中专': 'zhigao/zhongzhuan', '初中及以下': 'chuzhongjiyixia',
            '高中及以下': 'gaozhongjiyixia', '大专/本科': 'dazhuan/benke',
            '专科及以下': 'zhuankejiyixia', '硕士及以上': 'shuoshijiyishang',
            '本科以下': 'benkeyixia', '本科及以上': 'benkejiyishang',
            '大专及以下': 'dazhuanjiyixia', '学士': 'xueshi', '无学位': 'wuxuewei',
            '基础教育': 'jichujiaoyu', '职业教育': 'zhiyejiaoyu',
            '高等教育': 'gaodengjiaoyu', '普高': 'pugao',
        },

        'pinyin_abbr': {  # 拼音简写
            '学前': 'xq', '小学': 'xx', '初中': 'cz', '职业初中': 'zycz',
            '普通高中': 'ptgz', '职业高中': 'zygz', '高中': 'gz',
            '中专': 'zz', '技校': 'jx', '大专': 'dz', '专科': 'zk',
            '本科': 'bk', '硕士': 'ss', '博士': 'bs', '博士后': 'bsh',
            '研究生': 'yjs', '高中/中专': 'gz/zz', '职高/中专': 'zg/zz',
            '初中及以下': 'czjyx', '高中及以下': 'gzjyx', '大专/本科': 'dz/bk',
            '专科及以下': 'zkjyx', '硕士及以上': 'ssjys', '本科以下': 'bkyx',
            '本科及以上': 'bkjys', '大专及以下': 'dzjyx', '学士': 'xs',
            '无学位': 'wxw', '基础教育': 'jcjy', '职业教育': 'zyjy',
            '高等教育': 'gdjy', '普高': 'pg',
        },

        'number': {  # 数字编码（按等级递增）
            # 动态生成：根据列表长度分配1, 2, 3...
        },

        'roman': {  # 罗马数字
            # 动态生成：I, II, III, IV...
        },

        'level': {  # 等级符号
            # 动态生成：L1, L2, L3...
        },
    }

    def _apply_representation(self, values, rep_type):
        """应用表示方式转换"""
        if rep_type == 'cn_short':
            # 中文简称：保持原样
            return values

        elif rep_type in ['number', 'roman', 'level']:
            # 动态编码
            if rep_type == 'number':
                return [str(i + 1) for i in range(len(values))]
            elif rep_type == 'roman':
                roman_map = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII']
                return [roman_map[i] for i in range(len(values))]
            elif rep_type == 'level':
                return [f'L{i + 1}' for i in range(len(values))]

        else:
            # 使用映射表
            mapping = self.REPRESENTATIONS[rep_type]
            result = []
            for val in values:
                # 如果映射表中没有，保持原值
                result.append(mapping.get(val, val))
            return result

    def generate_all_variants(self):
        """生成所有20×11=220个变体组合"""
        variants = []

        for gran_name, gran_values in self.GRANULARITIES.items():
            for rep_name in self.REPRESENTATIONS.keys():
                converted_values = self._apply_representation(gran_values, rep_name)

                variants.append({
                    'granularity': gran_name,
                    'representation': rep_name,
                    'values': converted_values,
                    'variant_id': f"{gran_name}_{rep_name}",
                    'size': len(converted_values),
                })

        return variants


# 使用示例
def educations(num: int) -> list[str]:
    generator = EducationVariantGenerator()

    # 生成所有变体
    variants = generator.generate_all_variants()
    variant = random.choice(variants)["values"]

    return [random.choice(variant) for _ in range(num)]
