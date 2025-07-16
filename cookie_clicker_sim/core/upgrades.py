"""
升级系统

定义Cookie Clicker中的所有升级类型和效果计算
"""

from typing import Dict, List, Optional, Callable, Any
from .constants import *


class Upgrade:
    """升级类"""
    
    def __init__(self, name: str, price: float, effect_type: str, 
                 effect_value: float, unlock_condition: Optional[Callable] = None,
                 description: str = "", icon_id: int = 0):
        self.name = name
        self.price = price
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.unlock_condition = unlock_condition
        self.description = description
        self.icon_id = icon_id
        
        # 状态
        self.unlocked = False
        self.bought = False
        
        # 特殊属性
        self.is_heavenly = False      # 是否为天堂升级
        self.is_debug = False         # 是否为调试升级
        self.is_seasonal = False      # 是否为季节升级
        self.building_target = None   # 目标建筑物(如果是建筑物专属升级)
    
    def check_unlock_condition(self, game_state) -> bool:
        """
        检查解锁条件
        """
        if self.unlock_condition is None:
            return True
        return self.unlock_condition(game_state)
    
    def can_afford(self, game_state) -> bool:
        """
        检查是否能够购买
        """
        if self.is_heavenly:
            return game_state.heavenly_chips >= self.price
        else:
            return game_state.cookies >= self.price
    
    def buy(self, game_state) -> bool:
        """
        购买升级
        """
        if not self.unlocked or self.bought:
            return False
        
        if not self.can_afford(game_state):
            return False
        
        if self.is_heavenly:
            game_state.heavenly_chips -= self.price
            game_state.heavenly_chips_spent += self.price
        else:
            game_state.spend_cookies(self.price)
        
        self.bought = True
        game_state.add_upgrade(self.name)
        return True
    
    def get_effect_description(self) -> str:
        """
        获取效果描述
        """
        if self.effect_type == UPGRADE_TYPES['CPS_MULT']:
            return f"+{self.effect_value*100:.0f}% CpS"
        elif self.effect_type == UPGRADE_TYPES['CLICK_MULT']:
            return f"+{self.effect_value*100:.0f}% click power"
        elif self.effect_type == UPGRADE_TYPES['BUILDING_MULT']:
            target = self.building_target or "buildings"
            return f"+{self.effect_value*100:.0f}% {target} CpS"
        elif self.effect_type == UPGRADE_TYPES['PRICE_REDUCTION']:
            return f"-{self.effect_value*100:.0f}% building prices"
        else:
            return self.description
    
    def __str__(self):
        return f"Upgrade({self.name}, {self.get_effect_description()})"
    
    def __repr__(self):
        return self.__str__()


# 升级数据定义
UPGRADES_DATA = [
    # 基础点击升级
    {
        'name': 'Reinforced index finger',
        'price': 100,
        'effect_type': UPGRADE_TYPES['CLICK_MULT'],
        'effect_value': 1.0,  # +100% = 2倍
        'unlock_condition': lambda gs: gs.cookie_clicks >= 15,
        'description': 'The mouse and cursors are twice as efficient.'
    },
    {
        'name': 'Carpal tunnel prevention cream',
        'price': 500,
        'effect_type': UPGRADE_TYPES['CLICK_MULT'], 
        'effect_value': 1.0,
        'unlock_condition': lambda gs: gs.cookie_clicks >= 100,
        'description': 'The mouse and cursors are twice as efficient.'
    },
    {
        'name': 'Ambidextrous',
        'price': 10000,
        'effect_type': UPGRADE_TYPES['CLICK_MULT'],
        'effect_value': 1.0,
        'unlock_condition': lambda gs: gs.cookie_clicks >= 1000,
        'description': 'The mouse and cursors are twice as efficient.'
    },
    
    # 奶奶升级
    {
        'name': 'Forwards from grandma',
        'price': 1000,
        'effect_type': UPGRADE_TYPES['BUILDING_MULT'],
        'effect_value': 1.0,
        'building_target': 'Grandma',
        'unlock_condition': lambda gs: gs.get_building_count('Grandma') >= 1,
        'description': 'Grandmas are twice as efficient.'
    },
    {
        'name': 'Steel-plated rolling pins',
        'price': 5000,
        'effect_type': UPGRADE_TYPES['BUILDING_MULT'],
        'effect_value': 1.0,
        'building_target': 'Grandma',
        'unlock_condition': lambda gs: gs.get_building_count('Grandma') >= 5,
        'description': 'Grandmas are twice as efficient.'
    },
    {
        'name': 'Lubricated dentures',
        'price': 50000,
        'effect_type': UPGRADE_TYPES['BUILDING_MULT'],
        'effect_value': 1.0,
        'building_target': 'Grandma',
        'unlock_condition': lambda gs: gs.get_building_count('Grandma') >= 25,
        'description': 'Grandmas are twice as efficient.'
    },
    
    # 农场升级
    {
        'name': 'Cheap hoes',
        'price': 11000,
        'effect_type': UPGRADE_TYPES['BUILDING_MULT'],
        'effect_value': 1.0,
        'building_target': 'Farm',
        'unlock_condition': lambda gs: gs.get_building_count('Farm') >= 1,
        'description': 'Farms are twice as efficient.'
    },
    {
        'name': 'Fertilizer',
        'price': 55000,
        'effect_type': UPGRADE_TYPES['BUILDING_MULT'],
        'effect_value': 1.0,
        'building_target': 'Farm',
        'unlock_condition': lambda gs: gs.get_building_count('Farm') >= 5,
        'description': 'Farms are twice as efficient.'
    },
    {
        'name': 'Cookie trees',
        'price': 550000,
        'effect_type': UPGRADE_TYPES['BUILDING_MULT'],
        'effect_value': 1.0,
        'building_target': 'Farm',
        'unlock_condition': lambda gs: gs.get_building_count('Farm') >= 25,
        'description': 'Farms are twice as efficient.'
    },
    
    # 牛奶升级
    {
        'name': 'Kitten helpers',
        'price': 9000000,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 0.05,
        'unlock_condition': lambda gs: gs.milk_progress >= 0.5,
        'description': 'You gain more CpS the more milk you have.'
    },
    {
        'name': 'Kitten workers',
        'price': 9000000000,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 0.1,
        'unlock_condition': lambda gs: gs.milk_progress >= 1.0,
        'description': 'You gain more CpS the more milk you have.'
    },
    {
        'name': 'Kitten engineers',
        'price': 9000000000000,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 0.2,
        'unlock_condition': lambda gs: gs.milk_progress >= 2.0,
        'description': 'You gain more CpS the more milk you have.'
    },
    
    # 天堂升级
    {
        'name': 'Heavenly chip secret',
        'price': 1,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 0.05,
        'is_heavenly': True,
        'description': 'Heavenly chips are 5% more powerful.'
    },
    {
        'name': 'Heavenly cookie stand',
        'price': 3,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 0.20,
        'is_heavenly': True,
        'unlock_condition': lambda gs: gs.has_upgrade('Heavenly chip secret'),
        'description': 'Heavenly chips are 20% more powerful.'
    },
    {
        'name': 'Heavenly bakery',
        'price': 10,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 0.25,
        'is_heavenly': True,
        'unlock_condition': lambda gs: gs.has_upgrade('Heavenly cookie stand'),
        'description': 'Heavenly chips are 25% more powerful.'
    },
    
    # 特殊升级
    {
        'name': 'Lucky day',
        'price': 777777777,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 1.0,
        'unlock_condition': lambda gs: gs.golden_cookies_clicked >= 7,
        'description': 'Golden cookies appear twice as often and last twice as long.'
    },
    {
        'name': 'Serendipity',
        'price': 77777777777,
        'effect_type': UPGRADE_TYPES['SPECIAL'],
        'effect_value': 1.0,
        'unlock_condition': lambda gs: gs.golden_cookies_clicked >= 27,
        'description': 'Golden cookies appear twice as often and last twice as long.'
    }
]


# 创建升级实例
UPGRADES: Dict[str, Upgrade] = {}

def initialize_upgrades():
    """初始化所有升级"""
    global UPGRADES
    
    for upgrade_data in UPGRADES_DATA:
        upgrade = Upgrade(
            name=upgrade_data['name'],
            price=upgrade_data['price'],
            effect_type=upgrade_data['effect_type'],
            effect_value=upgrade_data['effect_value'],
            unlock_condition=upgrade_data.get('unlock_condition'),
            description=upgrade_data['description']
        )
        
        # 设置特殊属性
        upgrade.is_heavenly = upgrade_data.get('is_heavenly', False)
        upgrade.building_target = upgrade_data.get('building_target')
        
        UPGRADES[upgrade.name] = upgrade

# 初始化升级
initialize_upgrades()


class UpgradeManager:
    """升级管理器"""
    
    def __init__(self, game_state):
        self.game_state = game_state
    
    def update_unlocks(self):
        """
        更新升级解锁状态
        """
        for upgrade in UPGRADES.values():
            if not upgrade.unlocked and not upgrade.bought:
                if upgrade.check_unlock_condition(self.game_state):
                    upgrade.unlocked = True
                    self.game_state.upgrades_unlocked.add(upgrade.name)
    
    def buy_upgrade(self, upgrade_name: str) -> bool:
        """
        购买升级
        """
        if upgrade_name not in UPGRADES:
            return False
        
        upgrade = UPGRADES[upgrade_name]
        return upgrade.buy(self.game_state)
    
    def get_available_upgrades(self) -> List[str]:
        """
        获取可购买的升级列表
        """
        available = []
        for upgrade_name, upgrade in UPGRADES.items():
            if upgrade.unlocked and not upgrade.bought:
                available.append(upgrade_name)
        return available
    
    def get_affordable_upgrades(self) -> List[str]:
        """
        获取买得起的升级列表
        """
        affordable = []
        for upgrade_name, upgrade in UPGRADES.items():
            if (upgrade.unlocked and not upgrade.bought and 
                upgrade.can_afford(self.game_state)):
                affordable.append(upgrade_name)
        return affordable
    
    def get_upgrade_info(self, upgrade_name: str) -> Optional[Dict]:
        """
        获取升级详细信息
        """
        if upgrade_name not in UPGRADES:
            return None
        
        upgrade = UPGRADES[upgrade_name]
        return {
            'name': upgrade.name,
            'price': upgrade.price,
            'description': upgrade.description,
            'effect_description': upgrade.get_effect_description(),
            'unlocked': upgrade.unlocked,
            'bought': upgrade.bought,
            'can_afford': upgrade.can_afford(self.game_state),
            'is_heavenly': upgrade.is_heavenly
        }
    
    def get_most_efficient_upgrade(self) -> Optional[str]:
        """
        获取效率最高的升级
        """
        # 简化实现：优先购买便宜的升级
        affordable = self.get_affordable_upgrades()
        if not affordable:
            return None
        
        # 按价格排序，优先购买便宜的
        affordable_upgrades = [(name, UPGRADES[name].price) for name in affordable]
        affordable_upgrades.sort(key=lambda x: x[1])
        
        return affordable_upgrades[0][0]
    
    def calculate_upgrade_value(self, upgrade_name: str) -> float:
        """
        计算升级的价值 (CPS提升/价格)
        """
        if upgrade_name not in UPGRADES:
            return 0.0
        
        upgrade = UPGRADES[upgrade_name]
        
        # 简化计算：根据升级类型估算价值
        if upgrade.effect_type == UPGRADE_TYPES['CPS_MULT']:
            current_cps = self.game_state.cookies_per_second
            cps_increase = current_cps * upgrade.effect_value
            return cps_increase / upgrade.price
        elif upgrade.effect_type == UPGRADE_TYPES['BUILDING_MULT']:
            # 计算特定建筑物的CPS提升
            if upgrade.building_target:
                from .buildings import BUILDINGS
                building = BUILDINGS.get(upgrade.building_target)
                if building:
                    amount = self.game_state.get_building_count(upgrade.building_target)
                    current_building_cps = building.get_cps_contribution(amount, self.game_state)
                    cps_increase = current_building_cps * upgrade.effect_value
                    return cps_increase / upgrade.price
        
        # 其他类型升级的价值较难量化，返回固定值
        return 1.0 / upgrade.price
