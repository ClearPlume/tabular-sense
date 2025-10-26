import math
import random


class AmountGenerator:
    def __init__(self):
        # 基础货币符号
        self.currencies = [
            ('¥', ''), ('￥', ''),  # 半角/全角人民币
            ('$', ''),
            ('€', ''),
            ('£', ''),
            ('', '元'), ('', '元整'),
            ('', '美元'), ('', 'USD'), ('', 'CNY'), ('', 'RMB'),
            ('', ' 元'), ('', ' 美元'),  # 带空格
        ]

        # 千分位分隔符
        self.separators = [',', ' ', '_', '']

        # 中文数字
        self.cn_digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        self.cn_units = ['', '十', '百', '千', '万', '十', '百', '千', '亿']
        self.cn_upper = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']

        # 单位简写
        self.chinese_units = ['万', 'w', '千万', '亿']
        self.english_units = ['K', 'k', 'M', 'm', 'B', 'b']

    def generate(self):
        """主生成函数，随机选择一种变体类型"""
        variant_type = random.choices(
            [
                'standard',  # 标准格式 35%
                'with_unit',  # 带单位 15%
                'chinese_number',  # 中文数字 10%
                'range',  # 范围 5%
                'approximate',  # 约数 5%
                'messy',  # 容错变体 10%
                'extreme',  # 极端值 5%
                'number',  # 普通数字 10%
                'special',  # 特殊格式 5%
            ],
            weights=[40, 15, 10, 5, 5, 15, 5, 10, 5]
        )[0]

        method = getattr(self, f'_generate_{variant_type}')
        return method()

    def _random_amount(self, min_val=0, max_val=10000000):
        """生成随机金额基数"""
        return random.choice([
            random.randint(min_val, max_val),
            round(random.uniform(min_val, max_val), random.randint(1, 4)),
        ])

    def _generate_standard(self):
        """标准格式：符号 + 数字 + 单位"""
        amount = self._random_amount()
        currency_prefix, currency_suffix = random.choice(self.currencies)
        separator = random.choice(self.separators)
        decimal_places = random.choice([0, 1, 2, 3, 4])
        sign = random.choice(['', '+', '-', ''] * 3)  # 正号少见

        # 符号处理
        if sign == '-':
            amount = -abs(amount)
            # 10% 概率用会计记账法 (100)
            if random.random() < 0.1:
                return self._accounting_format(abs(amount), currency_prefix, currency_suffix, separator, decimal_places)

        # 格式化数字
        formatted = self._format_number(abs(amount), separator, decimal_places)

        # 符号位置：可能在货币符号前或后
        if sign and random.random() < 0.2:  # 20% 概率符号在货币符号后（错误但存在）
            return f"{currency_prefix}{sign}{formatted}{currency_suffix}"
        else:
            return f"{sign}{currency_prefix}{formatted}{currency_suffix}"

    def _generate_with_unit(self):
        """带单位：1.5万、10.5k"""
        amount = self._random_amount(1000, 1000000000)

        if random.random() < 0.5:
            # 中文单位
            return self._with_chinese_unit(amount)
        else:
            # 英文单位
            return self._with_english_unit(amount)

    def _generate_chinese_number(self):
        """中文数字"""
        amount = random.randint(0, 999999)

        variant = random.choice([
            'lowercase',  # 一百二十三元
            'uppercase',  # 壹佰贰拾叁元整
            'spoken',  # 三块五、一千五
        ])

        if variant == 'lowercase':
            return self._to_chinese_lower(amount) + random.choice(['元', '元整', '块'])
        elif variant == 'uppercase':
            return self._to_chinese_upper(amount) + '元整'
        else:  # spoken
            return self._to_chinese_spoken(amount)

    def _generate_range(self):
        """范围：100-200、¥50~150"""
        low = self._random_amount(10, 10000)
        high = low + self._random_amount(10, 5000)
        separator = random.choice(['-', '~', ' to ', '至'])
        currency = random.choice(['¥', '$', '€', '', ''])

        return f"{currency}{low}{separator}{high}" + random.choice(['', '元', 'USD'])

    def _generate_approximate(self):
        """约数：约¥100、~$50"""
        amount = self._random_amount()
        prefix = random.choice(['约', '~', '≈', 'around ', 'about ', '大约'])
        currency = random.choice(['¥', '$', '€'])

        return f"{prefix}{currency}{amount}"

    def _generate_messy(self):
        """容错变体：全角、多余空格、混用分隔符等"""
        base = self._generate_standard()

        mess_type = random.choice([
            'full_width',  # 全角
            'extra_space',  # 多余空格
            'duplicate_symbol',  # 重复符号
            'mixed_separator',  # 混用分隔符
            'redundant_unit',  # 冗余单位：¥100元RMB
            'html_entity',  # HTML实体
            'wrong_position',  # 符号位置错误
        ])

        if mess_type == 'full_width':
            return self._to_full_width(base)

        elif mess_type == 'extra_space':
            # 随机位置插入空格
            pos = random.randint(1, len(base) - 1)
            return base[:pos] + ' ' * random.randint(1, 3) + base[pos:]

        elif mess_type == 'duplicate_symbol':
            # 重复货币符号
            for symbol in ['¥', '$', '€', '£']:
                if symbol in base:
                    return base.replace(symbol, symbol * 2, 1)
            return base

        elif mess_type == 'mixed_separator':
            # 混用分隔符：1,234_567.89
            if ',' in base:
                parts = base.split(',')
                return parts[0] + ',' + parts[1].replace(',', '_') if len(parts) > 2 else base
            return base

        elif mess_type == 'redundant_unit':
            # ¥100元RMB
            if '¥' in base and '元' not in base:
                return base + random.choice(['元', 'RMB', 'CNY'])
            return base

        elif mess_type == 'html_entity':
            # &yen;100 或 &#165;100
            base = base.replace('¥', random.choice(['&yen;', '&#165;']))
            base = base.replace('$', random.choice(['&dollar;', '&#36;']))
            return base

        elif mess_type == 'wrong_position':
            # 符号在奇怪的地方：100-元
            if '元' in base and '-' not in base:
                return base.replace('元', '-元')
            return base

        return base

    def _generate_extreme(self):
        """极端值：0、负零、NaN、inf、极大值"""
        extreme_type = random.choice([
            'zero',
            'negative_zero',
            'tiny',
            'huge',
            'scientific',
        ])

        currency = random.choice(['¥', '$', '€', ''])

        if extreme_type == 'zero':
            decimal = random.choice([0, 2, 4])
            if decimal == 0:
                return f"{currency}0"
            return f"{currency}0.{'0' * decimal}"

        elif extreme_type == 'negative_zero':
            return f"{currency}-0.00"

        elif extreme_type == 'tiny':
            # 极小值
            return f"{currency}0.{'0' * random.randint(5, 10)}{random.randint(1, 9)}"

        elif extreme_type == 'huge':
            # 极大值
            return f"{currency}{random.randint(1, 9)}{'9' * random.randint(10, 15)}"

        elif extreme_type == 'scientific':
            # 科学计数法 + 货币
            base = random.uniform(1, 10)
            exp = random.randint(3, 8)
            return f"{currency}{base:.2f}e{exp}"

    def _generate_number(self):
        """普通数字"""
        log_min = math.log10(1)
        log_max = math.log10(10000000)
        amount = round(random.uniform(log_min, log_max) ** 10, 5)

        if random.random() > 0.5:
            return str(int(amount))
        else:
            return str(amount)

    def _generate_special(self):
        """特殊格式：单价、带说明、计算式"""
        amount = self._random_amount(10, 1000)
        currency = random.choice(['¥', '$'])

        special_type = random.choice([
            'unit_price',  # ¥100/人
            'with_note',  # ¥100(含税)
            'expression',  # $50*2
        ])

        if special_type == 'unit_price':
            unit = random.choice(['/人', '/件', '/天', '/月', '/kg', ' each', ' per item'])
            return f"{currency}{amount}{unit}"

        elif special_type == 'with_note':
            note = random.choice(['(含税)', '(不含税)', '(优惠价)', '(原价)', '(预付)'])
            return f"{currency}{amount}{note}"

        elif special_type == 'expression':
            op = random.choice(['*', 'x', 'X', '×'])
            multiplier = random.randint(2, 10)
            return f"{currency}{amount}{op}{multiplier}"

    # ========== 辅助函数 ==========

    def _format_number(self, amount, separator, decimal_places):
        """格式化数字：千分位 + 小数位"""
        if decimal_places == 0:
            integer_part = int(abs(amount))
        else:
            integer_part = int(abs(amount))
            decimal_part = abs(amount) - integer_part

        # 千分位
        if separator:
            formatted = f"{integer_part:,}".replace(',', separator)
        else:
            formatted = str(integer_part)

        # 小数
        if decimal_places > 0:
            decimal_str = f"{decimal_part:.{decimal_places}f}"[2:]  # 去掉 "0."
            formatted += f".{decimal_str}"

        return formatted

    def _accounting_format(self, amount, prefix, suffix, separator, decimal_places):
        """会计记账法：(100)表示负数"""
        formatted = self._format_number(amount, separator, decimal_places)
        return f"({prefix}{formatted}{suffix})"

    def _with_chinese_unit(self, amount):
        """中文单位：1.5万、10亿"""
        currency = random.choice(['¥', '$', ''])

        if amount >= 100000000:
            value = amount / 100000000
            unit = '亿'
        elif amount >= 10000:
            value = amount / 10000
            unit = random.choice(['万', 'w'])
        else:
            return f"{currency}{amount}"

        # 口语化："10个亿"、"3千万"
        if random.random() < 0.2:
            if unit == '亿':
                return f"{int(value)}个亿"
            elif unit == '万' and value >= 1000:
                return f"{int(value / 1000)}千万"

        decimal_places = random.choice([0, 1, 2])
        if decimal_places == 0:
            return f"{currency}{int(value)}{unit}"
        return f"{currency}{value:.{decimal_places}f}{unit}"

    def _with_english_unit(self, amount):
        """英文单位：1.5K、10.5M"""
        currency = random.choice(['$', '¥', '€', ''])

        if amount >= 1e9:
            value = amount / 1e9
            unit = random.choice(['B', 'b'])
        elif amount >= 1e6:
            value = amount / 1e6
            unit = random.choice(['M', 'm'])
        elif amount >= 1e3:
            value = amount / 1e3
            unit = random.choice(['K', 'k'])
        else:
            return f"{currency}{amount}"

        decimal_places = random.choice([0, 1, 2])
        if decimal_places == 0:
            return f"{currency}{int(value)}{unit}"
        return f"{currency}{value:.{decimal_places}f}{unit}"

    def _to_chinese_lower(self, amount):
        """转中文小写：一百二十三"""
        if amount == 0:
            return '零'

        result = []
        str_amount = str(int(amount))
        length = len(str_amount)

        for i, digit in enumerate(str_amount):
            d = int(digit)
            pos = length - i - 1

            if d != 0:
                result.append(self.cn_digits[d])
                if pos > 0:
                    result.append(self.cn_units[pos])
            elif result and result[-1] != '零':
                result.append('零')

        # 清理尾部零
        if result and result[-1] == '零':
            result.pop()

        return ''.join(result)

    def _to_chinese_upper(self, amount):
        """转中文大写：壹佰贰拾叁"""
        # 简化实现
        lower = self._to_chinese_lower(amount)
        for i, char in enumerate(self.cn_digits):
            lower = lower.replace(char, self.cn_upper[i])
        return lower

    def _to_chinese_spoken(self, amount):
        """口语化：三块五、一千五"""
        if amount < 10:
            return f"{self.cn_digits[int(amount)]}块"
        elif amount < 100:
            yuan = int(amount // 10)
            jiao = int(amount % 10)
            if jiao == 0:
                return f"{self.cn_digits[yuan]}十块"
            elif jiao == 5:
                return f"{self.cn_digits[yuan]}块五"
            return f"{self.cn_digits[yuan]}块{self.cn_digits[jiao]}"
        elif amount < 10000:
            if amount % 1000 == 0:
                return f"{self.cn_digits[int(amount // 1000)]}千块"
            elif amount % 500 == 0:
                qian = int(amount // 1000)
                if amount % 1000 == 500:
                    return f"{self.cn_digits[qian]}千五"
            return self._to_chinese_lower(amount) + '块'
        else:
            return self._to_chinese_lower(amount) + '元'

    def _to_full_width(self, text):
        """半角转全角"""
        result = []
        for char in text:
            code = ord(char)
            if 33 <= code <= 126:  # ASCII可打印字符
                result.append(chr(code + 0xFEE0))
            elif char == ' ':
                result.append(chr(0x3000))
            else:
                result.append(char)
        return ''.join(result)


def amounts(num: int) -> list[str]:
    generator = AmountGenerator()
    variant_type = random.choices(
        [
            'standard',  # 标准格式 35%
            'with_unit',  # 带单位 15%
            'chinese_number',  # 中文数字 10%
            'range',  # 范围 5%
            'approximate',  # 约数 5%
            'messy',  # 容错变体 10%
            'extreme',  # 极端值 5%
            'number',  # 普通数字 10%
            'special',  # 特殊格式 5%
        ],
        weights=[40, 15, 10, 5, 5, 15, 5, 10, 5]
    )[0]
    method = getattr(generator, f'_generate_{variant_type}')
    return [method() for _ in range(num)]
