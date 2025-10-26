# 状态变体
import random

STATUS_VARIANTS = [
    # ============ 订单领域 (8个状态) ============
    # 细粒度
    ['待支付', '已支付', '待发货', '已发货', '已签收', '已取消', '退款中', '已退款'],  # [0, 8] 中文
    # [1, 8] 英文
    ['pending_payment', 'paid', 'pending_ship', 'shipped', 'delivered', 'cancelled', 'refunding', 'refunded'],
    ['unpaid', 'paid', 'to_ship', 'shipped', 'delivered', 'cancel', 'refunding', 'refunded'],  # [2, 8] 英文简写
    ['0', '1', '2', '3', '4', '-1', '5', '6'],  # [3, 8] 数字
    ['daizhifu', 'yizhifu', 'daifahuo', 'yifahuo', 'yiqianshou', 'yiquxiao', 'tuikuanzhong', 'yituikuan'],  # [4, 8] 拼音
    ['dzf', 'yzf', 'dfh', 'yfh', 'yqs', 'yqx', 'tkz', 'ytk'],  # [5, 8] 拼音缩写

    # 粗粒度（3态）
    ['待处理', '进行中', '已完成'],  # [6, 3] 中文粗
    ['pending', 'processing', 'completed'],  # [7, 3] 英文粗
    ['0', '1', '2'],  # [8, 3] 数字粗

    # ============ 任务领域 (4个状态) ============
    ['待处理', '进行中', '已完成', '已关闭'],  # [9, 4] 中文
    ['todo', 'in_progress', 'completed', 'closed'],  # [10, 4] 英文
    ['pending', 'doing', 'done', 'closed'],  # [11, 4] 英文简写
    ['0', '1', '2', '3'],  # [12, 4] 数字
    ['daichuli', 'jinxingzhong', 'yiwancheng', 'yiguanbi'],  # [13, 4] 拼音
    ['dcl', 'jxz', 'ywc', 'ygb'],  # [14, 4] 拼音缩写

    # ============ 审批领域 (6个状态) ============
    ['草稿', '待审批', '审批中', '已通过', '已驳回', '已撤回'],  # [15, 6] 中文
    ['draft', 'pending', 'in_review', 'approved', 'rejected', 'withdrawn'],  # [16, 6] 英文
    ['draft', 'waiting', 'reviewing', 'pass', 'reject', 'cancel'],  # [17, 6] 英文简写
    ['0', '1', '2', '3', '-1', '-2'],  # [18, 6] 数字
    ['caogao', 'daishenpi', 'shenpizhong', 'yitongguo', 'yibohui', 'yichehui'],  # [19, 6] 拼音
    ['cg', 'dsp', 'spz', 'ytg', 'ybh', 'ych'],  # [20, 6] 拼音缩写

    # ============ 会员领域 (4个状态) ============
    ['正常', '冻结', '注销', '黑名单'],  # [21, 4] 中文
    ['active', 'frozen', 'cancelled', 'blacklisted'],  # [22, 4] 英文
    ['normal', 'freeze', 'cancel', 'blocked'],  # [23, 4] 英文简写
    ['1', '0', '-1', '-2'],  # [24, 4] 数字
    ['zhengchang', 'dongjie', 'zhuxiao', 'heimingdan'],  # [25, 4] 拼音
    ['zc', 'dj', 'zx', 'hmd'],  # [26, 4] 拼音缩写

    # ============ 设备领域 (4个状态) ============
    ['在线', '离线', '故障', '维护中'],  # [27, 4] 中文
    ['online', 'offline', 'error', 'maintenance'],  # [28, 4] 英文
    ['on', 'off', 'err', 'fix'],  # [29, 4] 英文简写
    ['1', '0', '-1', '2'],  # [30, 4] 数字
    ['zaixian', 'lixian', 'guzhang', 'weihuzhong'],  # [31, 4] 拼音
    ['zx', 'lx', 'gz', 'whz'],  # [32, 4] 拼音缩写

    # ============ 支付领域 (5个状态) ============
    ['未支付', '支付中', '已支付', '支付失败', '已退款'],  # [33, 5] 中文
    ['unpaid', 'paying', 'paid', 'failed', 'refunded'],  # [34, 5] 英文
    ['wait', 'processing', 'success', 'fail', 'refund'],  # [35, 5] 英文简写
    ['0', '1', '2', '-1', '3'],  # [36, 5] 数字
    ['weizhifu', 'zhifuzhong', 'yizhifu', 'zhifushibai', 'yituikuan'],  # [37, 5] 拼音
    ['wzf', 'zfz', 'yzf', 'zfsb', 'ytk'],  # [38, 5] 拼音缩写

    # ============ 工单领域 (6个状态) ============
    ['待处理', '已分配', '进行中', '已解决', '已关闭', '重新打开'],  # [39, 6] 中文
    ['open', 'assigned', 'in_progress', 'resolved', 'closed', 'reopened'],  # [40, 6] 英文
    ['new', 'assign', 'doing', 'solved', 'close', 'reopen'],  # [41, 6] 英文简写
    ['0', '1', '2', '3', '4', '5'],  # [42, 6] 数字
    ['daichuli', 'yifenpei', 'jinxingzhong', 'yijiejue', 'yiguanbi', 'chongxindakai'],  # [43, 6] 拼音
    ['dcl', 'yfp', 'jxz', 'yjj', 'ygb', 'cxdk'],  # [44, 6] 拼音缩写

    # ============ 物流领域 (6个状态) ============
    ['待揽收', '已揽收', '运输中', '派送中', '已签收', '异常'],  # [45, 6] 中文
    ['pending_pickup', 'picked_up', 'in_transit', 'delivering', 'delivered', 'exception'],  # [46, 6] 英文
    ['wait', 'pickup', 'transit', 'delivery', 'received', 'error'],  # [47, 6] 英文简写
    ['0', '1', '2', '3', '4', '-1'],  # [48, 6] 数字
    ['dailanshou', 'yilanshou', 'yunshuzhong', 'paisongzhong', 'yiqianshou', 'yichang'],  # [49, 6] 拼音
    ['dls', 'yls', 'ysz', 'psz', 'yqs', 'yc'],  # [50, 6] 拼音缩写

    # ============ 预约领域 (6个状态) ============
    ['待预约', '已预约', '待确认', '已确认', '已完成', '已取消'],  # [51, 6] 中文
    ['not_booked', 'booked', 'pending_confirm', 'confirmed', 'completed', 'cancelled'],  # [52, 6] 英文
    ['wait', 'booked', 'confirming', 'confirm', 'done', 'cancel'],  # [53, 6] 英文简写
    ['0', '1', '2', '3', '4', '-1'],  # [54, 6] 数字
    ['daiyuyue', 'yiyuyue', 'daiqueren', 'yiqueren', 'yiwancheng', 'yiquxiao'],  # [55, 6] 拼音
    ['dyy', 'yyy', 'dqr', 'yqr', 'ywc', 'yqx'],  # [56, 6] 拼音缩写

    # ============ 考试领域 (5个状态) ============
    ['未开始', '进行中', '已交卷', '已批改', '已发布'],  # [57, 5] 中文
    ['not_started', 'in_progress', 'submitted', 'graded', 'published'],  # [58, 5] 英文
    ['wait', 'doing', 'submit', 'graded', 'release'],  # [59, 5] 英文简写
    ['0', '1', '2', '3', '4'],  # [60, 5] 数字
    ['weikaishi', 'jinxingzhong', 'yijiaojuan', 'yipigai', 'yifabu'],  # [61, 5] 拼音
    ['wks', 'jxz', 'yjj', 'ypg', 'yfb'],  # [62, 5] 拼音缩写

    # ============ 文章领域 (5个状态) ============
    ['草稿', '待审核', '已发布', '已下架', '已删除'],  # [63, 5] 中文
    ['draft', 'pending_review', 'published', 'offline', 'deleted'],  # [64, 5] 英文
    ['draft', 'review', 'online', 'offline', 'delete'],  # [65, 5] 英文简写
    ['0', '1', '2', '-1', '-2'],  # [66, 5] 数字
    ['caogao', 'daishenhe', 'yifabu', 'yixiajia', 'yishanchu'],  # [67, 5] 拼音
    ['cg', 'dsh', 'yfb', 'yxj', 'ysc'],  # [68, 5] 拼音缩写

    # ============ 合同领域 (6个状态) ============
    ['草拟', '待签署', '已签署', '执行中', '已完成', '已作废'],  # [69, 6] 中文
    ['drafting', 'pending_sign', 'signed', 'executing', 'completed', 'voided'],  # [70, 6] 英文
    ['draft', 'wait_sign', 'signed', 'running', 'done', 'void'],  # [71, 6] 英文简写
    ['0', '1', '2', '3', '4', '-1'],  # [72, 6] 数字
    ['caoni', 'daiqianshu', 'yiqianshu', 'zhixingzhong', 'yiwancheng', 'yizuofei'],  # [73, 6] 拼音
    ['cn', 'dqs', 'yqs', 'zxz', 'ywc', 'yzf'],  # [74, 6] 拼音缩写

    # ============ 项目领域 (6个状态) ============
    ['未启动', '规划中', '执行中', '已完成', '已归档', '已暂停'],  # [75, 6] 中文
    ['not_started', 'planning', 'executing', 'completed', 'archived', 'paused'],  # [76, 6] 英文
    ['wait', 'plan', 'doing', 'done', 'archive', 'pause'],  # [77, 6] 英文简写
    ['0', '1', '2', '3', '4', '-1'],  # [78, 6] 数字
    ['weiqidong', 'guihuazhong', 'zhixingzhong', 'yiwancheng', 'yiguidang', 'yizanting'],  # [79, 6] 拼音
    ['wqd', 'ghz', 'zxz', 'ywc', 'ygd', 'yzt'],  # [80, 6] 拼音缩写

    # ============ 请假领域 (5个状态) ============
    ['待提交', '待审批', '已批准', '已拒绝', '已销假'],  # [81, 5] 中文
    ['draft', 'pending_approval', 'approved', 'rejected', 'returned'],  # [82, 5] 英文
    ['draft', 'waiting', 'pass', 'reject', 'back'],  # [83, 5] 英文简写
    ['0', '1', '2', '-1', '3'],  # [84, 5] 数字
    ['daitijiao', 'daishenpi', 'yipizhun', 'yijujue', 'yixiaojia'],  # [85, 5] 拼音
    ['dtj', 'dsp', 'ypz', 'yjj', 'yxj'],  # [86, 5] 拼音缩写

    # ============ 报销领域 (6个状态) ============
    ['待提交', '待审核', '审核中', '已通过', '已打款', '已拒绝'],  # [87, 6] 中文
    ['draft', 'pending_review', 'reviewing', 'approved', 'paid', 'rejected'],  # [88, 6] 英文
    ['draft', 'wait', 'reviewing', 'pass', 'paid', 'reject'],  # [89, 6] 英文简写
    ['0', '1', '2', '3', '4', '-1'],  # [90, 6] 数字
    ['daitijiao', 'daishenhe', 'shenhezhong', 'yitongguo', 'yidakuan', 'yijujue'],  # [91, 6] 拼音
    ['dtj', 'dsh', 'shz', 'ytg', 'ydk', 'yjj'],  # [92, 6] 拼音缩写

    # ============ 招聘领域 (9个状态) ============
    ['简历筛选', '初试', '复试', '终试', 'offer', '入职', '已淘汰'],  # [93, 7] 中文
    ['resume_screening', 'first_interview', 'second_interview', 'final_interview', 'offer', 'onboarded', 'rejected'],
    # [94, 7] 英文
    ['screening', 'first', 'second', 'final', 'offer', 'hired', 'reject'],  # [95, 7] 英文简写
    ['0', '1', '2', '3', '4', '5', '-1'],  # [96, 7] 数字
    ['jianli', 'chushi', 'fushi', 'zhongshi', 'offer', 'ruzhi', 'yitaotai'],  # [97, 7] 拼音
    ['jl', 'cs', 'fs', 'zs', 'offer', 'rz', 'ytt'],  # [98, 7] 拼音缩写

    # ============ 库存领域 (4个状态) ============
    ['充足', '不足', '预警', '缺货'],  # [99, 4] 中文
    ['sufficient', 'insufficient', 'warning', 'out_of_stock'],  # [100, 4] 英文
    ['enough', 'low', 'alert', 'empty'],  # [101, 4] 英文简写
    ['2', '1', '0', '-1'],  # [102, 4] 数字
    ['chongzu', 'buzu', 'yujing', 'quehuo'],  # [103, 4] 拼音
    ['cz', 'bz', 'yj', 'qh'],  # [104, 4] 拼音缩写

    # ============ 发票领域 (5个状态) ============
    ['待开票', '已开票', '待邮寄', '已邮寄', '已签收'],  # [105, 5] 中文
    ['pending_issue', 'issued', 'pending_mail', 'mailed', 'received'],  # [106, 5] 英文
    ['wait', 'issued', 'to_mail', 'mailed', 'received'],  # [107, 5] 英文简写
    ['0', '1', '2', '3', '4'],  # [108, 5] 数字
    ['daikaipiao', 'yikaipiao', 'daiyouji', 'yiyouji', 'yiqianshou'],  # [109, 5] 拼音
    ['dkp', 'ykp', 'dyj', 'yyj', 'yqs'],  # [110, 5] 拼音缩写

    # ============ 认证领域 (5个状态) ============
    ['未认证', '待审核', '已认证', '认证失败', '已过期'],  # [111, 5] 中文
    ['not_verified', 'pending_review', 'verified', 'failed', 'expired'],  # [112, 5] 英文
    ['wait', 'reviewing', 'pass', 'fail', 'expire'],  # [113, 5] 英文简写
    ['0', '1', '2', '-1', '-2'],  # [114, 5] 数字
    ['weirenzheng', 'daishenhe', 'yirenzheng', 'renzhengshibai', 'yiguoqi'],  # [115, 5] 拼音
    ['wrz', 'dsh', 'yrz', 'rzsb', 'ygq'],  # [116, 5] 拼音缩写

    # ============ 课程领域 (4个状态) ============
    ['未开始', '进行中', '已结课', '已归档'],  # [117, 4] 中文
    ['not_started', 'ongoing', 'finished', 'archived'],  # [118, 4] 英文
    ['wait', 'running', 'done', 'archive'],  # [119, 4] 英文简写
    ['0', '1', '2', '3'],  # [120, 4] 数字
    ['weikaishi', 'jinxingzhong', 'yijieke', 'yiguidang'],  # [121, 4] 拼音
    ['wks', 'jxz', 'yjk', 'ygd'],  # [122, 4] 拼音缩写

    # ============ 活动领域 (5个状态) ============
    ['预告', '报名中', '进行中', '已结束', '已取消'],  # [123, 5] 中文
    ['preview', 'registration', 'ongoing', 'ended', 'cancelled'],  # [124, 5] 英文
    ['coming', 'signup', 'running', 'end', 'cancel'],  # [125, 5] 英文简写
    ['0', '1', '2', '3', '-1'],  # [126, 5] 数字
    ['yugao', 'baomingzhong', 'jinxingzhong', 'yijieshu', 'yiquxiao'],  # [127, 5] 拼音
    ['yg', 'bmz', 'jxz', 'yjs', 'yqx'],  # [128, 5] 拼音缩写

    # ============ 混合风格变体（约30个） ============
    # 状态码前缀风格
    ['STATUS_0', 'STATUS_1', 'STATUS_2', 'STATUS_3', 'STATUS_4'],  # [129, 5] 订单简化
    ['ST_PENDING', 'ST_PROCESSING', 'ST_COMPLETED', 'ST_CANCELLED'],  # [130, 4] 任务
    ['STATE_DRAFT', 'STATE_REVIEW', 'STATE_APPROVED', 'STATE_REJECTED'],  # [131, 4] 审批

    # 口语化中文
    ['等付钱', '付完了', '等发货', '发出去了', '收到了', '不要了'],  # [132, 6] 订单口语
    ['还没做', '正在做', '做完了', '关掉了'],  # [133, 4] 任务口语
    ['等批', '在批', '过了', '没过'],  # [134, 4] 审批口语

    # 混合中英文
    ['待支付pending', '已paid', 'to_ship发货', '已shipped', '已delivered', '已cancel'],  # [135, 6] 订单混合
    ['待处理todo', '进行ing', '已done', '已closed'],  # [136, 4] 任务混合
    ['草稿draft', '待审pending', '审批reviewing', '通过pass', '驳回reject'],  # [137, 5] 审批混合

    # 更多领域的混合变体
    ['会员active', '冻结frozen', '注销cancel', '拉黑blocked'],  # [138, 4] 会员混合
    ['在线online', '离线offline', '故障error', '维护fixing'],  # [139, 4] 设备混合
    ['未付unpaid', '支付中paying', '已付paid', '失败failed'],  # [140, 4] 支付混合

    # 数字前缀变体
    ['S0', 'S1', 'S2', 'S3', 'S4', 'S-1'],  # [141, 6] 短状态码
    ['0_待处理', '1_进行中', '2_已完成', '3_已关闭'],  # [142, 4] 数字+中文
    ['0_pending', '1_doing', '2_done', '3_closed'],  # [143, 4] 数字+英文

    # 更多领域的数字混合
    ['00', '01', '10', '11', '-1'],  # [144, 5] 二进制风格
    ['A0', 'A1', 'A2', 'A3', 'AX'],  # [145, 5] 字母+数字

    # 简短缩写（2-3字符）
    ['PD', 'PR', 'CM', 'CL'],  # [146, 4] 任务超短
    ['DR', 'RV', 'AP', 'RJ'],  # [147, 4] 审批超短
    ['ON', 'OF', 'ER', 'MN'],  # [148, 4] 设备超短

    # 大写拼音
    ['DAIZHIFU', 'YIZHIFU', 'DAIFAHUO', 'YIFAHUO'],  # [149, 4] 订单大写拼音
    ['DAICHULI', 'JINXINGZHONG', 'YIWANCHENG'],  # [150, 3] 任务大写拼音

    # 全小写英文
    ['draft', 'pending', 'approved', 'rejected'],  # [151, 4] 审批小写
    ['active', 'frozen', 'deleted'],  # [152, 3] 会员小写

    # 下划线风格
    ['PENDING_PAYMENT', 'PAID', 'PENDING_SHIP', 'SHIPPED'],  # [153, 4] 订单大写下划线
    ['todo_task', 'doing_task', 'done_task'],  # [154, 3] 任务下划线

    # 驼峰命名
    ['pendingPayment', 'paid', 'pendingShip', 'shipped'],  # [155, 4] 订单驼峰
    ['todoTask', 'inProgress', 'completed'],  # [156, 3] 任务驼峰

    # 更多粗细粒度变体
    ['新建', '处理', '完成'],  # [157, 3] 工单粗粒度
    ['待办', '在办', '办结'],  # [158, 3] 政务风格
    ['未审', '在审', '已审'],  # [159, 3] 审核粗粒度

    # 特殊符号风格（可能不实用但增加变体）
    ['[待支付]', '[已支付]', '[已发货]', '[已完成]'],  # [160, 4] 方括号
    ['<待处理>', '<进行中>', '<已完成>'],  # [161, 3] 尖括号
    ['(0)', '(1)', '(2)', '(3)'],  # [162, 4] 括号数字

    # 更多口语化
    ['还没付', '付好了', '等着发', '发走了', '拿到了'],  # [163, 5] 订单更口语
]


def states(num: int) -> list[str]:
    variant = random.choice(STATUS_VARIANTS)
    return [random.choice(variant) for _ in range(num)]
