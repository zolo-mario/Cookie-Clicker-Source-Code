"""
基础模拟示例

演示Cookie Clicker模拟器的基本使用方法
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from cookie_clicker_sim import GameSimulator, GameState
from cookie_clicker_sim.core.constants import calculate_prestige


def basic_simulation_demo():
    """基础模拟演示"""
    print("=== Cookie Clicker 数值模拟器演示 ===\n")
    
    # 创建模拟器
    simulator = GameSimulator()
    
    print("初始状态:")
    print(f"饼干: {simulator.game_state.cookies:.0f}")
    print(f"CPS: {simulator.game_state.cookies_per_second:.1f}")
    print(f"建筑物总数: {simulator.game_state.get_total_buildings()}")
    print()
    
    # 手动点击获得初始饼干
    print("手动点击100次...")
    simulator.click_cookie(100)
    print(f"饼干: {simulator.game_state.cookies:.0f}")
    print()
    
    # 购买第一个建筑物
    print("购买第一个光标...")
    if simulator.buy_building('Cursor'):
        print("购买成功!")
        print(f"饼干: {simulator.game_state.cookies:.0f}")
        print(f"CPS: {simulator.game_state.cookies_per_second:.1f}")
    else:
        print("购买失败，饼干不足")
    print()
    
    # 模拟1小时
    print("模拟1小时的游戏进程...")
    simulator.simulate_time_period(3600)  # 3600秒 = 1小时
    
    print("1小时后的状态:")
    summary = simulator.get_simulation_summary()
    game_state = summary['game_state']
    stats = summary['simulation_stats']
    
    print(f"饼干: {game_state['cookies']:.0f}")
    print(f"总获得饼干: {game_state['cookies_earned']:.0f}")
    print(f"CPS: {game_state['cookies_per_second']:.1f}")
    print(f"建筑物总数: {game_state['total_buildings']}")
    print(f"升级数量: {game_state['upgrades_owned']}")
    print(f"声望等级: {game_state['prestige']}")
    print()
    
    print("模拟统计:")
    print(f"总模拟时间: {stats['total_time']:.1f}秒")
    print(f"生产的饼干: {stats['cookies_produced']:.0f}")
    print(f"购买的建筑物: {stats['buildings_bought']}")
    print(f"购买的升级: {stats['upgrades_bought']}")
    print()
    
    # 显示CPS分解
    print("CPS详细分解:")
    cps_breakdown = simulator.get_cps_breakdown()
    for source, cps in cps_breakdown.items():
        if isinstance(cps, (int, float)) and cps > 0:
            print(f"  {source}: {cps:.1f}")
    print()
    
    # 显示购买建议
    print("购买建议:")
    recommendations = simulator.get_purchase_recommendations(5)
    for i, option in enumerate(recommendations, 1):
        print(f"  {i}. {option.type.title()}: {option.name}")
        print(f"     价格: {option.price:.0f}, 效率: {option.efficiency:.6f}")
    print()


def strategy_comparison_demo():
    """策略比较演示"""
    print("=== 策略比较演示 ===\n")
    
    # 策略1: 只买最便宜的建筑物
    print("策略1: 只买最便宜的建筑物")
    sim1 = GameSimulator()
    sim1.auto_buy_enabled = False  # 关闭自动购买
    
    # 给一些初始饼干
    sim1.game_state.cookies = 1000
    
    # 手动购买策略：只买光标
    for _ in range(10):
        if sim1.game_state.cookies >= 15:  # 光标价格
            sim1.buy_building('Cursor')
    
    sim1.simulate_time_period(1800)  # 30分钟
    summary1 = sim1.get_simulation_summary()
    
    print(f"30分钟后 - 饼干: {summary1['game_state']['cookies']:.0f}, "
          f"CPS: {summary1['game_state']['cookies_per_second']:.1f}")
    
    # 策略2: 自动优化购买
    print("\n策略2: 自动优化购买")
    sim2 = GameSimulator()
    sim2.game_state.cookies = 1000  # 相同的初始饼干
    sim2.simulate_time_period(1800)  # 30分钟
    summary2 = sim2.get_simulation_summary()
    
    print(f"30分钟后 - 饼干: {summary2['game_state']['cookies']:.0f}, "
          f"CPS: {summary2['game_state']['cookies_per_second']:.1f}")
    
    # 比较结果
    print(f"\n策略比较:")
    print(f"策略1 vs 策略2 饼干比: "
          f"{summary1['game_state']['cookies'] / summary2['game_state']['cookies']:.2f}")
    print(f"策略1 vs 策略2 CPS比: "
          f"{summary1['game_state']['cookies_per_second'] / summary2['game_state']['cookies_per_second']:.2f}")
    print()


def prestige_analysis_demo():
    """声望分析演示"""
    print("=== 声望分析演示 ===\n")
    
    simulator = GameSimulator()
    
    # 快速获得大量饼干用于演示
    simulator.game_state.cookies = 1e15  # 1千万亿饼干
    simulator.game_state.cookies_earned = 1e15
    
    print("模拟重生前状态:")
    print(f"饼干: {simulator.game_state.cookies:.2e}")
    print(f"当前声望: {simulator.game_state.prestige}")
    
    # 计算重生后的声望
    total_cookies = simulator.game_state.cookies_reset + simulator.game_state.cookies_earned
    potential_prestige = int(calculate_prestige(total_cookies))
    prestige_gain = potential_prestige - simulator.game_state.prestige
    
    print(f"重生后声望: {potential_prestige}")
    print(f"声望增长: {prestige_gain}")
    print()
    
    if prestige_gain > 0:
        print("执行重生...")
        simulator.ascend()
        
        print("重生后状态:")
        print(f"饼干: {simulator.game_state.cookies:.0f}")
        print(f"声望等级: {simulator.game_state.prestige}")
        print(f"天堂芯片: {simulator.game_state.heavenly_chips}")
        print(f"声望CPS倍数: {simulator.game_state.get_prestige_multiplier():.2f}")
        print()
        
        # 模拟重生后的发展
        print("重生后模拟1小时...")
        simulator.simulate_time_period(3600)
        
        summary = simulator.get_simulation_summary()
        print(f"1小时后 - 饼干: {summary['game_state']['cookies']:.0f}, "
              f"CPS: {summary['game_state']['cookies_per_second']:.1f}")
    else:
        print("声望增长不足，不建议重生")
    print()


def event_callback_demo():
    """事件回调演示"""
    print("=== 事件回调演示 ===\n")
    
    # 定义事件回调函数
    def on_purchase(game_state, data):
        if data.type == 'building':
            print(f"购买了建筑物: {data.name} (价格: {data.price:.0f})")
        elif data.type == 'upgrade':
            print(f"购买了升级: {data.name} (价格: {data.price:.0f})")
    
    def on_ascension(game_state, prestige_gain):
        print(f"执行重生! 获得 {prestige_gain} 声望等级")
    
    def on_step(game_state, dt):
        # 每100步输出一次状态
        if hasattr(on_step, 'counter'):
            on_step.counter += 1
        else:
            on_step.counter = 1
        
        if on_step.counter % 100 == 0:
            print(f"时间: {game_state.game_time:.0f}s, "
                  f"饼干: {game_state.cookies:.0f}, "
                  f"CPS: {game_state.cookies_per_second:.1f}")
    
    # 创建模拟器并设置回调
    simulator = GameSimulator()
    simulator.set_event_callback('purchase', on_purchase)
    simulator.set_event_callback('ascension', on_ascension)
    simulator.set_event_callback('step', on_step)
    
    # 给一些初始饼干
    simulator.game_state.cookies = 1000
    
    print("开始模拟 (带事件回调)...")
    simulator.simulate_time_period(600)  # 10分钟
    print("模拟完成\n")


if __name__ == "__main__":
    # 运行所有演示
    basic_simulation_demo()
    strategy_comparison_demo()
    prestige_analysis_demo()
    event_callback_demo()
    
    print("=== 演示完成 ===")
    print("你可以使用这个模拟器来:")
    print("1. 测试不同的购买策略")
    print("2. 分析最优重生时机")
    print("3. 预测游戏进度")
    print("4. 优化建筑物配比")
    print("5. 研究升级效果")
