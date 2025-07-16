"""
Cookie Clicker 数值模型深度分析

分析游戏的核心数值机制、增长模型和最优策略
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from ..core.game_state import GameState
from ..core.buildings import BUILDINGS
from ..core.constants import *


class NumericalAnalyzer:
    """数值模型分析器"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_growth_model(self) -> Dict[str, Any]:
        """
        分析游戏的增长模型
        """
        print("=== Cookie Clicker 增长模型分析 ===")
        
        # 1. 建筑物价格增长模型
        price_analysis = self._analyze_price_growth()
        
        # 2. CPS增长模型  
        cps_analysis = self._analyze_cps_growth()
        
        # 3. 声望系统模型
        prestige_analysis = self._analyze_prestige_model()
        
        # 4. 效率衰减模型
        efficiency_analysis = self._analyze_efficiency_decay()
        
        return {
            'price_growth': price_analysis,
            'cps_growth': cps_analysis,
            'prestige_model': prestige_analysis,
            'efficiency_decay': efficiency_analysis
        }
    
    def _analyze_price_growth(self) -> Dict[str, Any]:
        """分析建筑物价格增长模型"""
        print("\n1. 建筑物价格增长模型")
        
        # 价格增长公式: price = base_price * (1.15^amount)
        multiplier = BUILDING_PRICE_MULTIPLIER  # 1.15
        
        analysis = {
            'model_type': 'Exponential Growth',
            'formula': f'price = base_price × {multiplier}^amount',
            'growth_rate': f'{(multiplier - 1) * 100:.0f}% per building',
            'doubling_time': math.log(2) / math.log(multiplier),
            'examples': {}
        }
        
        # 分析不同建筑物的价格增长
        for name, building in list(BUILDINGS.items())[:5]:
            base_price = building.base_price
            prices_at_amounts = []
            
            for amount in [0, 10, 25, 50, 100]:
                price = base_price * (multiplier ** amount)
                prices_at_amounts.append((amount, price))
            
            analysis['examples'][name] = {
                'base_price': base_price,
                'price_progression': prices_at_amounts,
                'price_at_100': base_price * (multiplier ** 100)
            }
        
        print(f"  增长模型: {analysis['model_type']}")
        print(f"  增长公式: {analysis['formula']}")
        print(f"  每个建筑物价格增长: {analysis['growth_rate']}")
        print(f"  价格翻倍需要建筑物数量: {analysis['doubling_time']:.1f}个")
        
        return analysis
    
    def _analyze_cps_growth(self) -> Dict[str, Any]:
        """分析CPS增长模型"""
        print("\n2. CPS增长模型")
        
        analysis = {
            'model_type': 'Linear per Building + Exponential via Price',
            'base_formula': 'total_cps = Σ(building_amount × building_base_cps × multipliers)',
            'growth_characteristics': {},
            'building_efficiency': {}
        }
        
        # 分析每个建筑物的CPS效率
        for name, building in BUILDINGS.items():
            base_cps = building.base_cps
            base_price = building.base_price
            
            # 计算基础效率 (CPS per cookie spent)
            base_efficiency = base_cps / base_price
            
            # 计算在不同数量下的边际效率
            marginal_efficiencies = []
            for amount in range(0, 11):
                price = building.get_price(amount)
                marginal_efficiency = base_cps / price
                marginal_efficiencies.append((amount, marginal_efficiency))
            
            analysis['building_efficiency'][name] = {
                'base_cps': base_cps,
                'base_price': base_price,
                'base_efficiency': base_efficiency,
                'marginal_efficiency_decay': marginal_efficiencies
            }
        
        # 找出最高效的建筑物
        best_building = max(analysis['building_efficiency'].items(), 
                          key=lambda x: x[1]['base_efficiency'])
        
        analysis['most_efficient_building'] = {
            'name': best_building[0],
            'efficiency': best_building[1]['base_efficiency']
        }
        
        print(f"  CPS模型: {analysis['model_type']}")
        print(f"  最高效建筑物: {best_building[0]} (效率: {best_building[1]['base_efficiency']:.6f})")
        
        return analysis
    
    def _analyze_prestige_model(self) -> Dict[str, Any]:
        """分析声望系统模型"""
        print("\n3. 声望系统模型")
        
        # 声望公式: prestige = (total_cookies / 1e12)^(1/3)
        analysis = {
            'model_type': 'Cube Root Growth',
            'formula': 'prestige = (total_cookies / 1×10¹²)^(1/3)',
            'growth_rate': 'Decreasing marginal returns',
            'prestige_levels': [],
            'cookie_requirements': []
        }
        
        # 计算不同声望等级需要的饼干数
        prestige_levels = [1, 10, 100, 1000, 10000]
        for prestige in prestige_levels:
            cookies_needed = calculate_cookies_for_prestige(prestige)
            analysis['prestige_levels'].append((prestige, cookies_needed))
        
        # 计算不同饼干数量对应的声望
        cookie_amounts = [1e12, 1e15, 1e18, 1e21, 1e24]
        for cookies in cookie_amounts:
            prestige = calculate_prestige(cookies)
            analysis['cookie_requirements'].append((cookies, prestige))
        
        print(f"  声望模型: {analysis['model_type']}")
        print(f"  增长特性: {analysis['growth_rate']}")
        print("  声望等级示例:")
        for prestige, cookies in analysis['prestige_levels'][:3]:
            print(f"    {prestige}级声望需要: {cookies:.2e} 饼干")
        
        return analysis
    
    def _analyze_efficiency_decay(self) -> Dict[str, Any]:
        """分析效率衰减模型"""
        print("\n4. 效率衰减模型")
        
        analysis = {
            'model_type': 'Exponential Decay due to Price Growth',
            'decay_rate': f'{(1 - 1/BUILDING_PRICE_MULTIPLIER) * 100:.1f}% per building',
            'efficiency_curves': {}
        }
        
        # 分析主要建筑物的效率衰减
        key_buildings = ['Cursor', 'Grandma', 'Farm', 'Factory']
        
        for building_name in key_buildings:
            if building_name in BUILDINGS:
                building = BUILDINGS[building_name]
                
                # 计算效率衰减曲线
                amounts = list(range(0, 51))
                efficiencies = []
                
                for amount in amounts:
                    price = building.get_price(amount)
                    efficiency = building.base_cps / price
                    efficiencies.append(efficiency)
                
                # 找到效率减半点
                initial_efficiency = efficiencies[0]
                half_efficiency = initial_efficiency / 2
                
                half_point = None
                for i, eff in enumerate(efficiencies):
                    if eff <= half_efficiency:
                        half_point = i
                        break
                
                analysis['efficiency_curves'][building_name] = {
                    'initial_efficiency': initial_efficiency,
                    'efficiency_at_10': efficiencies[10] if len(efficiencies) > 10 else 0,
                    'efficiency_at_25': efficiencies[25] if len(efficiencies) > 25 else 0,
                    'half_efficiency_point': half_point
                }
        
        print(f"  衰减模型: {analysis['model_type']}")
        print(f"  衰减率: {analysis['decay_rate']}")
        
        return analysis
    
    def analyze_optimal_strategies(self) -> Dict[str, Any]:
        """
        分析最优策略
        """
        print("\n=== 最优策略分析 ===")
        
        # 1. 早期策略 (0-1小时)
        early_strategy = self._analyze_early_game_strategy()
        
        # 2. 中期策略 (1-10小时)
        mid_strategy = self._analyze_mid_game_strategy()
        
        # 3. 后期策略 (10小时+)
        late_strategy = self._analyze_late_game_strategy()
        
        # 4. 重生策略
        ascension_strategy = self._analyze_ascension_strategy()
        
        return {
            'early_game': early_strategy,
            'mid_game': mid_strategy,
            'late_game': late_strategy,
            'ascension': ascension_strategy
        }
    
    def _analyze_early_game_strategy(self) -> Dict[str, Any]:
        """分析早期游戏策略"""
        print("\n1. 早期策略分析 (0-1小时)")
        
        strategy = {
            'phase': 'Early Game (0-1 hour)',
            'primary_goal': 'Establish basic CPS foundation',
            'key_principles': [
                'Focus on cheapest buildings first',
                'Buy upgrades as soon as available',
                'Manual clicking for initial capital',
                'Prioritize Cursor and Grandma buildings'
            ],
            'building_priority': ['Cursor', 'Grandma', 'Farm'],
            'upgrade_priority': 'All available upgrades',
            'expected_progress': {
                'cookies_by_1hour': '10K - 100K',
                'cps_by_1hour': '100 - 1,000',
                'buildings_by_1hour': '20 - 50'
            }
        }
        
        print(f"  阶段: {strategy['phase']}")
        print(f"  主要目标: {strategy['primary_goal']}")
        print(f"  建筑物优先级: {', '.join(strategy['building_priority'])}")
        
        return strategy
    
    def _analyze_mid_game_strategy(self) -> Dict[str, Any]:
        """分析中期游戏策略"""
        print("\n2. 中期策略分析 (1-10小时)")
        
        strategy = {
            'phase': 'Mid Game (1-10 hours)',
            'primary_goal': 'Optimize efficiency and unlock higher-tier buildings',
            'key_principles': [
                'Balance between buildings and upgrades',
                'Focus on efficiency rather than cheapest options',
                'Unlock and invest in higher-tier buildings',
                'Consider first ascension around 10-50 prestige'
            ],
            'building_priority': ['Factory', 'Bank', 'Temple', 'Wizard Tower'],
            'upgrade_priority': 'Efficiency-focused upgrades',
            'expected_progress': {
                'cookies_by_10hour': '1M - 1B',
                'cps_by_10hour': '10K - 1M',
                'buildings_by_10hour': '100 - 500'
            }
        }
        
        print(f"  阶段: {strategy['phase']}")
        print(f"  主要目标: {strategy['primary_goal']}")
        print(f"  建筑物优先级: {', '.join(strategy['building_priority'])}")
        
        return strategy
    
    def _analyze_late_game_strategy(self) -> Dict[str, Any]:
        """分析后期游戏策略"""
        print("\n3. 后期策略分析 (10小时+)")
        
        strategy = {
            'phase': 'Late Game (10+ hours)',
            'primary_goal': 'Maximize prestige gain and unlock endgame content',
            'key_principles': [
                'Focus on highest-tier buildings',
                'Optimize ascension timing',
                'Utilize heavenly upgrades effectively',
                'Balance between active and idle play'
            ],
            'building_priority': ['Time Machine', 'Antimatter Condenser', 'Prism'],
            'upgrade_priority': 'Heavenly upgrades and synergy upgrades',
            'expected_progress': {
                'cookies_per_ascension': '1T - 1Qa',
                'prestige_per_ascension': '100 - 10K',
                'ascension_frequency': 'Every 2-24 hours'
            }
        }
        
        print(f"  阶段: {strategy['phase']}")
        print(f"  主要目标: {strategy['primary_goal']}")
        print(f"  建筑物优先级: {', '.join(strategy['building_priority'])}")
        
        return strategy
    
    def _analyze_ascension_strategy(self) -> Dict[str, Any]:
        """分析重生策略"""
        print("\n4. 重生策略分析")
        
        strategy = {
            'optimal_timing': 'When prestige gain >= current prestige × 0.5',
            'minimum_prestige_gain': 10,
            'heavenly_upgrade_priority': [
                'Heavenly chip secret (+5% heavenly chip power)',
                'Heavenly cookie stand (+20% heavenly chip power)',
                'Heavenly bakery (+25% heavenly chip power)'
            ],
            'post_ascension_strategy': [
                'Immediately buy key heavenly upgrades',
                'Rush to previous building levels quickly',
                'Focus on unlocking new content'
            ]
        }
        
        print(f"  最优重生时机: {strategy['optimal_timing']}")
        print(f"  最小声望增长: {strategy['minimum_prestige_gain']}")
        
        return strategy
    
    def calculate_theoretical_limits(self) -> Dict[str, Any]:
        """
        计算理论极限
        """
        print("\n=== 理论极限分析 ===")
        
        # JavaScript Number.MAX_SAFE_INTEGER = 2^53 - 1
        max_safe_integer = 2**53 - 1
        
        # 计算各种理论极限
        limits = {
            'max_cookies': max_safe_integer,
            'max_prestige': calculate_prestige(max_safe_integer),
            'max_building_amount': 5000,  # 游戏内部限制
            'theoretical_max_cps': 0
        }
        
        # 计算理论最大CPS
        max_cps = 0
        for building in BUILDINGS.values():
            building_max_cps = building.base_cps * limits['max_building_amount']
            max_cps += building_max_cps
        
        # 考虑各种倍数 (简化估算)
        total_multiplier = 1000  # 保守估计的总倍数
        limits['theoretical_max_cps'] = max_cps * total_multiplier
        
        print(f"最大安全整数: {limits['max_cookies']:.2e}")
        print(f"理论最大声望: {limits['max_prestige']:.0f}")
        print(f"理论最大CPS: {limits['theoretical_max_cps']:.2e}")
        
        return limits
    
    def generate_comprehensive_report(self) -> str:
        """
        生成综合分析报告
        """
        print("\n=== 生成综合分析报告 ===")
        
        # 执行所有分析
        growth_analysis = self.analyze_growth_model()
        strategy_analysis = self.analyze_optimal_strategies()
        limits_analysis = self.calculate_theoretical_limits()
        
        # 生成报告
        report = f"""
Cookie Clicker 数值模型与策略深度分析报告
==========================================

## 1. 核心数值模型

### 1.1 建筑物价格增长模型
- 模型类型: {growth_analysis['price_growth']['model_type']}
- 增长公式: {growth_analysis['price_growth']['formula']}
- 增长率: {growth_analysis['price_growth']['growth_rate']}
- 价格翻倍点: {growth_analysis['price_growth']['doubling_time']:.1f}个建筑物

### 1.2 CPS增长模型
- 模型类型: {growth_analysis['cps_growth']['model_type']}
- 最高效建筑物: {growth_analysis['cps_growth']['most_efficient_building']['name']}
- 基础效率: {growth_analysis['cps_growth']['most_efficient_building']['efficiency']:.6f}

### 1.3 声望系统模型
- 模型类型: {growth_analysis['prestige_model']['model_type']}
- 增长公式: {growth_analysis['prestige_model']['formula']}
- 增长特性: {growth_analysis['prestige_model']['growth_rate']}

### 1.4 效率衰减模型
- 模型类型: {growth_analysis['efficiency_decay']['model_type']}
- 衰减率: {growth_analysis['efficiency_decay']['decay_rate']}

## 2. 最优策略分析

### 2.1 早期策略 (0-1小时)
- 主要目标: {strategy_analysis['early_game']['primary_goal']}
- 建筑物优先级: {', '.join(strategy_analysis['early_game']['building_priority'])}
- 预期进度: {strategy_analysis['early_game']['expected_progress']['cookies_by_1hour']} 饼干

### 2.2 中期策略 (1-10小时)
- 主要目标: {strategy_analysis['mid_game']['primary_goal']}
- 建筑物优先级: {', '.join(strategy_analysis['mid_game']['building_priority'])}
- 预期进度: {strategy_analysis['mid_game']['expected_progress']['cookies_by_10hour']} 饼干

### 2.3 后期策略 (10小时+)
- 主要目标: {strategy_analysis['late_game']['primary_goal']}
- 建筑物优先级: {', '.join(strategy_analysis['late_game']['building_priority'])}
- 重生频率: {strategy_analysis['late_game']['expected_progress']['ascension_frequency']}

### 2.4 重生策略
- 最优时机: {strategy_analysis['ascension']['optimal_timing']}
- 最小声望增长: {strategy_analysis['ascension']['minimum_prestige_gain']}

## 3. 理论极限
- 最大饼干数: {limits_analysis['max_cookies']:.2e}
- 理论最大声望: {limits_analysis['max_prestige']:.0f}
- 理论最大CPS: {limits_analysis['theoretical_max_cps']:.2e}

## 4. 关键洞察

### 4.1 数学本质
Cookie Clicker本质上是一个指数增长与指数成本的平衡游戏。建筑物价格的1.15倍增长创造了一个自然的效率衰减，迫使玩家不断寻找新的增长点。

### 4.2 策略核心
最优策略的核心是在任何给定时刻选择效率最高的投资选项。这需要平衡：
- 短期CPS增长 vs 长期投资
- 建筑物购买 vs 升级购买
- 当前进度 vs 重生收益

### 4.3 心理设计
游戏通过以下机制维持玩家参与：
- 指数增长带来的成就感
- 持续的新解锁内容
- 重生系统提供的"重新开始"动机
- 数字增长的视觉满足感

## 5. 建议与结论

对于新玩家：
1. 早期专注于建立基础CPS
2. 不要忽视升级的重要性
3. 学会计算购买效率
4. 适时进行第一次重生

对于高级玩家：
1. 精确计算重生时机
2. 优化天堂升级路径
3. 利用小游戏系统
4. 平衡主动和挂机游戏

Cookie Clicker的成功在于其简单而深刻的数学模型，以及精心设计的心理激励机制。
"""
        
        return report


if __name__ == "__main__":
    analyzer = NumericalAnalyzer()
    report = analyzer.generate_comprehensive_report()
    print(report)
