"""
游戏状态管理类

管理Cookie Clicker的完整游戏状态，包括饼干、建筑物、升级、成就等
"""

import time
import copy
from typing import Dict, Set, Optional
from .constants import *


class GameState:
    """游戏状态类，存储所有游戏数据"""
    
    def __init__(self):
        # 基础饼干数据
        self.cookies = 0.0                    # 当前饼干数量
        self.cookies_earned = 0.0             # 本次运行总获得饼干数
        self.cookies_reset = 0.0              # 重置前累计饼干数
        self.cookies_per_second = 0.0         # 当前每秒饼干产量
        self.cookies_per_click = 1.0          # 每次点击获得饼干数
        
        # 点击相关
        self.cookie_clicks = 0                # 总点击次数
        self.handmade_cookies = 0.0           # 手动点击获得的饼干数
        
        # 建筑物数量 {building_name: amount}
        self.buildings = {}
        for name, _, _, _ in BUILDINGS_BASE_DATA:
            self.buildings[name] = 0
        
        # 建筑物等级 {building_name: level}
        self.building_levels = {}
        for name, _, _, _ in BUILDINGS_BASE_DATA:
            self.building_levels[name] = 0
        
        # 升级状态
        self.upgrades_owned = set()           # 已购买的升级
        self.upgrades_unlocked = set()        # 已解锁但未购买的升级
        
        # 成就系统
        self.achievements = set()             # 已获得的成就
        self.achievements_owned = 0           # 成就数量
        
        # 声望系统
        self.prestige = 0                     # 当前声望等级
        self.heavenly_chips = 0               # 天堂芯片总数
        self.heavenly_chips_spent = 0         # 已花费天堂芯片
        self.heavenly_power = 1.0             # 天堂力量倍数
        self.ascension_mode = 0               # 重生模式 (0=正常, 1=挑战)
        
        # 时间相关
        self.game_time = 0.0                  # 游戏总时间(秒)
        self.session_start = time.time()      # 本次会话开始时间
        self.last_update = time.time()        # 上次更新时间
        
        # 特殊系统状态
        self.season = ''                      # 当前季节
        self.season_time = 0                  # 季节剩余时间
        
        # 牛奶系统
        self.milk_progress = 0.0              # 牛奶进度
        self.milk_type = 0                    # 牛奶类型
        
        # 金饼干系统
        self.golden_cookies_clicked = 0       # 金饼干点击次数
        self.golden_cookies_missed = 0        # 错过的金饼干数
        self.last_golden_cookie = 0           # 上次金饼干时间
        
        # Buff系统
        self.buffs = {}                       # 当前生效的buff
        
        # 小游戏状态
        self.garden_unlocked = False          # 花园是否解锁
        self.grimoire_unlocked = False        # 魔法书是否解锁
        self.pantheon_unlocked = False        # 万神殿是否解锁
        
        # 花园状态
        self.garden_plants = {}               # 花园植物状态
        self.garden_soil = 0                  # 土壤类型
        
        # 万神殿状态
        self.pantheon_slots = [-1, -1, -1]    # 三个神灵槽位
        self.pantheon_swaps = 3               # 剩余交换次数
        
        # 魔法书状态
        self.magic_power = 0                  # 当前魔法值
        self.max_magic_power = 0              # 最大魔法值
        self.spells_cast = 0                  # 施法次数
        
        # 统计数据
        self.stats = {
            'buildings_owned': 0,
            'upgrades_owned': 0,
            'resets': 0,
            'playtime': 0.0
        }
    
    def copy(self):
        """创建游戏状态的深拷贝"""
        return copy.deepcopy(self)
    
    def get_total_buildings(self):
        """获取建筑物总数"""
        return sum(self.buildings.values())
    
    def get_building_count(self, building_name):
        """获取指定建筑物数量"""
        return self.buildings.get(building_name, 0)
    
    def add_building(self, building_name, amount=1):
        """增加建筑物数量"""
        if building_name in self.buildings:
            self.buildings[building_name] += amount
            self.stats['buildings_owned'] = self.get_total_buildings()
            return True
        return False
    
    def has_upgrade(self, upgrade_name):
        """检查是否拥有指定升级"""
        return upgrade_name in self.upgrades_owned
    
    def add_upgrade(self, upgrade_name):
        """添加升级"""
        self.upgrades_owned.add(upgrade_name)
        self.stats['upgrades_owned'] = len(self.upgrades_owned)
    
    def has_achievement(self, achievement_name):
        """检查是否拥有指定成就"""
        return achievement_name in self.achievements
    
    def add_achievement(self, achievement_name):
        """添加成就"""
        if achievement_name not in self.achievements:
            self.achievements.add(achievement_name)
            self.achievements_owned = len(self.achievements)
            self.update_milk_progress()
    
    def update_milk_progress(self):
        """更新牛奶进度"""
        self.milk_progress = self.achievements_owned / ACHIEVEMENTS_PER_MILK
        self.milk_type = min(int(self.milk_progress), 12)  # 最多12种牛奶
    
    def get_milk_multiplier(self):
        """获取牛奶CPS倍数"""
        if self.milk_progress <= 0:
            return 1.0
        
        # 基础牛奶效果: 每种牛奶+4% CPS
        base_mult = 1 + (self.milk_type * 0.04)
        
        # 小猫升级效果
        kitten_mult = 1.0
        if self.has_upgrade('Kitten helpers'):
            kitten_mult *= (1 + self.milk_progress * 0.05)
        if self.has_upgrade('Kitten workers'):
            kitten_mult *= (1 + self.milk_progress * 0.1)
        if self.has_upgrade('Kitten engineers'):
            kitten_mult *= (1 + self.milk_progress * 0.2)
        
        return base_mult * kitten_mult
    
    def earn_cookies(self, amount):
        """获得饼干"""
        self.cookies += amount
        self.cookies_earned += amount
    
    def spend_cookies(self, amount):
        """花费饼干"""
        if self.cookies >= amount:
            self.cookies -= amount
            return True
        return False
    
    def update_prestige(self):
        """更新声望等级"""
        total_cookies = self.cookies_reset + self.cookies_earned
        self.prestige = int(calculate_prestige(total_cookies))
    
    def get_prestige_multiplier(self):
        """获取声望CPS倍数"""
        if self.ascension_mode == 1:  # 挑战模式无声望加成
            return 1.0
        return 1 + (self.prestige * 0.01 * self.heavenly_power)
    
    def add_buff(self, buff_name, duration, effect):
        """添加buff效果"""
        self.buffs[buff_name] = {
            'duration': duration,
            'effect': effect,
            'start_time': self.game_time
        }
    
    def remove_buff(self, buff_name):
        """移除buff效果"""
        if buff_name in self.buffs:
            del self.buffs[buff_name]
    
    def update_buffs(self, dt):
        """更新buff状态"""
        expired_buffs = []
        for buff_name, buff_data in self.buffs.items():
            buff_data['duration'] -= dt
            if buff_data['duration'] <= 0:
                expired_buffs.append(buff_name)
        
        for buff_name in expired_buffs:
            self.remove_buff(buff_name)
    
    def get_active_buffs(self):
        """获取当前生效的buff列表"""
        return list(self.buffs.keys())
    
    def reset_for_ascension(self):
        """为重生重置游戏状态"""
        # 保存重置前数据
        self.cookies_reset += self.cookies_earned
        
        # 重置基础数据
        self.cookies = 0.0
        self.cookies_earned = 0.0
        self.cookies_per_second = 0.0
        self.cookie_clicks = 0
        self.handmade_cookies = 0.0
        
        # 重置建筑物
        for name in self.buildings:
            self.buildings[name] = 0
            self.building_levels[name] = 0
        
        # 重置升级(保留天堂升级)
        heavenly_upgrades = {u for u in self.upgrades_owned if 'heavenly' in u.lower()}
        self.upgrades_owned = heavenly_upgrades
        self.upgrades_unlocked.clear()
        
        # 重置buff
        self.buffs.clear()
        
        # 重置时间
        self.game_time = 0.0
        self.session_start = time.time()
        
        # 更新统计
        self.stats['resets'] += 1
        self.stats['buildings_owned'] = 0
        self.stats['upgrades_owned'] = len(self.upgrades_owned)
    
    def to_dict(self):
        """转换为字典格式(用于保存)"""
        return {
            'cookies': self.cookies,
            'cookies_earned': self.cookies_earned,
            'cookies_reset': self.cookies_reset,
            'buildings': self.buildings.copy(),
            'building_levels': self.building_levels.copy(),
            'upgrades_owned': list(self.upgrades_owned),
            'achievements': list(self.achievements),
            'prestige': self.prestige,
            'heavenly_chips': self.heavenly_chips,
            'heavenly_chips_spent': self.heavenly_chips_spent,
            'game_time': self.game_time,
            'stats': self.stats.copy()
        }
    
    def from_dict(self, data):
        """从字典格式加载(用于读取存档)"""
        self.cookies = data.get('cookies', 0.0)
        self.cookies_earned = data.get('cookies_earned', 0.0)
        self.cookies_reset = data.get('cookies_reset', 0.0)
        self.buildings.update(data.get('buildings', {}))
        self.building_levels.update(data.get('building_levels', {}))
        self.upgrades_owned = set(data.get('upgrades_owned', []))
        self.achievements = set(data.get('achievements', []))
        self.prestige = data.get('prestige', 0)
        self.heavenly_chips = data.get('heavenly_chips', 0)
        self.heavenly_chips_spent = data.get('heavenly_chips_spent', 0)
        self.game_time = data.get('game_time', 0.0)
        self.stats.update(data.get('stats', {}))
        
        # 更新派生数据
        self.achievements_owned = len(self.achievements)
        self.update_milk_progress()
        self.update_prestige()
    
    def __str__(self):
        """字符串表示"""
        return (f"GameState(cookies={self.cookies:.0f}, "
                f"cps={self.cookies_per_second:.1f}, "
                f"buildings={self.get_total_buildings()}, "
                f"prestige={self.prestige})")
    
    def __repr__(self):
        return self.__str__()
