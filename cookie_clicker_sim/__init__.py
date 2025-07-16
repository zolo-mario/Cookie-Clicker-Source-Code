"""
Cookie Clicker 数值模拟器

基于Cookie Clicker源码分析的数值模拟系统，用于游戏策略优化和平衡性分析。
"""

__version__ = "1.0.0"
__author__ = "Cookie Clicker Simulator Team"

from .core.game_state import GameState
from .core.buildings import Building, BUILDINGS
from .core.upgrades import Upgrade, UPGRADES
from .engines.simulator import GameSimulator
from .engines.cps_calculator import CPSCalculator
from .engines.purchase_optimizer import PurchaseOptimizer

__all__ = [
    'GameState',
    'Building', 'BUILDINGS',
    'Upgrade', 'UPGRADES', 
    'GameSimulator',
    'CPSCalculator',
    'PurchaseOptimizer'
]
