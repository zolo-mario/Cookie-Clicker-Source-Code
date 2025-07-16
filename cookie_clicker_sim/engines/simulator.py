"""
游戏模拟器

Cookie Clicker的完整游戏模拟引擎
"""

import time
import copy
from typing import Dict, List, Optional, Callable, Any
from ..core.game_state import GameState
from ..core.buildings import BuildingManager
from ..core.upgrades import UpgradeManager
from .cps_calculator import CPSCalculator
from .purchase_optimizer import PurchaseOptimizer


class GameSimulator:
    """游戏模拟器"""
    
    def __init__(self, initial_state: Optional[GameState] = None):
        self.game_state = initial_state or GameState()
        self.cps_calculator = CPSCalculator()
        self.purchase_optimizer = PurchaseOptimizer()
        self.building_manager = BuildingManager(self.game_state)
        self.upgrade_manager = UpgradeManager(self.game_state)
        
        # 模拟设置
        self.auto_buy_enabled = True
        self.auto_click_enabled = False
        self.auto_ascend_enabled = False
        
        # 统计数据
        self.simulation_stats = {
            'total_time': 0.0,
            'total_steps': 0,
            'cookies_produced': 0.0,
            'buildings_bought': 0,
            'upgrades_bought': 0,
            'ascensions': 0
        }
        
        # 事件回调
        self.event_callbacks = {}
    
    def reset(self, new_state: Optional[GameState] = None):
        """重置模拟器"""
        self.game_state = new_state or GameState()
        self.building_manager = BuildingManager(self.game_state)
        self.upgrade_manager = UpgradeManager(self.game_state)
        self.cps_calculator.invalidate_cache()
        
        # 重置统计
        self.simulation_stats = {
            'total_time': 0.0,
            'total_steps': 0,
            'cookies_produced': 0.0,
            'buildings_bought': 0,
            'upgrades_bought': 0,
            'ascensions': 0
        }
    
    def simulate_step(self, dt: float = 1.0):
        """
        模拟一个时间步长
        """
        # 更新CPS
        self.game_state.cookies_per_second = self.cps_calculator.calculate_total_cps(
            self.game_state
        )
        
        # 生产饼干
        cookies_produced = self.game_state.cookies_per_second * dt
        self.game_state.earn_cookies(cookies_produced)
        self.simulation_stats['cookies_produced'] += cookies_produced
        
        # 更新buff状态
        self.game_state.update_buffs(dt)
        
        # 更新升级解锁状态
        self.upgrade_manager.update_unlocks()
        
        # 自动点击
        if self.auto_click_enabled:
            self._auto_click(dt)
        
        # 自动购买
        if self.auto_buy_enabled:
            self._auto_purchase()
        
        # 自动重生
        if self.auto_ascend_enabled:
            self._auto_ascend()
        
        # 更新时间
        self.game_state.game_time += dt
        self.game_state.last_update = time.time()
        self.simulation_stats['total_time'] += dt
        self.simulation_stats['total_steps'] += 1
        
        # 触发事件回调
        self._trigger_event('step', dt)
    
    def simulate_time_period(self, duration: float, time_step: float = 1.0):
        """
        模拟指定时间段
        """
        steps = int(duration / time_step)
        remaining_time = duration % time_step
        
        for _ in range(steps):
            self.simulate_step(time_step)
        
        if remaining_time > 0:
            self.simulate_step(remaining_time)
        
        return self.game_state
    
    def simulate_until_condition(self, condition: Callable[[GameState], bool], 
                               max_time: float = 86400, time_step: float = 1.0) -> bool:
        """
        模拟直到满足条件
        """
        elapsed_time = 0.0
        
        while elapsed_time < max_time:
            self.simulate_step(time_step)
            elapsed_time += time_step
            
            if condition(self.game_state):
                return True
        
        return False
    
    def _auto_click(self, dt: float):
        """
        自动点击逻辑
        """
        # 简单的自动点击：每秒点击10次
        clicks_per_second = 10
        click_power = self.cps_calculator.calculate_click_power(self.game_state)
        
        cookies_from_clicks = click_power * clicks_per_second * dt
        self.game_state.earn_cookies(cookies_from_clicks)
        self.game_state.handmade_cookies += cookies_from_clicks
        self.game_state.cookie_clicks += int(clicks_per_second * dt)
    
    def _auto_purchase(self):
        """
        自动购买逻辑
        """
        max_purchases_per_step = 10  # 每步最多购买10次
        purchases_made = 0
        
        while purchases_made < max_purchases_per_step:
            best_option = self.purchase_optimizer.get_best_purchase(self.game_state)
            
            if not best_option:
                break
            
            success = False
            if best_option.type == 'building':
                success = self.building_manager.buy_building(best_option.name)
                if success:
                    self.simulation_stats['buildings_bought'] += 1
            elif best_option.type == 'upgrade':
                success = self.upgrade_manager.buy_upgrade(best_option.name)
                if success:
                    self.simulation_stats['upgrades_bought'] += 1
            
            if success:
                purchases_made += 1
                self.cps_calculator.invalidate_cache()  # 使缓存失效
                self._trigger_event('purchase', best_option)
            else:
                break
    
    def _auto_ascend(self):
        """
        自动重生逻辑
        """
        # 简单的重生策略：当能获得至少10个声望等级时重生
        from ..core.constants import calculate_prestige
        
        total_cookies = self.game_state.cookies_reset + self.game_state.cookies_earned
        potential_prestige = int(calculate_prestige(total_cookies))
        prestige_gain = potential_prestige - self.game_state.prestige
        
        if prestige_gain >= 10:
            self.ascend()
    
    def ascend(self):
        """
        执行重生
        """
        # 计算声望收益
        from ..core.constants import calculate_prestige
        
        total_cookies = self.game_state.cookies_reset + self.game_state.cookies_earned
        new_prestige = int(calculate_prestige(total_cookies))
        prestige_gain = new_prestige - self.game_state.prestige
        
        if prestige_gain > 0:
            self.game_state.heavenly_chips += prestige_gain
            self.game_state.prestige = new_prestige
        
        # 重置游戏状态
        self.game_state.reset_for_ascension()
        
        # 重新初始化管理器
        self.building_manager = BuildingManager(self.game_state)
        self.upgrade_manager = UpgradeManager(self.game_state)
        self.cps_calculator.invalidate_cache()
        
        # 更新统计
        self.simulation_stats['ascensions'] += 1
        
        # 触发事件
        self._trigger_event('ascension', prestige_gain)
    
    def click_cookie(self, times: int = 1):
        """
        手动点击饼干
        """
        click_power = self.cps_calculator.calculate_click_power(self.game_state)
        total_cookies = click_power * times
        
        self.game_state.earn_cookies(total_cookies)
        self.game_state.handmade_cookies += total_cookies
        self.game_state.cookie_clicks += times
        
        self._trigger_event('click', {'times': times, 'cookies': total_cookies})
    
    def buy_building(self, building_name: str, amount: int = 1) -> bool:
        """
        购买建筑物
        """
        success = self.building_manager.buy_building(building_name, amount)
        if success:
            self.cps_calculator.invalidate_cache()
            self.simulation_stats['buildings_bought'] += amount
            self._trigger_event('building_purchase', {
                'name': building_name, 
                'amount': amount
            })
        return success
    
    def buy_upgrade(self, upgrade_name: str) -> bool:
        """
        购买升级
        """
        success = self.upgrade_manager.buy_upgrade(upgrade_name)
        if success:
            self.cps_calculator.invalidate_cache()
            self.simulation_stats['upgrades_bought'] += 1
            self._trigger_event('upgrade_purchase', {'name': upgrade_name})
        return success
    
    def add_buff(self, buff_name: str, duration: float, effect: Dict[str, Any]):
        """
        添加buff效果
        """
        self.game_state.add_buff(buff_name, duration, effect)
        self.cps_calculator.invalidate_cache()
        self._trigger_event('buff_added', {
            'name': buff_name, 
            'duration': duration, 
            'effect': effect
        })
    
    def get_simulation_summary(self) -> Dict[str, Any]:
        """
        获取模拟总结
        """
        return {
            'game_state': {
                'cookies': self.game_state.cookies,
                'cookies_earned': self.game_state.cookies_earned,
                'cookies_per_second': self.game_state.cookies_per_second,
                'total_buildings': self.game_state.get_total_buildings(),
                'upgrades_owned': len(self.game_state.upgrades_owned),
                'achievements': len(self.game_state.achievements),
                'prestige': self.game_state.prestige,
                'heavenly_chips': self.game_state.heavenly_chips
            },
            'simulation_stats': self.simulation_stats.copy(),
            'efficiency_metrics': {
                'cookies_per_hour': (self.simulation_stats['cookies_produced'] / 
                                   max(self.simulation_stats['total_time'], 1) * 3600),
                'average_cps': (self.simulation_stats['cookies_produced'] / 
                              max(self.simulation_stats['total_time'], 1)),
                'purchases_per_hour': ((self.simulation_stats['buildings_bought'] + 
                                      self.simulation_stats['upgrades_bought']) / 
                                     max(self.simulation_stats['total_time'], 1) * 3600)
            }
        }
    
    def get_cps_breakdown(self) -> Dict[str, float]:
        """
        获取CPS详细分解
        """
        return self.cps_calculator.get_cps_breakdown(self.game_state)
    
    def get_purchase_recommendations(self, count: int = 5) -> List[Any]:
        """
        获取购买建议
        """
        return self.purchase_optimizer.get_purchase_priority_list(
            self.game_state, count
        )
    
    def set_event_callback(self, event_name: str, callback: Callable):
        """
        设置事件回调
        """
        if event_name not in self.event_callbacks:
            self.event_callbacks[event_name] = []
        self.event_callbacks[event_name].append(callback)
    
    def _trigger_event(self, event_name: str, data: Any = None):
        """
        触发事件回调
        """
        if event_name in self.event_callbacks:
            for callback in self.event_callbacks[event_name]:
                try:
                    callback(self.game_state, data)
                except Exception as e:
                    print(f"Error in event callback {event_name}: {e}")
    
    def save_state(self) -> Dict[str, Any]:
        """
        保存当前状态
        """
        return {
            'game_state': self.game_state.to_dict(),
            'simulation_stats': self.simulation_stats.copy(),
            'settings': {
                'auto_buy_enabled': self.auto_buy_enabled,
                'auto_click_enabled': self.auto_click_enabled,
                'auto_ascend_enabled': self.auto_ascend_enabled
            }
        }
    
    def load_state(self, state_data: Dict[str, Any]):
        """
        加载状态
        """
        # 加载游戏状态
        self.game_state.from_dict(state_data['game_state'])

        # 加载统计数据
        self.simulation_stats.update(state_data.get('simulation_stats', {}))

        # 加载设置
        settings = state_data.get('settings', {})
        self.auto_buy_enabled = settings.get('auto_buy_enabled', True)
        self.auto_click_enabled = settings.get('auto_click_enabled', False)
        self.auto_ascend_enabled = settings.get('auto_ascend_enabled', False)

        # 重新初始化管理器
        self.building_manager = BuildingManager(self.game_state)
        self.upgrade_manager = UpgradeManager(self.game_state)
        self.cps_calculator.invalidate_cache()

        # 重新计算CPS
        self.game_state.cookies_per_second = self.cps_calculator.calculate_total_cps(self.game_state)
    
    def __str__(self):
        return (f"GameSimulator(cookies={self.game_state.cookies:.0f}, "
                f"cps={self.game_state.cookies_per_second:.1f}, "
                f"time={self.simulation_stats['total_time']:.1f}s)")
    
    def __repr__(self):
        return self.__str__()
