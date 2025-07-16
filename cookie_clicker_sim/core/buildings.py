"""
建筑物系统

定义Cookie Clicker中的所有建筑物类型和相关计算
"""

import math
from typing import Dict, List, Optional
from .constants import *


class Building:
    """建筑物类"""
    
    def __init__(self, name: str, base_price: float, base_cps: float, 
                 icon_id: int = 0, price_multiplier: float = BUILDING_PRICE_MULTIPLIER):
        self.name = name
        self.base_price = base_price
        self.base_cps = base_cps
        self.icon_id = icon_id
        self.price_multiplier = price_multiplier
        
        # 建筑物特殊属性
        self.grandma_synergy = False  # 是否与奶奶有协同效应
        self.special_upgrades = []    # 专属升级列表
        self.unlock_condition = None  # 解锁条件
        
    def get_price(self, current_amount: int) -> float:
        """
        计算购买下一个建筑物的价格
        公式: base_price * (price_multiplier ^ current_amount)
        """
        return self.base_price * (self.price_multiplier ** current_amount)
    
    def get_bulk_price(self, current_amount: int, buy_amount: int) -> float:
        """
        计算批量购买的总价格
        """
        total_price = 0.0
        for i in range(buy_amount):
            total_price += self.get_price(current_amount + i)
        return total_price
    
    def get_cps_contribution(self, amount: int, game_state) -> float:
        """
        计算建筑物的CPS贡献
        """
        if amount <= 0:
            return 0.0
        
        # 基础CPS
        base_cps = self.base_cps * amount
        
        # 应用各种倍数
        multiplier = self.get_total_multiplier(game_state)
        
        return base_cps * multiplier
    
    def get_total_multiplier(self, game_state) -> float:
        """
        计算建筑物的总倍数
        """
        multiplier = 1.0
        
        # 建筑物等级加成 (每级+1%)
        building_level = game_state.building_levels.get(self.name, 0)
        if building_level > 0:
            multiplier *= (1 + building_level * 0.01)
        
        # 升级倍数
        multiplier *= self.get_upgrade_multiplier(game_state)
        
        # 奶奶协同效应
        if self.grandma_synergy:
            multiplier *= self.get_grandma_synergy_multiplier(game_state)
        
        # 牛奶倍数 (对所有建筑物)
        multiplier *= game_state.get_milk_multiplier()
        
        # 声望倍数
        multiplier *= game_state.get_prestige_multiplier()
        
        # 特殊建筑物倍数
        multiplier *= self.get_special_multiplier(game_state)
        
        return multiplier
    
    def get_upgrade_multiplier(self, game_state) -> float:
        """
        计算升级带来的倍数
        """
        multiplier = 1.0
        
        # 通用升级
        if game_state.has_upgrade('Forwards from grandma'):
            multiplier *= 2.0
        if game_state.has_upgrade('Steel-plated rolling pins'):
            multiplier *= 2.0
        if game_state.has_upgrade('Lubricated dentures'):
            multiplier *= 2.0
        
        # 建筑物专属升级
        building_upgrades = self.get_building_specific_upgrades()
        for upgrade_name in building_upgrades:
            if game_state.has_upgrade(upgrade_name):
                multiplier *= 2.0  # 大多数建筑物升级都是2倍
        
        return multiplier
    
    def get_grandma_synergy_multiplier(self, game_state) -> float:
        """
        计算与奶奶的协同效应倍数
        """
        if not self.grandma_synergy:
            return 1.0
        
        grandma_count = game_state.get_building_count('Grandma')
        if grandma_count <= 0:
            return 1.0
        
        # 每个奶奶提供1%的协同加成
        return 1 + (grandma_count * 0.01)
    
    def get_special_multiplier(self, game_state) -> float:
        """
        计算特殊倍数 (龙系统、万神殿等)
        """
        multiplier = 1.0
        
        # 龙系统光环效果
        # TODO: 实现龙系统
        
        # 万神殿效果
        # TODO: 实现万神殿系统
        
        # 花园效果
        # TODO: 实现花园系统
        
        return multiplier
    
    def get_building_specific_upgrades(self) -> List[str]:
        """
        获取建筑物专属升级列表
        """
        # 这里简化处理，实际应该从升级数据库中查询
        upgrades_map = {
            'Cursor': ['Reinforced index finger', 'Carpal tunnel prevention cream', 'Ambidextrous'],
            'Grandma': ['Forwards from grandma', 'Steel-plated rolling pins', 'Lubricated dentures'],
            'Farm': ['Cheap hoes', 'Fertilizer', 'Cookie trees'],
            'Mine': ['Sugar gas', 'Megadrill', 'Ultradrill'],
            'Factory': ['Sturdier conveyor belts', 'Child labor', 'Sweatshop'],
            'Bank': ['Taller tellers', 'Scissor-resistant credit cards', 'Acid-proof vaults'],
            'Temple': ['Golden idols', 'Sacrifices', 'Delicious blessing'],
            'Wizard tower': ['Pointier hats', 'Beardlier beards', 'Ancient grimoires'],
            'Shipment': ['Vanilla nebulae', 'Wormholes', 'Frequent flyer'],
            'Alchemy lab': ['Antimony', 'Essence of dough', 'True chocolate'],
            'Portal': ['Ancient tablet', 'Insane oatling workers', 'Soul bond'],
            'Time machine': ['Flux capacitors', 'Time paradox resolver', 'Quantum conundrum'],
            'Antimatter condenser': ['Sugar bosons', 'String theory', 'Large macaron collider'],
            'Prism': ['Gem polish', 'Ninth color', 'Chocolate light'],
            'Chancemaker': ['Your lucky cookie', 'All-natural clovers', 'Leprechaun village'],
            'Fractal engine': ['Metabakeries', 'Mandelbrot cake', 'Fractoids']
        }
        return upgrades_map.get(self.name, [])
    
    def get_efficiency(self, current_amount: int, game_state) -> float:
        """
        计算购买效率 (CPS增长 / 价格)
        """
        price = self.get_price(current_amount)
        current_cps = self.get_cps_contribution(current_amount, game_state)
        new_cps = self.get_cps_contribution(current_amount + 1, game_state)
        cps_increase = new_cps - current_cps
        
        return cps_increase / price if price > 0 else 0.0
    
    def can_afford(self, current_amount: int, cookies: float) -> bool:
        """
        检查是否能够购买
        """
        return cookies >= self.get_price(current_amount)
    
    def __str__(self):
        return f"Building({self.name}, price={self.base_price}, cps={self.base_cps})"
    
    def __repr__(self):
        return self.__str__()


# 创建所有建筑物实例
BUILDINGS: Dict[str, Building] = {}

def initialize_buildings():
    """初始化所有建筑物"""
    global BUILDINGS
    
    for i, (name, base_price, base_cps, icon_id) in enumerate(BUILDINGS_BASE_DATA):
        building = Building(name, base_price, base_cps, icon_id)
        
        # 设置特殊属性
        if name != 'Cursor' and name != 'Grandma':
            building.grandma_synergy = True
        
        BUILDINGS[name] = building

# 初始化建筑物
initialize_buildings()


class BuildingManager:
    """建筑物管理器"""
    
    def __init__(self, game_state):
        self.game_state = game_state
    
    def buy_building(self, building_name: str, amount: int = 1) -> bool:
        """
        购买建筑物
        """
        if building_name not in BUILDINGS:
            return False
        
        building = BUILDINGS[building_name]
        current_amount = self.game_state.get_building_count(building_name)
        total_price = building.get_bulk_price(current_amount, amount)
        
        if self.game_state.spend_cookies(total_price):
            self.game_state.add_building(building_name, amount)
            return True
        
        return False
    
    def get_building_info(self, building_name: str) -> Optional[Dict]:
        """
        获取建筑物详细信息
        """
        if building_name not in BUILDINGS:
            return None
        
        building = BUILDINGS[building_name]
        current_amount = self.game_state.get_building_count(building_name)
        
        return {
            'name': building.name,
            'amount': current_amount,
            'price': building.get_price(current_amount),
            'cps': building.get_cps_contribution(current_amount, self.game_state),
            'efficiency': building.get_efficiency(current_amount, self.game_state),
            'can_afford': building.can_afford(current_amount, self.game_state.cookies)
        }
    
    def get_all_buildings_info(self) -> Dict[str, Dict]:
        """
        获取所有建筑物信息
        """
        return {name: self.get_building_info(name) for name in BUILDINGS.keys()}
    
    def get_most_efficient_building(self) -> Optional[str]:
        """
        获取效率最高的建筑物
        """
        best_building = None
        best_efficiency = 0.0
        
        for building_name in BUILDINGS.keys():
            building = BUILDINGS[building_name]
            current_amount = self.game_state.get_building_count(building_name)
            
            if building.can_afford(current_amount, self.game_state.cookies):
                efficiency = building.get_efficiency(current_amount, self.game_state)
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_building = building_name
        
        return best_building
    
    def calculate_total_cps(self) -> float:
        """
        计算所有建筑物的总CPS
        """
        total_cps = 0.0
        
        for building_name, building in BUILDINGS.items():
            amount = self.game_state.get_building_count(building_name)
            cps = building.get_cps_contribution(amount, self.game_state)
            total_cps += cps
        
        return total_cps
