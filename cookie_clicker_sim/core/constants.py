"""
游戏数值常数定义

基于Cookie Clicker源码分析的精确数值常数
"""

import math

# 声望系统常数
HC_FACTOR = 3  # 天堂芯片因子
PRESTIGE_BASE = 1_000_000_000_000  # 声望计算基数 (1万亿)

# 建筑物价格增长率
BUILDING_PRICE_MULTIPLIER = 1.15

# 牛奶系统
ACHIEVEMENTS_PER_MILK = 25  # 每25个成就解锁一种牛奶

# 金饼干系统
GOLDEN_COOKIE_BASE_FREQ = 5 * 60  # 基础5分钟间隔
GOLDEN_COOKIE_FREQ_VAR = 10 * 60  # 最大10分钟变化

# 建筑物基础数据 (基于源码分析)
BUILDINGS_BASE_DATA = [
    # (name, base_price, base_cps, icon_id)
    ('Cursor', 15, 0.1, 0),
    ('Grandma', 100, 1.0, 1), 
    ('Farm', 1100, 8.0, 2),
    ('Mine', 12000, 47.0, 3),
    ('Factory', 130000, 260.0, 4),
    ('Bank', 1400000, 1400.0, 5),
    ('Temple', 20000000, 7800.0, 6),
    ('Wizard tower', 330000000, 44000.0, 7),
    ('Shipment', 5100000000, 260000.0, 8),
    ('Alchemy lab', 75000000000, 1600000.0, 9),
    ('Portal', 1000000000000, 10000000.0, 10),
    ('Time machine', 14000000000000, 65000000.0, 11),
    ('Antimatter condenser', 170000000000000, 430000000.0, 12),
    ('Prism', 2100000000000000, 2900000000.0, 13),
    ('Chancemaker', 26000000000000000, 21000000000.0, 14),
    ('Fractal engine', 310000000000000000, 150000000000.0, 15),
]

def calculate_building_base_cps(building_index):
    """
    根据建筑物索引计算基础CPS
    基于源码公式: Math.ceil((Math.pow(n*1,n*0.5+2))*10)/10
    """
    n = building_index
    if n == 0:  # Cursor特殊处理
        return 0.1
    
    base_cps = math.ceil((n ** (n * 0.5 + 2)) * 10) / 10
    
    # 数值修正 (源码中的digits处理)
    digits = 10 ** (math.ceil(math.log10(math.ceil(base_cps)))) / 100
    base_cps = round(base_cps / digits) * digits
    
    return base_cps

def calculate_building_base_price(building_index):
    """
    根据建筑物索引计算基础价格
    基于源码公式: (n+9+(n<5?0:Math.pow(n-5,1.75)*5))*Math.pow(10,n)*(Math.max(1,n-14))
    """
    n = building_index
    
    base = n + 9
    if n >= 5:
        base += ((n - 5) ** 1.75) * 5
    
    price = base * (10 ** n) * max(1, n - 14)
    return price

def calculate_prestige(cookies_reset):
    """
    计算声望等级
    公式: Math.pow(cookies/1000000000000, 1/3)
    """
    return (cookies_reset / PRESTIGE_BASE) ** (1 / HC_FACTOR)

def calculate_cookies_for_prestige(prestige_level):
    """
    计算达到指定声望等级需要的饼干数
    """
    return (prestige_level ** HC_FACTOR) * PRESTIGE_BASE

# 升级效果类型
UPGRADE_TYPES = {
    'CPS_MULT': 'cps_multiplier',      # CPS倍数
    'CLICK_MULT': 'click_multiplier',   # 点击倍数
    'BUILDING_MULT': 'building_multiplier',  # 建筑物倍数
    'PRICE_REDUCTION': 'price_reduction',    # 价格减少
    'SPECIAL': 'special_effect'         # 特殊效果
}

# 成就类型
ACHIEVEMENT_TYPES = {
    'COOKIES_BAKED': 'cookies_baked',
    'COOKIES_EARNED': 'cookies_earned', 
    'BUILDING_COUNT': 'building_count',
    'CLICK_COUNT': 'click_count',
    'GOLDEN_COOKIES': 'golden_cookies',
    'SPECIAL': 'special'
}

# 季节系统
SEASONS = {
    'christmas': {
        'name': 'Christmas',
        'duration': 24 * 60 * 60,  # 24小时
        'effects': {'cps_mult': 1.02}
    },
    'halloween': {
        'name': 'Halloween', 
        'duration': 24 * 60 * 60,
        'effects': {'golden_freq': 1.1}
    },
    'easter': {
        'name': 'Easter',
        'duration': 24 * 60 * 60, 
        'effects': {'click_mult': 1.02}
    },
    'valentines': {
        'name': 'Valentines',
        'duration': 24 * 60 * 60,
        'effects': {'cps_mult': 1.01}
    }
}

# 龙系统光环效果
DRAGON_AURAS = {
    'breath_of_milk': {'milk_mult': 1.05},
    'dragon_cursor': {'cursor_mult': 1.05},
    'elder_battalion': {'grandma_mult': 1.01},
    'reaper_of_fields': {'golden_cookies': 1.03},
    'season_switcher': {'season_effects': True},
    'dragonflight': {'click_mult': 1.03, 'golden_freq': 1.1},
    'reality_bending': {'random_effects': True},
    'milk_selector': {'milk_choice': True},
    'supreme_intellect': {'brain_effects': True}
}

# 万神殿神灵效果
PANTHEON_GODS = {
    'holobore': {  # 禁欲主义
        'slot1': {'cps_mult': 1.15},
        'slot2': {'cps_mult': 1.10}, 
        'slot3': {'cps_mult': 1.05}
    },
    'vomitrax': {  # 贪婪
        'slot1': {'building_cost_mult': 0.93, 'upgrade_cost_mult': 0.93},
        'slot2': {'building_cost_mult': 0.95, 'upgrade_cost_mult': 0.95},
        'slot3': {'building_cost_mult': 0.98, 'upgrade_cost_mult': 0.98}
    },
    'godzamok': {  # 毁灭
        'slot1': {'click_mult_per_building_sold': 1.15},
        'slot2': {'click_mult_per_building_sold': 1.10},
        'slot3': {'click_mult_per_building_sold': 1.05}
    }
}

# 花园植物效果
GARDEN_PLANTS = {
    'bakerWheat': {'cps_mult': 1.01},
    'thumbcorn': {'click_mult': 1.02},
    'cronerice': {'grandma_mult': 1.03},
    'gildmillet': {'golden_mult': 1.01, 'golden_dur': 1.001},
    'clover': {'golden_freq': 1.01},
    'goldenClover': {'golden_freq': 1.03},
    'shimmerlily': {'golden_mult': 1.01, 'golden_freq': 1.01},
    'elderwort': {'wrath_mult': 1.01, 'wrath_freq': 1.01, 'grandma_mult': 1.01}
}

# 魔法书法术
GRIMOIRE_SPELLS = {
    'conjure_baked_goods': {
        'name': 'Conjure Baked Goods',
        'cost_min': 2,
        'cost_percent': 0.4,
        'effect': 'summon_cookies'
    },
    'hand_of_fate': {
        'name': 'Hand of Fate', 
        'cost_min': 10,
        'cost_percent': 0.6,
        'effect': 'force_golden_cookie'
    },
    'stretch_time': {
        'name': 'Stretch Time',
        'cost_min': 8,
        'cost_percent': 0.2,
        'effect': 'extend_buffs'
    }
}
