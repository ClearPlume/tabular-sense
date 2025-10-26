import random

# 56个民族的6种变体
ETHNICITY_DATA = [
    # (数字编码, 中文全称, 中文简称, 拼音全称, 字母代码, 英文全称)
    ('01', '汉族', '汉', 'Han', 'HA', 'Han'),
    ('02', '蒙古族', '蒙古', 'Mongol', 'MG', 'Mongolian'),
    ('03', '回族', '回', 'Hui', 'HU', 'Hui'),
    ('04', '藏族', '藏', 'Zang', 'ZA', 'Tibetan'),
    ('05', '维吾尔族', '维吾尔', 'Uygur', 'UG', 'Uygur'),
    ('06', '苗族', '苗', 'Miao', 'MH', 'Miao'),
    ('07', '彝族', '彝', 'Yi', 'YI', 'Yi'),
    ('08', '壮族', '壮', 'Zhuang', 'ZH', 'Zhuang'),
    ('09', '布依族', '布依', 'Buyei', 'BY', 'Bouyei'),
    ('10', '朝鲜族', '朝鲜', 'Chosen', 'CS', 'Korean'),
    ('11', '满族', '满', 'Man', 'MA', 'Manchu'),
    ('12', '侗族', '侗', 'Dong', 'DO', 'Dong'),
    ('13', '瑶族', '瑶', 'Yao', 'YA', 'Yao'),
    ('14', '白族', '白', 'Bai', 'BA', 'Bai'),
    ('15', '土家族', '土家', 'Tujia', 'TJ', 'Tujia'),
    ('16', '哈尼族', '哈尼', 'Hani', 'HN', 'Hani'),
    ('17', '哈萨克族', '哈萨克', 'Kazak', 'KZ', 'Kazak'),
    ('18', '傣族', '傣', 'Dai', 'DA', 'Dai'),
    ('19', '黎族', '黎', 'Li', 'LI', 'Li'),
    ('20', '傈僳族', '傈僳', 'Lisu', 'LS', 'Lisu'),
    ('21', '佤族', '佤', 'Va', 'VA', 'Va'),
    ('22', '畲族', '畲', 'She', 'SH', 'She'),
    ('23', '高山族', '高山', 'Gaoshan', 'GS', 'Gaoshan'),
    ('24', '拉祜族', '拉祜', 'Lahu', 'LH', 'Lahu'),
    ('25', '水族', '水', 'Sui', 'SU', 'Sui'),
    ('26', '东乡族', '东乡', 'Dongxiang', 'DX', 'Dongxiang'),
    ('27', '纳西族', '纳西', 'Naxi', 'NX', 'Naxi'),
    ('28', '景颇族', '景颇', 'Jingpo', 'JP', 'Jingpo'),
    ('29', '柯尔克孜族', '柯尔克孜', 'Kirgiz', 'KG', 'Kyrgyz'),
    ('30', '土族', '土', 'Tu', 'TU', 'Tu'),
    ('31', '达斡尔族', '达斡尔', 'Daur', 'DU', 'Daur'),
    ('32', '仫佬族', '仫佬', 'Mulao', 'ML', 'Mulam'),
    ('33', '羌族', '羌', 'Qiang', 'QI', 'Qiang'),
    ('34', '布朗族', '布朗', 'Blang', 'BL', 'Blang'),
    ('35', '撒拉族', '撒拉', 'Salar', 'SL', 'Salar'),
    ('36', '毛南族', '毛南', 'Maonan', 'MN', 'Maonan'),
    ('37', '仡佬族', '仡佬', 'Gelao', 'GL', 'Gelao'),
    ('38', '锡伯族', '锡伯', 'Xibe', 'XB', 'Xibe'),
    ('39', '阿昌族', '阿昌', 'Achang', 'AC', 'Achang'),
    ('40', '普米族', '普米', 'Pumi', 'PM', 'Pumi'),
    ('41', '塔吉克族', '塔吉克', 'Tajik', 'TA', 'Tajik'),
    ('42', '怒族', '怒', 'Nu', 'NU', 'Nu'),
    ('43', '乌孜别克族', '乌孜别克', 'Uzbek', 'UZ', 'Uzbek'),
    ('44', '俄罗斯族', '俄罗斯', 'Russ', 'RS', 'Russian'),
    ('45', '鄂温克族', '鄂温克', 'Ewenki', 'EW', 'Evenki'),
    ('46', '德昂族', '德昂', 'Deang', 'DE', 'Deang'),
    ('47', '保安族', '保安', 'Bonan', 'BN', 'Bonan'),
    ('48', '裕固族', '裕固', 'Yugur', 'YG', 'Yugur'),
    ('49', '京族', '京', 'Gin', 'GI', 'Gin'),
    ('50', '塔塔尔族', '塔塔尔', 'Tatar', 'TT', 'Tatar'),
    ('51', '独龙族', '独龙', 'Derung', 'DR', 'Derung'),
    ('52', '鄂伦春族', '鄂伦春', 'Oroqen', 'OR', 'Oroqen'),
    ('53', '赫哲族', '赫哲', 'Hezhen', 'HZ', 'Hezhe'),
    ('54', '门巴族', '门巴', 'Monba', 'MB', 'Monba'),
    ('55', '珞巴族', '珞巴', 'Lhoba', 'LB', 'Lhoba'),
    ('56', '基诺族', '基诺', 'Jino', 'JN', 'Jino'),
]

# 生成变体
ETHNICITY_VARIANTS = [
    [row[1] for row in ETHNICITY_DATA],  # 中文全称
    [row[2] for row in ETHNICITY_DATA],  # 中文简称
    [row[0] for row in ETHNICITY_DATA],  # 数字编码
    [row[3] for row in ETHNICITY_DATA],  # 拼音全称
    [row[4] for row in ETHNICITY_DATA],  # 字母代码
    [row[5] for row in ETHNICITY_DATA],  # 英文全称
]


def ethnicities(num: int) -> list[str]:
    variant = random.choice(ETHNICITY_VARIANTS)
    return [random.choice(variant) for _ in range(num)]
