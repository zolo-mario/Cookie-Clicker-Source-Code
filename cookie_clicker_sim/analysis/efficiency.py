"""
效率分析器

分析Cookie Clicker中各种购买选项的效率
"""

from typing import Dict, List, Tuple, Optional, Any
from ..core.game_state import GameState
from ..core.buildings import BUILDINGS
from ..core.upgrades import UPGRADES


class EfficiencyAnalyzer:
    """效率分析器"""
    
    def __init__(self):
        pass
    
    def analyze_building_efficiency(self, game_state: GameState) -> Dict[str, Dict[str, float]]:
        """
        分析所有建筑物的效率
        """
        results = {}
        
        for building_name, building in BUILDINGS.items():
            current_amount = game_state.get_building_count(building_name)
            
            if current_amount > 0:
                price = building.get_price(current_amount)
                cps = building.get_cps_contribution(current_amount, game_state)
                efficiency = building.get_efficiency(current_amount, game_state)
                
                results[building_name] = {
                    'amount': current_amount,
                    'price': price,
                    'cps': cps,
                    'efficiency': efficiency,
                    'cps_per_building': cps / current_amount if current_amount > 0 else 0
                }
        
        return results
    
    def find_most_efficient_building(self, game_state: GameState) -> Optional[str]:
        """
        找到效率最高的建筑物
        """
        best_building = None
        best_efficiency = 0.0
        
        for building_name, building in BUILDINGS.items():
            current_amount = game_state.get_building_count(building_name)
            efficiency = building.get_efficiency(current_amount, game_state)
            
            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_building = building_name
        
        return best_building
    
    def compare_strategies(self, strategies: Dict[str, GameState]) -> Dict[str, Dict[str, Any]]:
        """
        比较不同策略的效果
        """
        results = {}
        
        for strategy_name, game_state in strategies.items():
            results[strategy_name] = {
                'cookies': game_state.cookies,
                'cps': game_state.cookies_per_second,
                'buildings': game_state.get_total_buildings(),
                'upgrades': len(game_state.upgrades_owned),
                'prestige': game_state.prestige
            }
        
        return results
