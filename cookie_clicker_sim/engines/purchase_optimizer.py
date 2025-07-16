"""
购买优化引擎

负责分析最优的购买策略，包括建筑物和升级的效率计算
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from ..core.game_state import GameState
from ..core.buildings import BUILDINGS, BuildingManager
from ..core.upgrades import UPGRADES, UpgradeManager
from .cps_calculator import CPSCalculator


class PurchaseOption:
    """购买选项"""
    
    def __init__(self, option_type: str, name: str, price: float, 
                 efficiency: float, cps_increase: float = 0.0):
        self.type = option_type  # 'building' or 'upgrade'
        self.name = name
        self.price = price
        self.efficiency = efficiency  # CPS增长/价格
        self.cps_increase = cps_increase
        self.payback_time = price / cps_increase if cps_increase > 0 else float('inf')
    
    def __str__(self):
        return (f"PurchaseOption({self.type}: {self.name}, "
                f"price={self.price:.0f}, efficiency={self.efficiency:.6f})")
    
    def __repr__(self):
        return self.__str__()


class PurchaseOptimizer:
    """购买优化器"""
    
    def __init__(self):
        self.cps_calculator = CPSCalculator()
        self.efficiency_cache = {}
        
    def get_best_purchase(self, game_state: GameState, 
                         budget: Optional[float] = None) -> Optional[PurchaseOption]:
        """
        获取最佳购买选择
        """
        if budget is None:
            budget = game_state.cookies
        
        options = self.get_all_purchase_options(game_state, budget)
        
        if not options:
            return None
        
        # 按效率排序，返回最高效的选择
        options.sort(key=lambda x: x.efficiency, reverse=True)
        return options[0]
    
    def get_all_purchase_options(self, game_state: GameState, 
                                budget: float) -> List[PurchaseOption]:
        """
        获取所有可购买选项
        """
        options = []
        
        # 建筑物选项
        building_options = self._get_building_options(game_state, budget)
        options.extend(building_options)
        
        # 升级选项
        upgrade_options = self._get_upgrade_options(game_state, budget)
        options.extend(upgrade_options)
        
        return options
    
    def _get_building_options(self, game_state: GameState, 
                             budget: float) -> List[PurchaseOption]:
        """
        获取建筑物购买选项
        """
        options = []
        
        for building_name, building in BUILDINGS.items():
            current_amount = game_state.get_building_count(building_name)
            price = building.get_price(current_amount)
            
            if price <= budget:
                efficiency = self._calculate_building_efficiency(
                    building_name, current_amount, game_state
                )
                
                # 计算CPS增长
                current_cps = building.get_cps_contribution(current_amount, game_state)
                new_cps = building.get_cps_contribution(current_amount + 1, game_state)
                cps_increase = new_cps - current_cps
                
                option = PurchaseOption(
                    'building', building_name, price, efficiency, cps_increase
                )
                options.append(option)
        
        return options
    
    def _get_upgrade_options(self, game_state: GameState, 
                            budget: float) -> List[PurchaseOption]:
        """
        获取升级购买选项
        """
        options = []
        upgrade_manager = UpgradeManager(game_state)
        
        for upgrade_name in upgrade_manager.get_affordable_upgrades():
            upgrade = UPGRADES[upgrade_name]
            
            if upgrade.price <= budget:
                efficiency = self._calculate_upgrade_efficiency(
                    upgrade_name, game_state
                )
                
                option = PurchaseOption(
                    'upgrade', upgrade_name, upgrade.price, efficiency
                )
                options.append(option)
        
        return options
    
    def _calculate_building_efficiency(self, building_name: str, 
                                     current_amount: int, 
                                     game_state: GameState) -> float:
        """
        计算建筑物购买效率
        """
        building = BUILDINGS[building_name]
        
        # 计算CPS增长
        current_cps = building.get_cps_contribution(current_amount, game_state)
        new_cps = building.get_cps_contribution(current_amount + 1, game_state)
        cps_increase = new_cps - current_cps
        
        # 计算价格
        price = building.get_price(current_amount)
        
        # 效率 = CPS增长 / 价格
        return cps_increase / price if price > 0 else 0.0
    
    def _calculate_upgrade_efficiency(self, upgrade_name: str, 
                                    game_state: GameState) -> float:
        """
        计算升级购买效率
        """
        upgrade = UPGRADES[upgrade_name]
        
        # 计算升级前后的CPS差异
        current_cps = self.cps_calculator.calculate_total_cps(game_state)
        
        # 模拟购买升级
        temp_state = game_state.copy()
        temp_state.add_upgrade(upgrade_name)
        
        # 使缓存失效以重新计算
        self.cps_calculator.invalidate_cache()
        new_cps = self.cps_calculator.calculate_total_cps(temp_state)
        
        cps_increase = new_cps - current_cps
        
        # 效率 = CPS增长 / 价格
        return cps_increase / upgrade.price if upgrade.price > 0 else 0.0
    
    def get_optimal_strategy(self, game_state: GameState, 
                           time_horizon: float = 3600) -> List[PurchaseOption]:
        """
        获取指定时间范围内的最优购买策略
        """
        strategy = []
        temp_state = game_state.copy()
        
        # 模拟购买过程
        for _ in range(100):  # 最多100次购买
            best_option = self.get_best_purchase(temp_state)
            
            if not best_option:
                break
            
            # 检查是否在时间范围内能够回本
            if best_option.payback_time > time_horizon:
                break
            
            # 执行购买
            if best_option.type == 'building':
                building_manager = BuildingManager(temp_state)
                if building_manager.buy_building(best_option.name):
                    strategy.append(best_option)
            elif best_option.type == 'upgrade':
                upgrade_manager = UpgradeManager(temp_state)
                if upgrade_manager.buy_upgrade(best_option.name):
                    strategy.append(best_option)
            
            # 更新CPS
            temp_state.cookies_per_second = self.cps_calculator.calculate_total_cps(temp_state)
        
        return strategy
    
    def analyze_building_efficiency_curve(self, building_name: str, 
                                        game_state: GameState, 
                                        max_amount: int = 100) -> List[Tuple[int, float]]:
        """
        分析建筑物效率曲线
        """
        if building_name not in BUILDINGS:
            return []
        
        building = BUILDINGS[building_name]
        current_amount = game_state.get_building_count(building_name)
        
        efficiency_curve = []
        
        for amount in range(current_amount, current_amount + max_amount):
            efficiency = self._calculate_building_efficiency(
                building_name, amount, game_state
            )
            efficiency_curve.append((amount, efficiency))
        
        return efficiency_curve
    
    def find_optimal_building_ratio(self, game_state: GameState, 
                                  total_budget: float) -> Dict[str, int]:
        """
        寻找最优建筑物配比
        """
        # 使用贪心算法寻找最优配比
        optimal_ratio = {}
        temp_state = game_state.copy()
        temp_state.cookies = total_budget
        
        # 初始化建筑物数量
        for building_name in BUILDINGS.keys():
            optimal_ratio[building_name] = temp_state.get_building_count(building_name)
        
        # 贪心购买
        while temp_state.cookies > 0:
            best_option = self.get_best_purchase(temp_state)
            
            if not best_option or best_option.type != 'building':
                break
            
            # 购买建筑物
            building_manager = BuildingManager(temp_state)
            if building_manager.buy_building(best_option.name):
                optimal_ratio[best_option.name] += 1
            else:
                break
        
        return optimal_ratio
    
    def calculate_time_to_afford(self, target_price: float, 
                               game_state: GameState) -> float:
        """
        计算能够负担目标价格所需的时间
        """
        current_cookies = game_state.cookies
        current_cps = game_state.cookies_per_second
        
        if current_cookies >= target_price:
            return 0.0
        
        if current_cps <= 0:
            return float('inf')
        
        needed_cookies = target_price - current_cookies
        return needed_cookies / current_cps
    
    def get_purchase_priority_list(self, game_state: GameState, 
                                 max_items: int = 20) -> List[PurchaseOption]:
        """
        获取购买优先级列表
        """
        # 获取所有可能的购买选项(不限制预算)
        all_options = []
        
        # 建筑物选项
        for building_name, building in BUILDINGS.items():
            current_amount = game_state.get_building_count(building_name)
            price = building.get_price(current_amount)
            efficiency = self._calculate_building_efficiency(
                building_name, current_amount, game_state
            )
            
            current_cps = building.get_cps_contribution(current_amount, game_state)
            new_cps = building.get_cps_contribution(current_amount + 1, game_state)
            cps_increase = new_cps - current_cps
            
            option = PurchaseOption(
                'building', building_name, price, efficiency, cps_increase
            )
            all_options.append(option)
        
        # 升级选项
        upgrade_manager = UpgradeManager(game_state)
        for upgrade_name in upgrade_manager.get_available_upgrades():
            upgrade = UPGRADES[upgrade_name]
            efficiency = self._calculate_upgrade_efficiency(upgrade_name, game_state)
            
            option = PurchaseOption(
                'upgrade', upgrade_name, upgrade.price, efficiency
            )
            all_options.append(option)
        
        # 按效率排序
        all_options.sort(key=lambda x: x.efficiency, reverse=True)
        
        return all_options[:max_items]
    
    def simulate_purchase_sequence(self, game_state: GameState, 
                                 purchase_list: List[str], 
                                 time_limit: float = 3600) -> Dict[str, Any]:
        """
        模拟购买序列的效果
        """
        temp_state = game_state.copy()
        results = {
            'initial_cps': self.cps_calculator.calculate_total_cps(temp_state),
            'purchases_made': [],
            'total_cost': 0.0,
            'time_taken': 0.0,
            'final_cps': 0.0
        }
        
        for item_name in purchase_list:
            # 计算购买所需时间
            if item_name in BUILDINGS:
                current_amount = temp_state.get_building_count(item_name)
                price = BUILDINGS[item_name].get_price(current_amount)
            elif item_name in UPGRADES:
                price = UPGRADES[item_name].price
            else:
                continue
            
            wait_time = self.calculate_time_to_afford(price, temp_state)
            
            if results['time_taken'] + wait_time > time_limit:
                break
            
            # 等待并生产饼干
            temp_state.cookies += temp_state.cookies_per_second * wait_time
            results['time_taken'] += wait_time
            
            # 执行购买
            if item_name in BUILDINGS:
                building_manager = BuildingManager(temp_state)
                if building_manager.buy_building(item_name):
                    results['purchases_made'].append(item_name)
                    results['total_cost'] += price
            elif item_name in UPGRADES:
                upgrade_manager = UpgradeManager(temp_state)
                if upgrade_manager.buy_upgrade(item_name):
                    results['purchases_made'].append(item_name)
                    results['total_cost'] += price
            
            # 更新CPS
            temp_state.cookies_per_second = self.cps_calculator.calculate_total_cps(temp_state)
        
        results['final_cps'] = temp_state.cookies_per_second
        results['cps_improvement'] = results['final_cps'] - results['initial_cps']
        results['efficiency'] = (results['cps_improvement'] / results['total_cost'] 
                               if results['total_cost'] > 0 else 0.0)
        
        return results
