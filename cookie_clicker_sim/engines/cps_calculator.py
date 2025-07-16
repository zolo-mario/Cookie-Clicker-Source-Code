"""
CPS计算引擎

负责计算Cookie Clicker中的每秒饼干产量(CPS)
"""

from typing import Dict, List
from ..core.game_state import GameState
from ..core.buildings import BUILDINGS, BuildingManager
from ..core.upgrades import UPGRADES
from ..core.constants import *


class CPSCalculator:
    """CPS计算器"""
    
    def __init__(self):
        self.cache = {}  # 缓存计算结果
        self.cache_valid = False
    
    def calculate_total_cps(self, game_state: GameState) -> float:
        """
        计算总CPS
        """
        # 检查缓存
        cache_key = self._get_cache_key(game_state)
        if self.cache_valid and cache_key in self.cache:
            return self.cache[cache_key]
        
        total_cps = 0.0
        
        # 1. 建筑物CPS
        building_cps = self._calculate_buildings_cps(game_state)
        total_cps += building_cps
        
        # 2. 特殊CPS来源
        special_cps = self._calculate_special_cps(game_state)
        total_cps += special_cps
        
        # 3. 应用全局倍数
        global_multiplier = self._calculate_global_multiplier(game_state)
        total_cps *= global_multiplier
        
        # 4. 应用buff效果
        buff_multiplier = self._calculate_buff_multiplier(game_state)
        total_cps *= buff_multiplier
        
        # 缓存结果
        self.cache[cache_key] = total_cps
        self.cache_valid = True
        
        return total_cps
    
    def _calculate_buildings_cps(self, game_state: GameState) -> float:
        """
        计算所有建筑物的CPS贡献
        """
        building_manager = BuildingManager(game_state)
        return building_manager.calculate_total_cps()
    
    def _calculate_special_cps(self, game_state: GameState) -> float:
        """
        计算特殊CPS来源
        """
        special_cps = 0.0
        
        # "egg"升级 (隐藏升级)
        if game_state.has_upgrade('"egg"'):
            special_cps += 9
        
        # 其他特殊CPS来源可以在这里添加
        
        return special_cps
    
    def _calculate_global_multiplier(self, game_state: GameState) -> float:
        """
        计算全局CPS倍数
        """
        multiplier = 1.0
        
        # 1. 声望倍数
        multiplier *= game_state.get_prestige_multiplier()
        
        # 2. 牛奶倍数
        multiplier *= game_state.get_milk_multiplier()
        
        # 3. 升级倍数
        multiplier *= self._calculate_upgrade_multiplier(game_state)
        
        # 4. 季节倍数
        multiplier *= self._calculate_season_multiplier(game_state)
        
        # 5. 龙系统倍数
        multiplier *= self._calculate_dragon_multiplier(game_state)
        
        # 6. 万神殿倍数
        multiplier *= self._calculate_pantheon_multiplier(game_state)
        
        # 7. 花园倍数
        multiplier *= self._calculate_garden_multiplier(game_state)
        
        return multiplier
    
    def _calculate_upgrade_multiplier(self, game_state: GameState) -> float:
        """
        计算升级带来的CPS倍数
        """
        multiplier = 1.0
        
        # 通用CPS升级
        cps_upgrades = [
            ('Specialized chocolate chips', 1.01),
            ('Designer cocoa beans', 1.02),
            ('Underworld ovens', 1.03),
            ('Exotic nuts', 1.04),
            ('Arcane sugar', 1.05),
        ]
        
        for upgrade_name, mult in cps_upgrades:
            if game_state.has_upgrade(upgrade_name):
                multiplier *= mult
        
        # 圣诞节升级
        if game_state.has_upgrade('Increased merriness'):
            multiplier *= 1.15
        if game_state.has_upgrade('Improved jolliness'):
            multiplier *= 1.15
        if game_state.has_upgrade('A lump of coal'):
            multiplier *= 1.01
        if game_state.has_upgrade('An itchy sweater'):
            multiplier *= 1.01
        if game_state.has_upgrade("Santa's dominion"):
            multiplier *= 1.2
        
        # 幸运饼干升级
        if game_state.has_upgrade('Fortune #100'):
            multiplier *= 1.01
        if game_state.has_upgrade('Fortune #101'):
            multiplier *= 1.07
        
        # 圣诞老人等级加成
        if game_state.has_upgrade("Santa's legacy"):
            santa_level = getattr(game_state, 'santa_level', 0)
            multiplier *= (1 + (santa_level + 1) * 0.03)
        
        return multiplier
    
    def _calculate_season_multiplier(self, game_state: GameState) -> float:
        """
        计算季节效果倍数
        """
        multiplier = 1.0
        
        if game_state.season in SEASONS:
            season_data = SEASONS[game_state.season]
            if 'cps_mult' in season_data['effects']:
                multiplier *= season_data['effects']['cps_mult']
        
        return multiplier
    
    def _calculate_dragon_multiplier(self, game_state: GameState) -> float:
        """
        计算龙系统倍数
        """
        multiplier = 1.0
        
        # TODO: 实现龙系统
        # 这里可以添加龙光环的CPS效果
        
        return multiplier
    
    def _calculate_pantheon_multiplier(self, game_state: GameState) -> float:
        """
        计算万神殿倍数
        """
        multiplier = 1.0
        
        # 禁欲主义神灵 (Holobore)
        if hasattr(game_state, 'pantheon_slots'):
            for i, god_id in enumerate(game_state.pantheon_slots):
                if god_id == 0:  # Holobore的ID
                    if i == 0:    # 钻石槽位
                        multiplier *= 1.15
                    elif i == 1:  # 红宝石槽位
                        multiplier *= 1.10
                    elif i == 2:  # 翡翠槽位
                        multiplier *= 1.05
        
        return multiplier
    
    def _calculate_garden_multiplier(self, game_state: GameState) -> float:
        """
        计算花园效果倍数
        """
        multiplier = 1.0
        
        # TODO: 实现花园系统
        # 这里可以添加植物的CPS效果
        
        return multiplier
    
    def _calculate_buff_multiplier(self, game_state: GameState) -> float:
        """
        计算buff效果倍数
        """
        multiplier = 1.0
        
        # Frenzy效果
        if 'frenzy' in game_state.buffs:
            multiplier *= 7.0
        
        # Elder Frenzy效果
        if 'elder_frenzy' in game_state.buffs:
            multiplier *= 666.0
        
        # Clot效果 (负面buff)
        if 'clot' in game_state.buffs:
            multiplier *= 0.5
        
        # 其他buff效果
        for buff_name, buff_data in game_state.buffs.items():
            if 'cps_mult' in buff_data.get('effect', {}):
                multiplier *= buff_data['effect']['cps_mult']
        
        return multiplier
    
    def calculate_click_power(self, game_state: GameState) -> float:
        """
        计算点击力量
        """
        # 基础点击力量
        click_power = 1.0
        
        # 光标建筑物加成
        cursor_count = game_state.get_building_count('Cursor')
        if cursor_count > 0:
            cursor_building = BUILDINGS['Cursor']
            cursor_cps = cursor_building.get_cps_contribution(cursor_count, game_state)
            click_power += cursor_cps
        
        # 点击升级倍数
        click_multiplier = self._calculate_click_multiplier(game_state)
        click_power *= click_multiplier
        
        # buff效果
        if 'click_frenzy' in game_state.buffs:
            click_power *= 777.0
        if 'dragonflight' in game_state.buffs:
            click_power *= 1111.0
        
        return click_power
    
    def _calculate_click_multiplier(self, game_state: GameState) -> float:
        """
        计算点击倍数
        """
        multiplier = 1.0
        
        # 点击升级
        click_upgrades = [
            'Reinforced index finger',
            'Carpal tunnel prevention cream', 
            'Ambidextrous',
            'Thousand fingers',
            'Million fingers',
            'Billion fingers',
            'Trillion fingers'
        ]
        
        for upgrade_name in click_upgrades:
            if game_state.has_upgrade(upgrade_name):
                multiplier *= 2.0  # 大多数点击升级都是2倍
        
        return multiplier
    
    def _get_cache_key(self, game_state: GameState) -> str:
        """
        生成缓存键
        """
        # 简化的缓存键，实际应该包含所有影响CPS的因素
        key_parts = [
            str(game_state.buildings),
            str(game_state.upgrades_owned),
            str(game_state.prestige),
            str(game_state.milk_progress),
            str(game_state.buffs.keys())
        ]
        return '|'.join(key_parts)
    
    def invalidate_cache(self):
        """
        使缓存失效
        """
        self.cache.clear()
        self.cache_valid = False
    
    def get_cps_breakdown(self, game_state: GameState) -> Dict[str, float]:
        """
        获取CPS详细分解
        """
        breakdown = {}
        
        # 建筑物CPS
        for building_name, building in BUILDINGS.items():
            amount = game_state.get_building_count(building_name)
            if amount > 0:
                cps = building.get_cps_contribution(amount, game_state)
                breakdown[building_name] = cps
        
        # 特殊CPS
        special_cps = self._calculate_special_cps(game_state)
        if special_cps > 0:
            breakdown['Special'] = special_cps
        
        # 全局倍数
        global_mult = self._calculate_global_multiplier(game_state)
        breakdown['Global Multiplier'] = global_mult
        
        # Buff倍数
        buff_mult = self._calculate_buff_multiplier(game_state)
        if buff_mult != 1.0:
            breakdown['Buff Multiplier'] = buff_mult
        
        return breakdown
