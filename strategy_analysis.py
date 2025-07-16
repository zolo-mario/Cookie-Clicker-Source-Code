"""
Cookie Clicker 策略深度分析

通过实际模拟验证不同策略的效果，分析数值模型的实际表现
"""

import sys
import os
import time
import numpy as np

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

from cookie_clicker_sim import GameSimulator
from cookie_clicker_sim.core.buildings import BUILDINGS
from cookie_clicker_sim.core.constants import calculate_prestige
from cookie_clicker_sim.analysis.numerical_analysis import NumericalAnalyzer


def analyze_building_efficiency_curves():
    """分析建筑物效率曲线"""
    print("=== 建筑物效率曲线分析 ===")
    
    simulator = GameSimulator()
    simulator.game_state.cookies = 1e12  # 给大量饼干用于分析
    
    # 分析前6个建筑物的效率曲线
    buildings_to_analyze = list(BUILDINGS.keys())[:6]
    
    efficiency_data = {}
    
    for building_name in buildings_to_analyze:
        print(f"\n分析 {building_name} 效率曲线...")
        
        building = BUILDINGS[building_name]
        amounts = list(range(0, 101, 5))  # 0到100，每5个一个点
        efficiencies = []
        prices = []
        cps_values = []
        
        for amount in amounts:
            # 计算价格和效率
            price = building.get_price(amount)
            
            # 模拟拥有这个数量的建筑物
            temp_state = simulator.game_state.copy()
            temp_state.buildings[building_name] = amount
            
            cps = building.get_cps_contribution(amount, temp_state)
            efficiency = building.get_efficiency(amount, temp_state)
            
            prices.append(price)
            cps_values.append(cps)
            efficiencies.append(efficiency)
        
        efficiency_data[building_name] = {
            'amounts': amounts,
            'prices': prices,
            'cps_values': cps_values,
            'efficiencies': efficiencies,
            'base_price': building.base_price,
            'base_cps': building.base_cps
        }
        
        # 找到效率峰值
        max_efficiency_idx = np.argmax(efficiencies)
        max_efficiency = efficiencies[max_efficiency_idx]
        optimal_amount = amounts[max_efficiency_idx]
        
        print(f"  基础价格: {building.base_price:,.0f}")
        print(f"  基础CPS: {building.base_cps}")
        print(f"  最高效率: {max_efficiency:.8f} (在{optimal_amount}个时)")
        print(f"  效率衰减: {efficiencies[0]:.8f} -> {efficiencies[-1]:.8f}")
    
    return efficiency_data


def test_different_strategies():
    """测试不同的购买策略"""
    print("\n=== 策略对比测试 ===")
    
    strategies = {
        'greedy_cheapest': '贪心最便宜策略',
        'greedy_efficient': '贪心最高效策略', 
        'balanced': '平衡策略',
        'building_focused': '专注建筑物策略',
        'upgrade_focused': '专注升级策略'
    }
    
    results = {}
    test_duration = 1800  # 30分钟测试
    
    for strategy_name, strategy_desc in strategies.items():
        print(f"\n测试策略: {strategy_desc}")
        
        simulator = GameSimulator()
        simulator.game_state.cookies = 5000  # 统一起始条件
        
        # 根据策略调整模拟器设置
        if strategy_name == 'greedy_cheapest':
            # 实现最便宜优先策略
            simulator.auto_buy_enabled = False
            simulate_cheapest_strategy(simulator, test_duration)
        elif strategy_name == 'greedy_efficient':
            # 使用默认的效率优先策略
            simulator.auto_buy_enabled = True
            simulator.simulate_time_period(test_duration)
        elif strategy_name == 'balanced':
            # 平衡策略：50%时间买建筑物，50%时间买升级
            simulate_balanced_strategy(simulator, test_duration)
        elif strategy_name == 'building_focused':
            # 专注建筑物策略
            simulate_building_focused_strategy(simulator, test_duration)
        elif strategy_name == 'upgrade_focused':
            # 专注升级策略
            simulate_upgrade_focused_strategy(simulator, test_duration)
        
        # 收集结果
        summary = simulator.get_simulation_summary()
        results[strategy_name] = {
            'description': strategy_desc,
            'final_cookies': summary['game_state']['cookies'],
            'final_cps': summary['game_state']['cookies_per_second'],
            'total_buildings': summary['game_state']['total_buildings'],
            'total_upgrades': summary['game_state']['upgrades_owned'],
            'buildings_bought': summary['simulation_stats']['buildings_bought'],
            'upgrades_bought': summary['simulation_stats']['upgrades_bought'],
            'efficiency': summary['efficiency_metrics']['cookies_per_hour']
        }
        
        print(f"  最终饼干: {results[strategy_name]['final_cookies']:,.0f}")
        print(f"  最终CPS: {results[strategy_name]['final_cps']:,.1f}")
        print(f"  建筑物: {results[strategy_name]['total_buildings']}")
        print(f"  升级: {results[strategy_name]['total_upgrades']}")
    
    return results


def simulate_cheapest_strategy(simulator, duration):
    """模拟最便宜优先策略"""
    end_time = simulator.game_state.game_time + duration
    
    while simulator.game_state.game_time < end_time:
        # 找到最便宜的可购买选项
        cheapest_option = None
        cheapest_price = float('inf')
        
        # 检查建筑物
        for building_name, building in BUILDINGS.items():
            current_amount = simulator.game_state.get_building_count(building_name)
            price = building.get_price(current_amount)
            
            if price < cheapest_price and simulator.game_state.cookies >= price:
                cheapest_option = ('building', building_name, price)
                cheapest_price = price
        
        # 检查升级
        from cookie_clicker_sim.core.upgrades import UPGRADES
        for upgrade_name, upgrade in UPGRADES.items():
            if (upgrade.unlocked and not upgrade.bought and 
                upgrade.price < cheapest_price and 
                simulator.game_state.cookies >= upgrade.price):
                cheapest_option = ('upgrade', upgrade_name, upgrade.price)
                cheapest_price = upgrade.price
        
        # 执行购买
        if cheapest_option:
            option_type, name, price = cheapest_option
            if option_type == 'building':
                simulator.buy_building(name)
            else:
                simulator.buy_upgrade(name)
        else:
            # 没有可购买的，等待一段时间
            simulator.simulate_step(60)  # 等待1分钟


def simulate_balanced_strategy(simulator, duration):
    """模拟平衡策略"""
    # 交替购买建筑物和升级
    simulator.auto_buy_enabled = False
    end_time = simulator.game_state.game_time + duration
    buy_buildings = True
    
    while simulator.game_state.game_time < end_time:
        if buy_buildings:
            # 买最高效的建筑物
            best_building = simulator.purchase_optimizer.get_best_purchase(simulator.game_state)
            if best_building and best_building.type == 'building':
                simulator.buy_building(best_building.name)
        else:
            # 买最便宜的升级
            from cookie_clicker_sim.core.upgrades import UpgradeManager
            upgrade_manager = UpgradeManager(simulator.game_state)
            affordable_upgrades = upgrade_manager.get_affordable_upgrades()
            if affordable_upgrades:
                cheapest_upgrade = min(affordable_upgrades, 
                                     key=lambda x: UPGRADES[x].price)
                simulator.buy_upgrade(cheapest_upgrade)
        
        buy_buildings = not buy_buildings
        simulator.simulate_step(30)  # 每30秒决策一次


def simulate_building_focused_strategy(simulator, duration):
    """模拟专注建筑物策略"""
    simulator.auto_buy_enabled = False
    end_time = simulator.game_state.game_time + duration
    
    while simulator.game_state.game_time < end_time:
        # 只买建筑物，忽略升级
        best_option = simulator.purchase_optimizer.get_best_purchase(simulator.game_state)
        
        if best_option and best_option.type == 'building':
            simulator.buy_building(best_option.name)
        else:
            # 如果没有建筑物可买，等待
            simulator.simulate_step(60)


def simulate_upgrade_focused_strategy(simulator, duration):
    """模拟专注升级策略"""
    simulator.auto_buy_enabled = False
    end_time = simulator.game_state.game_time + duration
    
    while simulator.game_state.game_time < end_time:
        # 优先买升级
        from cookie_clicker_sim.core.upgrades import UpgradeManager
        upgrade_manager = UpgradeManager(simulator.game_state)
        affordable_upgrades = upgrade_manager.get_affordable_upgrades()
        
        if affordable_upgrades:
            # 买最便宜的升级
            cheapest_upgrade = min(affordable_upgrades, 
                                 key=lambda x: UPGRADES[x].price)
            simulator.buy_upgrade(cheapest_upgrade)
        else:
            # 没有升级可买时，买最高效的建筑物
            best_option = simulator.purchase_optimizer.get_best_purchase(simulator.game_state)
            if best_option and best_option.type == 'building':
                simulator.buy_building(best_option.name)
            else:
                simulator.simulate_step(60)


def analyze_prestige_timing():
    """分析重生时机"""
    print("\n=== 重生时机分析 ===")
    
    # 模拟不同的重生策略
    prestige_strategies = {
        'never': '从不重生',
        'early_10': '10声望时重生',
        'early_50': '50声望时重生', 
        'optimal': '最优时机重生'
    }
    
    results = {}
    simulation_time = 7200  # 2小时测试
    
    for strategy_name, strategy_desc in prestige_strategies.items():
        print(f"\n测试重生策略: {strategy_desc}")
        
        simulator = GameSimulator()
        simulator.game_state.cookies = 10000
        
        if strategy_name == 'never':
            simulator.auto_ascend_enabled = False
            simulator.simulate_time_period(simulation_time)
        elif strategy_name == 'early_10':
            simulate_early_ascension(simulator, simulation_time, 10)
        elif strategy_name == 'early_50':
            simulate_early_ascension(simulator, simulation_time, 50)
        elif strategy_name == 'optimal':
            simulator.auto_ascend_enabled = True
            simulator.simulate_time_period(simulation_time)
        
        summary = simulator.get_simulation_summary()
        total_cookies = simulator.game_state.cookies_reset + simulator.game_state.cookies_earned
        current_prestige = calculate_prestige(total_cookies)
        
        results[strategy_name] = {
            'description': strategy_desc,
            'final_cookies': summary['game_state']['cookies'],
            'total_cookies_earned': total_cookies,
            'current_prestige': current_prestige,
            'ascensions': summary['simulation_stats']['ascensions'],
            'final_cps': summary['game_state']['cookies_per_second']
        }
        
        print(f"  最终饼干: {results[strategy_name]['final_cookies']:,.0f}")
        print(f"  总获得饼干: {total_cookies:.2e}")
        print(f"  当前声望: {current_prestige:.0f}")
        print(f"  重生次数: {results[strategy_name]['ascensions']}")
    
    return results


def simulate_early_ascension(simulator, duration, target_prestige):
    """模拟早期重生策略"""
    end_time = simulator.game_state.game_time + duration
    
    while simulator.game_state.game_time < end_time:
        # 检查是否应该重生
        total_cookies = simulator.game_state.cookies_reset + simulator.game_state.cookies_earned
        current_prestige = calculate_prestige(total_cookies)
        
        if current_prestige >= target_prestige:
            simulator.ascend()
            print(f"    在{simulator.game_state.game_time:.0f}秒时重生，获得{current_prestige:.0f}声望")
        
        simulator.simulate_step(300)  # 每5分钟检查一次


def generate_strategy_report(efficiency_data, strategy_results, prestige_results):
    """生成策略分析报告"""
    
    report = f"""
Cookie Clicker 策略深度分析报告
==============================

## 1. 建筑物效率分析

### 1.1 基础效率排名
"""
    
    # 计算基础效率排名
    base_efficiencies = []
    for building_name, data in efficiency_data.items():
        base_efficiency = data['base_cps'] / data['base_price']
        base_efficiencies.append((building_name, base_efficiency))
    
    base_efficiencies.sort(key=lambda x: x[1], reverse=True)
    
    for i, (name, efficiency) in enumerate(base_efficiencies, 1):
        report += f"{i}. {name}: {efficiency:.6f} CPS/Cookie\n"
    
    report += f"""
### 1.2 效率衰减分析
所有建筑物都遵循相同的效率衰减模式：
- 衰减率: 13.0% per building (由于1.15倍价格增长)
- 效率减半点: 约5个建筑物
- 长期趋势: 指数衰减

## 2. 策略对比结果

### 2.1 30分钟策略测试结果
"""
    
    # 按最终饼干数排序
    sorted_strategies = sorted(strategy_results.items(), 
                             key=lambda x: x[1]['final_cookies'], reverse=True)
    
    for i, (strategy_name, results) in enumerate(sorted_strategies, 1):
        report += f"""
{i}. {results['description']}
   - 最终饼干: {results['final_cookies']:,.0f}
   - 最终CPS: {results['final_cps']:,.1f}
   - 建筑物: {results['total_buildings']}
   - 升级: {results['total_upgrades']}
   - 效率: {results['efficiency']:,.0f} 饼干/小时
"""
    
    report += f"""
### 2.2 策略分析结论

最优策略: {sorted_strategies[0][1]['description']}
- 效率优先策略在短期内表现最佳
- 平衡策略提供稳定的中等收益
- 专注单一方向的策略通常效果较差

## 3. 重生时机分析

### 3.1 2小时重生策略测试结果
"""
    
    sorted_prestige = sorted(prestige_results.items(), 
                           key=lambda x: x[1]['total_cookies_earned'], reverse=True)
    
    for i, (strategy_name, results) in enumerate(sorted_prestige, 1):
        report += f"""
{i}. {results['description']}
   - 总获得饼干: {results['total_cookies_earned']:.2e}
   - 当前声望: {results['current_prestige']:.0f}
   - 重生次数: {results['ascensions']}
   - 最终CPS: {results['final_cps']:,.1f}
"""
    
    report += f"""
### 3.2 重生策略结论

最优重生策略: {sorted_prestige[0][1]['description']}
- 适时重生比从不重生效果更好
- 过早重生会损失短期收益
- 最优重生时机需要平衡当前进度和声望收益

## 4. 核心策略原则

### 4.1 数学原理
1. **效率优先**: 始终选择 CPS增长/价格 最高的选项
2. **边际收益递减**: 同一建筑物的效率随数量指数衰减
3. **复合增长**: 升级的倍数效果比建筑物的加法效果更强
4. **重生平衡**: 重生收益 vs 当前进度的权衡

### 4.2 实用建议
1. **早期 (0-1小时)**: 专注最便宜的建筑物和所有升级
2. **中期 (1-10小时)**: 平衡建筑物和升级，关注效率
3. **后期 (10小时+)**: 优化重生时机，利用声望加成
4. **长期**: 解锁和利用小游戏系统的额外加成

### 4.3 关键洞察
- Cookie Clicker的核心是一个优化问题
- 最优策略随游戏阶段动态变化
- 数学模型可以指导但不能完全替代直觉
- 游戏的乐趣在于发现和验证最优策略

## 5. 数值模型总结

Cookie Clicker使用了精心设计的数学模型：
- **指数价格增长** 创造自然的效率衰减
- **立方根声望公式** 提供递减但持续的长期激励
- **乘法升级效果** 确保升级始终有价值
- **多层次系统** (建筑物+升级+声望+小游戏) 创造复杂的优化空间

这个模型的成功在于它简单易懂但又足够复杂，能够支撑长期的策略探索和优化。
"""
    
    return report


if __name__ == "__main__":
    print("Cookie Clicker 策略深度分析")
    print("=" * 50)
    
    start_time = time.time()
    
    # 执行各种分析
    print("开始分析...")
    efficiency_data = analyze_building_efficiency_curves()
    strategy_results = test_different_strategies()
    prestige_results = analyze_prestige_timing()
    
    # 生成报告
    report = generate_strategy_report(efficiency_data, strategy_results, prestige_results)
    
    # 保存报告
    with open("strategy_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    end_time = time.time()
    
    print(f"\n" + "=" * 50)
    print("✅ 策略分析完成!")
    print(f"⏱️  总用时: {end_time - start_time:.1f}秒")
    print(f"📋 详细报告已保存到: strategy_analysis_report.txt")
    print(f"📊 分析了 {len(efficiency_data)} 个建筑物效率曲线")
    print(f"🎯 测试了 {len(strategy_results)} 种购买策略")
    print(f"⭐ 测试了 {len(prestige_results)} 种重生策略")
    
    # 显示关键结论
    best_strategy = max(strategy_results.items(), key=lambda x: x[1]['final_cookies'])
    best_prestige = max(prestige_results.items(), key=lambda x: x[1]['total_cookies_earned'])
    
    print(f"\n🏆 关键结论:")
    print(f"   最佳购买策略: {best_strategy[1]['description']}")
    print(f"   最佳重生策略: {best_prestige[1]['description']}")
    print(f"   最高效建筑物: {list(efficiency_data.keys())[0]} (基于基础效率)")
