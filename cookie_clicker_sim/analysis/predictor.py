"""
进度预测器

预测Cookie Clicker游戏进度和达成目标所需时间
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.game_state import GameState
from ..core.constants import calculate_prestige, calculate_cookies_for_prestige


class ProgressPredictor:
    """进度预测器"""
    
    def __init__(self):
        pass
    
    def predict_time_to_cookies(self, game_state: GameState, target_cookies: float) -> float:
        """
        预测达到目标饼干数所需时间
        """
        current_cookies = game_state.cookies
        current_cps = game_state.cookies_per_second
        
        if current_cookies >= target_cookies:
            return 0.0
        
        if current_cps <= 0:
            return float('inf')
        
        needed_cookies = target_cookies - current_cookies
        return needed_cookies / current_cps
    
    def predict_time_to_prestige(self, game_state: GameState, target_prestige: int) -> float:
        """
        预测达到目标声望等级所需时间
        """
        target_cookies = calculate_cookies_for_prestige(target_prestige)
        total_cookies_needed = target_cookies - game_state.cookies_reset
        current_cookies = game_state.cookies_earned
        
        if current_cookies >= total_cookies_needed:
            return 0.0
        
        return self.predict_time_to_cookies(game_state, total_cookies_needed)
    
    def predict_optimal_ascension_time(self, game_state: GameState) -> Dict[str, Any]:
        """
        预测最优重生时机
        """
        current_total = game_state.cookies_reset + game_state.cookies_earned
        current_prestige = int(calculate_prestige(current_total))
        
        # 计算不同声望增长的时间成本
        predictions = {}
        
        for prestige_gain in [1, 5, 10, 25, 50]:
            target_prestige = current_prestige + prestige_gain
            time_needed = self.predict_time_to_prestige(game_state, target_prestige)
            
            predictions[f'+{prestige_gain}声望'] = {
                'target_prestige': target_prestige,
                'time_needed': time_needed,
                'prestige_gain': prestige_gain
            }
        
        return predictions
