# 优先级变体
import random

PRIORITY_VARIANTS = [
    # === 中文系列 ===
    # 3级
    ['高', '中', '低'],
    ['重要', '一般', '不重要'],
    ['优先', '普通', '延后'],

    # 4级
    ['紧急', '高', '中', '低'],
    ['非常重要', '重要', '一般', '不重要'],
    ['立即处理', '优先', '普通', '延后'],

    # 5级
    ['非常紧急', '紧急', '高', '中', '低'],
    ['最高', '高', '中', '低', '最低'],
    ['立即', '紧急', '优先', '普通', '延后'],

    # === 英文系列（首字母大写）===
    # 3级
    ['High', 'Medium', 'Low'],
    ['Important', 'Normal', 'Minor'],
    ['Urgent', 'Normal', 'Low'],

    # 4级
    ['Critical', 'High', 'Medium', 'Low'],
    ['Urgent', 'High', 'Normal', 'Low'],
    ['Highest', 'High', 'Medium', 'Low'],

    # 5级
    ['Critical', 'Urgent', 'High', 'Medium', 'Low'],
    ['Blocker', 'Critical', 'Major', 'Minor', 'Trivial'],
    ['Highest', 'High', 'Medium', 'Low', 'Lowest'],

    # === 英文系列（全小写）===
    # 3级
    ['high', 'medium', 'low'],
    ['important', 'normal', 'minor'],
    ['urgent', 'normal', 'low'],

    # 4级
    ['critical', 'high', 'medium', 'low'],
    ['urgent', 'high', 'normal', 'low'],
    ['highest', 'high', 'medium', 'low'],

    # 5级
    ['critical', 'urgent', 'high', 'medium', 'low'],
    ['blocker', 'critical', 'major', 'minor', 'trivial'],
    ['highest', 'high', 'medium', 'low', 'lowest'],

    # === 英文系列（全大写）===
    # 3级
    ['HIGH', 'MEDIUM', 'LOW'],
    ['URGENT', 'NORMAL', 'LOW'],

    # 4级
    ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
    ['URGENT', 'HIGH', 'NORMAL', 'LOW'],

    # 5级
    ['CRITICAL', 'URGENT', 'HIGH', 'MEDIUM', 'LOW'],
    ['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'TRIVIAL'],

    # === P系列（代码风格）===
    # 3级
    ['P0', 'P1', 'P2'],

    # 4级
    ['P0', 'P1', 'P2', 'P3'],

    # 5级
    ['P0', 'P1', 'P2', 'P3', 'P4'],

    # 6级
    ['P0', 'P1', 'P2', 'P3', 'P4', 'P5'],

    # === L系列（Level）===
    ['L0', 'L1', 'L2'],
    ['L0', 'L1', 'L2', 'L3'],
    ['L0', 'L1', 'L2', 'L3', 'L4'],

    # === 数字系列（从1开始）===
    ['1', '2', '3'],
    ['1', '2', '3', '4'],
    ['1', '2', '3', '4', '5'],

    # === 数字系列（从0开始）===
    ['0', '1', '2'],
    ['0', '1', '2', '3'],
    ['0', '1', '2', '3', '4'],

    # === 字母系列 ===
    ['A', 'B', 'C'],
    ['A', 'B', 'C', 'D'],
    ['A', 'B', 'C', 'D', 'E'],
    ['S', 'A', 'B', 'C'],  # S级（游戏/评级风格）
    ['S', 'A', 'B', 'C', 'D'],

    # === 符号系列 ===
    ['★★★', '★★', '★'],
    ['⭐⭐⭐', '⭐⭐', '⭐'],
    ['!!!', '!!', '!'],
    ['+++', '++', '+'],

    # === 颜色系列 ===
    ['红色', '黄色', '绿色'],
    ['红', '橙', '黄', '绿'],
    ['Red', 'Yellow', 'Green'],
    ['red', 'orange', 'yellow', 'green'],

    # === 权重数字系列 ===
    ['100', '50', '0'],
    ['100', '75', '50', '25', '0'],
    ['10', '5', '1'],

    # === 混合中英 ===
    ['P0-紧急', 'P1-高', 'P2-中', 'P3-低'],
    ['Level1-高', 'Level2-中', 'Level3-低'],

    # === 拼音系列 ===
    ['gao', 'zhong', 'di'],
    ['jinji', 'gao', 'zhong', 'di'],

    # === 特殊业务术语 ===
    ['Blocker', 'Critical', 'Normal'],  # Bug优先级
    ['Must', 'Should', 'Could', 'Wont'],  # MoSCoW方法
    ['Now', 'Next', 'Later'],  # 敏捷开发
]


def priorities(num: int) -> list[str]:
    variant = random.choice(PRIORITY_VARIANTS)
    return [random.choice(variant) for _ in range(num)]
