from typing import Callable

from scripts.corpus_generators.email_generator import emails
from scripts.corpus_generators.job_generator import jobs
from scripts.corpus_generators.name_generator import names
from scripts.corpus_generators.url_generator import urls
from scripts.corpus_generators.useragent_generator import useragent
from scripts.corpus_generators.username_generator import usernames
from scripts.seed_generators.address_generator import addresses
from scripts.seed_generators.company_generator import companies
from scripts.seed_generators.hospital_generator import hospitals
from scripts.seed_generators.recreation_generator import recreations
from scripts.seed_generators.residential_generator import residential
from scripts.seed_generators.shopping_generator import shopping
from scripts.variant_generators.age_generator import ages
from scripts.variant_generators.amount_generator import amounts
from scripts.variant_generators.bank_card_generator import bank_cards
from scripts.variant_generators.boolean_generator import booleans
from scripts.variant_generators.coordinate_generator import coordinates
from scripts.variant_generators.date_generator import dates
from scripts.variant_generators.datetime_generator import datetime
from scripts.variant_generators.education_generator import educations
from scripts.variant_generators.ethnicity_generator import ethnicities
from scripts.variant_generators.float_generator import floats
from scripts.variant_generators.gender_generator import genders
from scripts.variant_generators.id_card_generator import id_cards
from scripts.variant_generators.int_generator import ints
from scripts.variant_generators.ip_generator import ips
from scripts.variant_generators.percent_generator import percents
from scripts.variant_generators.phone_generator import phones
from scripts.variant_generators.plate_generator import plates
from scripts.variant_generators.priority_generator import priorities
from scripts.variant_generators.state_generator import states
from scripts.variant_generators.time_generator import times

RANDOM_SEED = 42

VOCAB_SIZE = 20000

PAD_TOKEN_ID = 3
PAD_TOKEN = "<pad>"
SEP_TOKEN = "<sep>"

# 数据生成配置
RAW_CORPUS_PER_TYPE = 150000  # 每种类型的原始数据量
SAMPLES_PER_TYPE = 5000  # 每种类型的样本数
RAW_CORPUS_PER_INPUT = 10  # 每个样本的数据数

# 数据拆分比例
VAL_RATIO = 0.1
TEST_RATIO = 0.1

# 语料生成
CORPUS_TYPES: dict[str, Callable[[int], list[str]]] = {"email": emails, "job": jobs, "name": names, "url": urls,
                                                       "useragent": useragent, "username": usernames}
VARIANT_TYPES: dict[str, Callable[[int], list[str]]] = {"boolean": booleans, "education": educations,
                                                        "ethnicity": ethnicities, "gender": genders,
                                                        "priority": priorities, "state": states,
                                                        "age": ages, "amount": amounts, "bank_card": bank_cards,
                                                        "coordinate": coordinates, "date": dates, "datetime": datetime,
                                                        "float": floats, "id_card": id_cards, "int": ints,
                                                        "ip": ips, "percent": percents, "phone": phones,
                                                        "plate": plates, "time": times}
SEED_TYPES: dict[str, Callable[[int], list[str]]] = {"address": addresses, "company": companies,
                                                     "hospital": hospitals, "recreation": recreations,
                                                     "residential": residential, "shopping": shopping}

ALL_TYPES: list[str] = [*CORPUS_TYPES.keys(), *VARIANT_TYPES.keys(), *SEED_TYPES.keys()]

N_CLASSES = len(ALL_TYPES)

# 无意义的泛化列名（所有类型通用）
GENERIC_COLUMN_NAMES: list[str] = [
    # 英文泛化模式
    "col", "col1", "col2", "col3", "col4", "col5",
    "col_", "col_1", "col_2", "col_3", "col_4", "col_5",
    "column", "column1", "column2", "column3", "column4", "column5",
    "column_", "column_1", "column_2", "column_3", "column_4", "column_5",
    "field", "field1", "field2", "field3", "field4", "field5",
    "field_", "field_1", "field_2", "field_3", "field_4", "field_5",
    "data", "data1", "data2", "data3", "data4", "data5",
    "data_", "data_1", "data_2", "data_3", "data_4", "data_5",
    "value", "value1", "value2", "value3", "value4", "value5",
    "value_", "value_1", "value_2", "value_3", "value_4", "value_5",
    "attr", "attr1", "attr2", "attr3", "attr4", "attr5",
    "attr_", "attr_1", "attr_2", "attr_3", "attr_4", "attr_5",
    "attribute", "attribute1", "attribute2", "attribute3", "attribute4", "attribute5",
    "attribute_", "attribute_1", "attribute_2", "attribute_3", "attribute_4", "attribute_5",
    "prop", "prop1", "prop2", "prop3", "prop4", "prop5",
    "prop_", "prop_1", "prop_2", "prop_3", "prop_4", "prop_5",
    "property", "property1", "property2", "property3", "property4", "property5",
    "property_", "property_1", "property_2", "property_3", "property_4", "property_5",
    "item", "item1", "item2", "item3", "item4", "item5",
    "item_", "item_1", "item_2", "item_3", "item_4", "item_5",
    "element", "element1", "element2", "element3", "element4", "element5",
    "element_", "element_1", "element_2", "element_3", "element_4", "element_5",
    "elem", "elem1", "elem2", "elem3", "elem4", "elem5",
    "elem_", "elem_1", "elem_2", "elem_3", "elem_4", "elem_5",
    "var", "var1", "var2", "var3", "var4", "var5",
    "var_", "var_1", "var_2", "var_3", "var_4", "var_5",
    "variable", "variable1", "variable2", "variable3", "variable4", "variable5",
    "variable_", "variable_1", "variable_2", "variable_3", "variable_4", "variable_5",
    "val", "val1", "val2", "val3", "val4", "val5",
    "val_", "val_1", "val_2", "val_3", "val_4", "val_5",

    # 中文泛化模式
    "列", "列1", "列2", "列3", "列4", "列5",
    "字段", "字段1", "字段2", "字段3", "字段4", "字段5",
    "属性", "属性1", "属性2", "属性3", "属性4", "属性5",
    "数据", "数据1", "数据2", "数据3", "数据4", "数据5",
    "值", "值1", "值2", "值3", "值4", "值5",
    "项", "项1", "项2", "项3", "项4", "项5",
    "内容", "内容1", "内容2", "内容3", "内容4", "内容5",

    # 拼音泛化
    "lie", "lie1", "lie2", "lie3", "lie4", "lie5",
    "lie_1", "lie_2", "lie_3", "lie_4", "lie_5",
    "ziduan", "ziduan1", "ziduan2", "ziduan3", "ziduan4", "ziduan5",
    "ziduan_1", "ziduan_2", "ziduan_3", "ziduan_4", "ziduan_5",
    "shuju", "shuju1", "shuju2", "shuju3", "shuju4", "shuju5",
    "shuju_1", "shuju_2", "shuju_3", "shuju_4", "shuju_5",
    "zhi", "zhi1", "zhi2", "zhi3", "zhi4", "zhi5",
    "zhi_", "zhi_1", "zhi_2", "zhi_3", "zhi_4", "zhi_5",

    # 单字母（常见泛化）
    "a", "b", "c", "d", "e", "f", "g", "h",
    "x", "y", "z",
    "i", "j", "k", "m", "n", "p", "q", "r", "s", "t",

    # 随机无意义字符串（模拟自动生成的列名）
    "aaa", "abc", "xyz", "qwe", "asd", "zxc",
    "foo", "bar", "baz", "qux",
    "tmp", "temp", "test",
    "未命名", "未知", "其他",
]

# 列名的兼容性处理（有意义的类型特定列名）
MAGIC_COLUMN_NAMES: dict[str, list[str]] = {
    # ==================== CORPUS_TYPES ====================
    "age": [
        # 中文标准
        "年龄", "岁数", "年纪", "芳龄", "周岁", "实岁", "虚岁",
        # 拼音
        "nianling", "nianling1", "suishu", "nianji", "zhousuì",
        # 缩写
        "nl", "ss", "nj", "age_", "ag",
        # 英文变体
        "age", "Age", "AGE", "ages", "user_age", "person_age", "field_age",
        # 中英混合
        "年龄age", "age年龄", "用户年龄", "user年龄", "会员age",
        # 业务词汇
        "出生年龄", "当前年龄", "实际年龄", "登记年龄",
        # 后缀
        "age_info", "age_data", "age_value", "年龄信息",
        # typo
        "aeg", "agee", "aage", "nainling",
    ],

    "amount": [
        # 中文标准
        "金额", "数额", "总额", "款项", "价格", "费用",
        # 业务词汇（电商）
        "单价", "总价", "实付", "应付", "到手价", "券后价", "优惠后",
        "成交价", "原价", "现价", "售价", "标价", "吊牌价",
        # 业务词汇（金融）
        "本金", "利息", "收益", "盈利", "亏损", "余额", "结余",
        "投资额", "认购金额", "赎回金额", "交易额",
        # 拼音
        "jine", "jiage", "feiyong", "zonge", "shife",
        # 缩写
        "je", "jg", "fy", "amt", "price", "cost",
        # 英文
        "amount", "Amount", "AMOUNT", "money", "price", "fee", "cost",
        "total", "sum", "payment", "charge", "value",
        # 中英混合
        "金额amount", "amount金额", "实付金额", "totalAmount", "total_amount",
        "价格price", "费用fee", "user_amount", "订单金额",
        # 符号
        "金额(元)", "金额（元）", "价格¥", "amount($)", "RMB",
        # typo
        "amout", "ammount", "amont", "jine1", "jiine"
    ],

    "bank_card": [
        # 中文标准
        "银行卡号", "银行卡", "卡号", "账号", "账户号",
        # 业务词汇
        "借记卡", "信用卡", "储蓄卡", "工资卡", "结算卡",
        "收款账号", "付款账号", "绑定卡号",
        # 拼音
        "yinhangkahao", "kahao", "zhanghao", "yhkh", "yhk",
        # 缩写
        "yhkh", "khao", "zh", "card_no", "card_number", "acct",
        # 英文
        "bank_card", "bankcard", "card", "card_number", "account",
        "account_no", "account_number", "card_no", "bank_account",
        # 中英混合
        "银行卡card", "card号码", "bank_card_no", "卡号number",
        "账户account", "user_card", "绑定卡card",
        # 业务场景
        "提现卡号", "充值卡号", "默认卡号", "主卡号",
        # typo
        "bankcard", "bank_crad", "cardnumber", "yhk1"
    ],

    "coordinate": [
        # 中文标准
        "坐标", "经纬度", "位置", "定位", "地理坐标", "GPS",
        # 分开表示
        "经度", "纬度", "东经", "北纬", "longitude", "latitude",
        # 拼音
        "zuobiao", "jingweidu", "weizhi", "dingwei",
        # 缩写
        "zb", "jwd", "wz", "coord", "pos", "loc", "gps",
        "lng", "lat", "lon",
        # 英文
        "coordinate", "coordinates", "location", "position", "gps",
        "geo", "geolocation", "latlng", "lonlat",
        # 中英混合
        "坐标coordinate", "位置location", "经纬度latlng", "gps坐标",
        "geo_position", "地理位置", "location_info",
        # 业务场景
        "门店位置", "配送地址坐标", "打卡位置", "签到坐标",
        "起点坐标", "终点坐标", "当前位置",
        # typo
        "coordniate", "coordinat", "positon", "loaction"
    ],

    "date": [
        # 中文标准
        "日期", "年月日", "时间", "日子",
        # 业务词汇
        "出生日期", "创建日期", "更新日期", "生效日期", "失效日期",
        "开始日期", "结束日期", "入职日期", "离职日期",
        "注册日期", "发布日期", "截止日期", "到期日期",
        # 拼音
        "riqi", "rq", "shijian", "sj", "nyr",
        # 缩写
        "date", "dt", "day", "ymd", "d",
        # 英文
        "date", "Date", "DATE", "day", "birth_date", "create_date",
        "start_date", "end_date", "register_date", "expire_date",
        # 中英混合
        "日期date", "创建日期", "createDate", "create_time",
        "注册date", "生日birthday", "开始时间",
        # 业务场景
        "下单日期", "付款日期", "发货日期", "签收日期",
        "申请日期", "审核日期", "发放日期",
        # 特定格式
        "年月日", "YYYYMMDD", "出生年月", "年-月-日",
        # typo
        "dat", "datte", "riqi1", "date_"
    ],

    "datetime": [
        # 中文标准
        "时间", "日期时间", "时间戳", "完整时间",
        # 业务词汇
        "创建时间", "更新时间", "修改时间", "删除时间",
        "登录时间", "注册时间", "下单时间", "支付时间",
        "发货时间", "签收时间", "提交时间", "审核时间",
        "开始时间", "结束时间", "过期时间",
        # 拼音
        "shijian", "shijianchuo", "riqishijian", "wanzhengshijian",
        # 缩写
        "sj", "sjc", "dt", "ts", "time", "timestamp",
        # 英文
        "datetime", "timestamp", "time", "created_at", "updated_at",
        "create_time", "update_time", "modify_time", "login_time",
        "start_time", "end_time", "deleted_at",
        # 中英混合
        "时间time", "创建datetime", "timestamp时间戳", "登录时间",
        "createTime", "updateTime", "created_at时间",
        # 技术词汇
        "时间戳timestamp", "unix时间", "毫秒时间戳", "秒级时间戳",
        "UTC时间", "北京时间", "服务器时间",
        # 业务场景
        "下单时间", "付款时间", "确认时间", "完成时间",
        "打卡时间", "签到时间", "最后登录", "最近访问",
        # typo
        "datatime", "timstamp", "creat_time", "updat_time"
    ],

    "email": [
        # 中文标准
        "邮箱", "电子邮箱", "电子邮件", "邮件地址",
        # 拼音
        "youxiang", "youjian", "dianziyouxiang", "yx",
        # 缩写
        "yx", "email", "mail", "e_mail", "em",
        # 英文
        "email", "Email", "EMAIL", "mail", "e_mail", "e-mail",
        "email_address", "mail_address", "user_email",
        # 中英混合
        "邮箱email", "email地址", "userEmail", "user_mail",
        "联系邮箱", "email_info", "邮件mail",
        # 业务场景
        "注册邮箱", "绑定邮箱", "工作邮箱", "私人邮箱",
        "联系邮箱", "接收邮箱", "默认邮箱", "企业邮箱",
        # 后缀
        "email_address", "mail_box", "mailbox", "邮箱地址",
        # typo
        "emial", "eamil", "e_mai", "youxain", "youx1ang"
    ],

    "float": [
        # 中文标准
        "浮点数", "小数", "数值", "实数", "小数值",
        # 业务词汇
        "比率", "比例", "系数", "倍数", "分数", "得分",
        "评分", "权重", "指数", "参数",
        # 拼音
        "fudian", "xiaoshu", "shuzhi", "bili", "xishu",
        # 缩写
        "fd", "xs", "sz", "val", "num", "score", "rate",
        # 英文
        "float", "Float", "FLOAT", "decimal", "number", "value",
        "score", "rate", "ratio", "coefficient", "weight",
        # 中英混合
        "小数float", "数值value", "score分数", "比例rate",
        "float_value", "decimal_num", "评分score",
        # 业务场景
        "综合评分", "信用分", "好评率", "转化率", "增长率",
        "收益率", "成功率", "命中率", "准确率",
        # 技术词汇
        "double", "real", "numeric", "float_val",
        # typo
        "flot", "floatt", "deciaml", "numbr"
    ],

    "id_card": [
        # 中文标准
        "身份证", "身份证号", "身份证号码", "证件号", "证件号码",
        # 拼音
        "shenfenzheng", "shenfenzhenghao", "zhengjianhao", "sfz", "sfzh",
        # 缩写
        "sfz", "sfzh", "zjh", "id", "id_no", "id_card",
        # 英文
        "id_card", "idcard", "id_number", "card_id", "identity_card",
        "citizen_id", "national_id", "id_no",
        # 中英混合
        "身份证id", "id_card号", "证件idcard", "idNumber",
        "card_no身份证", "身份证number",
        # 业务场景
        "实名证件", "身份证件", "有效证件", "证件信息",
        "本人身份证", "用户身份证", "认证身份证",
        # 类型细分
        "居民身份证", "二代身份证", "18位身份证",
        # typo
        "id_crad", "idcar", "sfzh1", "shenfenzhen"
    ],

    "int": [
        # 中文标准
        "整数", "数字", "数量", "个数", "计数",
        # 业务词汇
        "数量", "件数", "人数", "次数", "天数", "年限",
        "编号", "序号", "ID", "流水号", "订单号",
        # 拼ين
        "zhengshu", "shuliang", "geshu", "cishu", "bianhao",
        # 缩写
        "zs", "sl", "gs", "cs", "num", "count", "id",
        # 英文
        "int", "Int", "INT", "integer", "number", "count",
        "quantity", "amount", "total", "id", "no",
        # 中英混合
        "数量quantity", "整数int", "count数量", "number编号",
        "id编号", "序号no", "件数count",
        # 业务场景
        "库存数量", "销量", "访问次数", "点击量", "浏览量",
        "收藏数", "点赞数", "评论数", "转发数", "关注数",
        "下单数", "发货数", "退货数",
        # 技术词汇
        "long", "bigint", "number", "numeric",
        # typo
        "intger", "numer", "coun", "quanity"
    ],

    "ip": [
        # 中文标准
        "IP", "IP地址", "网络地址", "主机地址",
        # 拼音
        "ip", "ipdizhi", "wangluodizhi", "ipaddr",
        # 缩写
        "ip", "addr", "address", "host",
        # 英文
        "ip", "IP", "ip_address", "ipaddress", "ip_addr",
        "host_ip", "server_ip", "client_ip", "remote_ip",
        # 中英混合
        "ip地址", "IPaddress", "ip_address地址", "主机ip",
        "serverIP", "客户端ip", "remote_addr",
        # 业务场景
        "登录IP", "注册IP", "访问IP", "来源IP", "真实IP",
        "用户IP", "客户IP", "服务器IP", "代理IP",
        # 技术词汇
        "ipv4", "ipv6", "public_ip", "private_ip", "local_ip",
        "wan_ip", "lan_ip", "内网IP", "外网IP",
        # 类型
        "IP地址(IPv4)", "IP(v6)", "ipv4地址",
        # typo
        "ip_adress", "ipadres", "ipaddres"
    ],

    "job": [
        # 中文标准
        "职业", "工作", "职位", "岗位", "职务", "行业",
        # 业务词汇
        "职称", "工种", "职级", "职能", "从事行业",
        "当前职业", "所属行业", "工作类型",
        # 拼音
        "zhiye", "gongzuo", "zhiwei", "gangwei", "zhiwu",
        # 缩写
        "zy", "gz", "zw", "gw", "job", "work", "pos",
        # 英文
        "job", "Job", "JOB", "occupation", "position", "career",
        "profession", "work", "title", "role",
        # 中英混合
        "职业job", "工作work", "position职位", "岗位post",
        "职业occupation", "title职称", "career",
        # 业务场景
        "申请职位", "应聘岗位", "目标职位", "期望职位",
        "现任职位", "历史职位", "主要职业",
        # 行业分类
        "从业领域", "所在行业", "工作领域", "职业类别",
        # typo
        "jbo", "ocupation", "positon", "zhiy"
    ],

    "name": [
        # 中文标准
        "姓名", "名字", "人名", "真实姓名", "本名",
        # 业务词汇
        "用户名", "客户名", "会员名", "收货人", "联系人",
        "真实姓名", "昵称", "笔名", "艺名",
        # 拼音
        "xingming", "mingzi", "renming", "yonghuming", "xm",
        # 缩写
        "xm", "mz", "name", "nm", "username",
        # 英文
        "name", "Name", "NAME", "username", "user_name",
        "real_name", "full_name", "person_name", "customer_name",
        # 中英混合
        "姓名name", "name姓名", "userName", "real_name真实姓名",
        "用户name", "customer姓名", "收货人name",
        # 业务场景
        "收件人", "寄件人", "联系人姓名", "负责人", "经办人",
        "申请人", "审批人", "操作人", "创建人", "修改人",
        # 细分
        "姓", "名", "first_name", "last_name", "middle_name",
        "surname", "given_name",
        # typo
        "nmae", "naem", "usrname", "xingmin"
    ],

    "percent": [
        # 中文标准
        "百分比", "比例", "占比", "百分率", "比率",
        # 业务词汇
        "增长率", "下降率", "转化率", "达成率", "完成率",
        "好评率", "差评率", "退货率", "复购率", "留存率",
        "收益率", "利润率", "毛利率", "折扣", "优惠",
        # 拼音
        "baifenbi", "bili", "zhanbi", "lvzhi", "bfb",
        # 缩写
        "bfb", "bl", "zb", "pct", "rate", "ratio", "perc",
        # 英文
        "percent", "Percent", "PERCENT", "percentage", "rate",
        "ratio", "proportion", "pct",
        # 中英混合
        "百分比percent", "比例ratio", "rate比率", "转化率",
        "completion_rate完成率", "增长rate",
        # 符号
        "百分比(%)", "比例%", "rate(%)", "占比（%）",
        # 业务场景
        "涨幅", "跌幅", "增幅", "降幅", "波动率",
        "同比", "环比", "增速", "增长率",
        # typo
        "precent", "persentage", "raito", "baifenb"
    ],

    "phone": [
        # 中文标准
        "手机", "手机号", "手机号码", "电话", "电话号码",
        "联系电话", "联系方式", "移动电话",
        # 业务词汇
        "座机", "固话", "办公电话", "家庭电话", "紧急联系电话",
        "主叫号码", "被叫号码", "来电号码", "回拨号码",
        # 拼音
        "shouji", "dianhua", "shoujihao", "dianhuahaoma",
        "lianxidianhua", "lianxifangshi", "sjh", "dhh",
        # 缩写
        "sjh", "dh", "lxdh", "lxfs", "tel", "phone", "mob", "mobile",
        # 英文
        "phone", "Phone", "PHONE", "mobile", "telephone", "tel",
        "phone_number", "mobile_number", "tel_number", "contact",
        # 中英混合
        "手机phone", "电话tel", "phone号码", "mobile手机",
        "联系电话contact", "telephone号码", "手机号mobile",
        # 业务场景
        "注册手机", "绑定手机", "收货电话", "联系手机",
        "主要电话", "备用电话", "紧急联系人电话",
        # 前缀
        "user_phone", "customer_phone", "member_mobile",
        # typo
        "phoen", "moblie", "telephon", "shouji1"
    ],

    "plate": [
        # 中文标准
        "车牌", "车牌号", "车牌号码", "号牌", "牌照",
        # 业务词汇
        "车辆号牌", "机动车号牌", "车号", "车辆编号",
        "新能源车牌", "蓝牌", "黄牌", "绿牌",
        # 拼音
        "chepai", "chepaihao", "haopai", "paizhao", "cp", "cph",
        # 缩写
        "cp", "cph", "hp", "plate", "plate_no", "license",
        # 英文
        "plate", "Plate", "PLATE", "plate_number", "license_plate",
        "license_number", "vehicle_plate", "car_plate",
        # 中英混合
        "车牌plate", "plate号码", "车牌号number", "license车牌",
        "vehicle_plate车辆", "车牌license",
        # 业务场景
        "登记车牌", "绑定车牌", "违章车牌", "进出车牌",
        "停车车牌", "通行车牌", "车辆牌照",
        # 类型
        "小型车牌", "大型车牌", "新能源牌照",
        # typo
        "plat", "licens", "chepai1", "chepaihao1"
    ],

    "time": [
        # 中文标准
        "时间", "时刻", "钟点", "具体时间", "时分秒",
        # 业务词汇
        "开始时间", "结束时间", "营业时间", "上班时间", "下班时间",
        "打卡时间", "签到时间", "预约时间", "到达时间",
        # 拼音
        "shijian", "shike", "zhongdian", "shifenmiao", "sj",
        # 缩写
        "sj", "sk", "time", "tm", "hms",
        # 英文
        "time", "Time", "TIME", "hour", "clock", "o_clock",
        "start_time", "end_time", "begin_time", "finish_time",
        # 中英混合
        "时间time", "时刻clock", "开始时间start", "time具体时间",
        "hour小时", "营业时间business_hours",
        # 格式
        "时:分:秒", "HH:MM:SS", "时分", "几点",
        # 业务场景
        "送达时间", "配送时间", "预计时间", "最晚时间",
        "上门时间", "服务时间", "就诊时间",
        # 24小时制
        "24小时制", "12小时制", "时间点",
        # typo
        "tim", "tiem", "shijain", "shijian1"
    ],

    "url": [
        # 中文标准
        "网址", "链接", "地址", "URL", "链接地址",
        # 业务词汇
        "页面地址", "跳转链接", "分享链接", "下载地址",
        "访问地址", "回调地址", "重定向地址",
        # 拼音
        "wangzhi", "lianjie", "dizhi", "url", "link",
        # 缩写
        "url", "link", "addr", "href", "uri",
        # 英文
        "url", "URL", "Url", "link", "Link", "LINK",
        "address", "web_url", "website", "href", "uri",
        # 中英混合
        "网址url", "链接link", "url地址", "link链接",
        "访问url", "跳转link", "回调url",
        # 业务场景
        "商品链接", "详情页", "支付链接", "分享url",
        "图片地址", "视频地址", "文件地址", "资源地址",
        # 技术词汇
        "endpoint", "api_url", "callback_url", "redirect_url",
        "return_url", "notify_url",
        # typo
        "ulr", "urll", "lik", "addres"
    ],

    "useragent": [
        # 中文标准
        "用户代理", "浏览器标识", "客户端标识", "UA",
        # 拼音
        "yonghudaili", "liulanqi", "kehuduanbiaoshi", "ua",
        # 缩写
        "ua", "agent", "user_agent", "useragent",
        # 英文
        "useragent", "UserAgent", "user_agent", "user-agent",
        "ua", "UA", "agent", "browser", "client",
        # 中英混合
        "用户代理ua", "浏览器useragent", "客户端agent",
        "user_agent信息", "ua标识",
        # 业务场景
        "浏览器信息", "设备信息", "客户端类型", "终端类型",
        "访问终端", "登录设备", "操作系统",
        # 技术词汇
        "http_user_agent", "client_agent", "browser_info",
        "device_info", "platform",
        # 简写
        "ua_string", "agent_string", "browser_ua",
        # typo
        "user_agnet", "useragnt", "user_agen"
    ],

    "username": [
        # 中文标准
        "用户名", "账号", "账户", "登录名", "昵称",
        # 业务词汇
        "会员名", "账户名", "ID", "user_id", "会员账号",
        "登录账号", "注册账号", "昵称", "网名",
        # 拼音
        "yonghuming", "zhanghao", "denglumming", "nicheng",
        "yhm", "zh", "nc",
        # 缩写
        "yhm", "zh", "nc", "user", "account", "login",
        # 英文
        "username", "Username", "USERNAME", "user_name",
        "account", "login", "login_name", "user_id", "userid",
        # 中英混合
        "用户名username", "账号account", "user用户", "login登录名",
        "username账号", "昵称nickname", "会员user",
        # 业务场景
        "登录用户名", "注册用户名", "显示名称", "用户标识",
        "会员ID", "客户账号", "操作账号",
        # 技术词汇
        "login_id", "user_login", "account_name", "display_name",
        # typo
        "usrname", "user_nam", "accout", "yonghumin"
    ],

    # ==================== VOCAB_TYPES ====================
    "boolean": [
        # 中文标准
        "布尔", "布尔值", "真假", "是否", "标志", "标记",
        # 业务词汇
        "是否有效", "是否启用", "是否删除", "是否可用",
        "是否通过", "是否成功", "是否完成", "是否激活",
        # 拼音
        "buer", "buerzhi", "zhengjia", "shifou", "biaozhi",
        # 缩写
        "bool", "flag", "is", "has", "can", "status",
        # 英文
        "boolean", "Boolean", "BOOLEAN", "bool", "flag",
        "is_active", "is_valid", "is_deleted", "is_enabled",
        "has_xxx", "can_xxx", "enabled", "disabled",
        # 中英混合
        "布尔boolean", "标志flag", "是否is", "enable启用",
        "valid有效", "active激活",
        # 业务场景
        "启用状态", "删除标记", "有效标志", "通过标记",
        "成功标志", "完成状态", "激活状态",
        # 0/1表示
        "状态(0/1)", "标记(true/false)", "是否(Y/N)",
        # typo
        "boolea", "flg", "is_activ", "enable"
    ],

    "education": [
        # 中文标准
        "学历", "教育程度", "文化程度", "受教育程度", "最高学历",
        # 业务词汇
        "毕业学历", "当前学历", "第一学历", "最高学位",
        "教育背景", "学位", "文凭",
        # 拼音
        "xueli", "jiaoyuchengdu", "wenhuachengdu", "xl",
        # 缩写
        "xl", "jy", "edu", "degree", "education",
        # 英文
        "education", "Education", "EDUCATION", "degree",
        "edu_level", "education_level", "academic", "diploma",
        # 中英混合
        "学历education", "教育程度degree", "edu学历",
        "degree学位", "文化程度level", "最高学历edu",
        # 业务场景
        "申请学历", "认证学历", "登记学历", "个人学历",
        "要求学历", "最低学历",
        # 学历层次
        "学历层次", "教育等级", "学位等级",
        # typo
        "educaton", "degre", "xueli1", "jiaoyuchengd"
    ],

    "ethnicity": [
        # 中文标准
        "民族", "族别", "民族成分", "所属民族",
        # 拼音
        "minzu", "zubie", "minzuchengfen", "mz",
        # 缩写
        "mz", "zb", "ethnic", "ethnicity", "nation",
        # 英文
        "ethnicity", "Ethnicity", "ETHNICITY", "ethnic",
        "nationality", "race", "ethnic_group",
        # 中英混合
        "民族ethnicity", "族别ethnic", "nation民族",
        "ethnic_group民族", "所属民族",
        # 业务场景
        "登记民族", "申报民族", "个人民族", "户籍民族",
        # 细分
        "少数民族", "汉族", "民族类别",
        # typo
        "ethnicty", "minzu1", "zubie1", "nationaliy"
    ],

    "gender": [
        # 中文标准
        "性别", "男女", "性别标识", "生理性别",
        # 业务词汇
        "用户性别", "会员性别", "客户性别", "患者性别",
        # 拼音
        "xingbie", "nannu", "xb", "sex",
        # 缩写
        "xb", "nn", "sex", "gender", "g",
        # 英文
        "gender", "Gender", "GENDER", "sex", "Sex", "SEX",
        "male_female", "m_f",
        # 中英混合
        "性别gender", "sex性别", "男女sex", "gender标识",
        "user_gender用户性别", "性别sex",
        # 业务场景
        "登记性别", "申报性别", "个人性别", "实名性别",
        # 表示方式
        "性别(男/女)", "sex(M/F)", "男女(0/1)",
        # typo
        "gendr", "sex1", "xingbie1", "gende"
    ],

    "priority": [
        # 中文标准
        "优先级", "优先度", "重要程度", "紧急程度", "等级",
        # 业务词汇
        "任务优先级", "工单等级", "问题级别", "处理优先级",
        "重要性", "紧急度", "优先等级", "级别",
        # 拼音
        "youxianji", "dengji", "jibie", "zhongyaochengdu",
        "yxj", "dj", "jb",
        # 缩写
        "yxj", "dj", "jb", "priority", "level", "rank",
        # 英文
        "priority", "Priority", "PRIORITY", "level", "rank",
        "importance", "urgency", "grade", "degree",
        # 中英混合
        "优先级priority", "等级level", "priority级别",
        "重要程度importance", "rank等级", "紧急度urgency",
        # 业务场景
        "处理优先级", "响应等级", "工单级别", "任务等级",
        "客户等级", "会员等级", "服务级别",
        # 表示方式
        "优先级(高/中/低)", "level(P0/P1)", "等级(L1/L2)",
        # typo
        "priorit", "lvel", "youxianji1", "dengji1"
    ],

    "state": [
        # 中文标准
        "状态", "状况", "情况", "当前状态", "状态值",
        # 业务词汇（通用）
        "订单状态", "任务状态", "工单状态", "流程状态",
        "审核状态", "支付状态", "发货状态", "处理状态",
        # 业务词汇（具体）
        "启用状态", "锁定状态", "激活状态", "删除状态",
        "在线状态", "运行状态", "完成状态", "进行状态",
        # 拼音
        "zhuangtai", "zhuangkuang", "qingkuang", "zt",
        # 缩写
        "zt", "status", "state", "st", "condition",
        # 英文
        "state", "State", "STATE", "status", "Status", "STATUS",
        "condition", "situation", "phase", "stage",
        # 中英混合
        "状态state", "status状态", "当前状态current", "阶段phase",
        "情况condition", "流程状态flow_status",
        # 业务场景
        "处理状态", "当前阶段", "执行状态", "业务状态",
        "系统状态", "设备状态", "连接状态",
        # 表示方式
        "状态(待处理/处理中/已完成)", "status(0/1/2)",
        # 技术词汇
        "state_machine", "workflow_status", "lifecycle",
        # typo
        "statu", "stat", "zhuangtai1", "staus"
    ],

    # ==================== SEED_TYPES ====================
    "address": [
        # 中文标准
        "地址", "详细地址", "住址", "地点", "位置",
        # 业务词汇（收发货）
        "收货地址", "发货地址", "配送地址", "送货地址", "邮寄地址",
        "收件地址", "寄件地址", "快递地址", "物流地址",
        # 业务词汇（注册登记）
        "注册地址", "联系地址", "通讯地址", "办公地址", "经营地址",
        "家庭地址", "现住址", "常住地址", "户籍地址", "居住地址",
        # 拼音
        "dizhi", "dz", "xiangxidizhi", "zhuzhi", "lxdz",
        # 缩写
        "dz", "xxdz", "addr", "address", "location", "loc",
        # 英文
        "address", "Address", "ADDRESS", "addr", "location",
        "shipping_address", "delivery_address", "contact_address",
        # 中英混合
        "地址address", "收货地址shipping", "addr详细地址",
        "location位置", "delivery_addr配送", "联系地址contact",
        # 业务场景
        "默认地址", "常用地址", "新地址", "备用地址",
        "发票地址", "退货地址", "安装地址", "上门地址",
        # 后缀
        "address_info", "address_detail", "full_address", "地址信息",
        # typo
        "addres", "adress", "dizhi1", "loaction"
    ],

    "company": [
        # 中文标准
        "公司", "公司名称", "企业", "企业名称", "单位", "工作单位",
        # 业务词汇
        "所在公司", "任职公司", "就职单位", "供职单位",
        "用人单位", "雇主", "东家", "所属企业",
        # 类型细分
        "公司全称", "公司简称", "企业全称", "单位名称",
        "注册公司", "开户公司", "缴费单位",
        # 拼音
        "gongsi", "qiye", "danwei", "gsmc", "qymc", "dwmc",
        # 缩写
        "gs", "qy", "dw", "company", "corp", "enterprise", "org",
        # 英文
        "company", "Company", "COMPANY", "enterprise", "corporation",
        "corp", "organization", "employer", "firm",
        # 中英混合
        "公司company", "企业enterprise", "company名称", "单位org",
        "employer雇主", "corporation企业", "工作单位work_unit",
        # 业务场景
        "投保公司", "承保企业", "签约公司", "合作企业",
        "客户公司", "供应商", "厂商", "制造商",
        # 后缀
        "company_name", "corp_name", "enterprise_name", "公司名",
        # typo
        "compay", "copany", "gongsi1", "qiye1", "danwei1"
    ],

    "hospital": [
        # 中文标准
        "医院", "医院名称", "医疗机构", "医疗单位", "就诊医院",
        # 业务词汇
        "治疗医院", "住院医院", "手术医院", "诊疗机构",
        "定点医院", "报销医院", "合作医院", "指定医院",
        # 类型细分
        "医院全称", "就医医院", "所在医院", "转诊医院",
        "三甲医院", "专科医院", "综合医院", "社区医院",
        # 拼音
        "yiyuan", "yy", "yiyuanmingcheng", "yljg",
        # 缩写
        "yy", "hospital", "clinic", "medical", "med",
        # 英文
        "hospital", "Hospital", "HOSPITAL", "clinic", "medical_center",
        "healthcare", "medical_institution", "infirmary",
        # 中英混合
        "医院hospital", "医疗机构medical", "clinic诊所",
        "hospital名称", "定点医院designated", "就诊hospital",
        # 业务场景
        "住院医院", "门诊医院", "急诊医院", "体检医院",
        "转院医院", "康复医院", "疗养医院",
        # 后缀
        "hospital_name", "medical_institution", "clinic_name", "医院名",
        # typo
        "hopital", "hospitl", "yiyuan1", "yiyaun"
    ],

    "recreation": [
        # 中文标准
        "娱乐场所", "休闲场所", "活动场所", "娱乐地点", "休闲地点",
        # 业务词汇
        "娱乐设施", "休闲设施", "活动中心", "文娱场所",
        "健身场所", "运动场所", "游乐场所", "消遣地点",
        # 类型细分
        "娱乐项目", "休闲项目", "活动场地", "娱乐场地",
        "健身房", "游乐场", "活动室", "娱乐城",
        # 拼音
        "yulechangsuo", "xiuxianchangsuo", "hdcs", "ylcs",
        # 缩写
        "ylcs", "xxcs", "recreation", "rec", "entertainment", "ent",
        # 英文
        "recreation", "Recreation", "RECREATION", "entertainment",
        "leisure", "activity", "amusement", "fun_place",
        # 中英混合
        "娱乐recreation", "休闲leisure", "entertainment场所",
        "activity活动", "娱乐场所rec", "健身gym",
        # 业务场景
        "常去娱乐", "喜好娱乐", "休闲偏好", "活动地点",
        "消费场所", "打卡地点", "聚会地点",
        # 后缀
        "recreation_place", "entertainment_venue", "leisure_place",
        # typo
        "recreaton", "entertanment", "yule1", "xiuxian1"
    ],

    "residential": [
        # 中文标准
        "小区", "住宅区", "居住地", "社区", "小区名称",
        # 业务词汇
        "所在小区", "居住小区", "住宅小区", "居民区",
        "生活小区", "住宅社区", "居住社区", "家庭住址小区",
        # 类型细分
        "小区全称", "楼盘名称", "项目名称", "地产名称",
        "花园小区", "公寓小区", "别墅区", "住宅项目",
        # 拼音
        "xiaoqu", "zhuzhaiq", "shequ", "juzhuди", "xq", "sq",
        # 缩写
        "xq", "sq", "residential", "community", "residence", "res",
        # 英文
        "residential", "Residential", "RESIDENTIAL", "community",
        "residence", "housing", "neighborhood", "estate",
        # 中英混合
        "小区residential", "社区community", "residence住宅",
        "neighborhood邻里", "住宅区housing", "estate楼盘",
        # 业务场景
        "注册小区", "登记小区", "配送小区", "服务小区",
        "所属社区", "管辖小区", "片区",
        # 后缀
        "residential_area", "community_name", "residence_name",
        # typo
        "residencial", "comunity", "xiaoqu1", "shequ1"
    ],

    "shopping": [
        # 中文标准
        "商场", "购物中心", "商业区", "购物广场", "商圈",
        # 业务词汇
        "购物地点", "消费场所", "商业中心", "购物场所",
        "商业广场", "百货商场", "购物mall", "商业体",
        # 类型细分
        "大型商场", "购物中心", "百货大楼", "商业综合体",
        "超市", "卖场", "商业街", "步行街",
        # 拼音
        "shangchang", "gouwuzhongxin", "shangyequ", "sc", "gwzx",
        # 缩写
        "sc", "gwzx", "syq", "mall", "shopping", "market",
        # 英文
        "shopping", "Shopping", "SHOPPING", "mall", "market",
        "plaza", "commercial", "store", "shop",
        # 中英混合
        "商场mall", "购物shopping", "market市场", "plaza广场",
        "商业中心commercial", "shopping_center购物", "超市supermarket",
        # 业务场景
        "常去商场", "购物偏好", "消费商场", "会员商场",
        "合作商场", "积分商场", "优惠商场",
        # 后缀
        "shopping_mall", "shopping_center", "commercial_area",
        # typo
        "shoping", "shoppin", "shangchang1", "mall1"
    ],
}
