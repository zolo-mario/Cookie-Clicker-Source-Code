"""
Cookie Clicker 模拟器测试脚本

快速测试模拟器的基本功能
"""

import sys
import os

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

try:
    from cookie_clicker_sim import GameSimulator, GameState
    from cookie_clicker_sim.core.buildings import BUILDINGS
    from cookie_clicker_sim.core.upgrades import UPGRADES
    from cookie_clicker_sim.core.constants import calculate_prestige
    
    print("✓ 模块导入成功")
except ImportError as e:
    print(f"✗ 模块导入失败: {e}")
    sys.exit(1)


def test_basic_functionality():
    """测试基本功能"""
    print("\n=== 测试基本功能 ===")
    
    # 创建游戏状态
    game_state = GameState()
    print(f"✓ 游戏状态创建成功: {game_state}")
    
    # 测试建筑物
    print(f"✓ 建筑物数量: {len(BUILDINGS)}")
    for name, building in list(BUILDINGS.items())[:3]:
        print(f"  - {name}: 价格={building.base_price}, CPS={building.base_cps}")
    
    # 测试升级
    print(f"✓ 升级数量: {len(UPGRADES)}")
    for name, upgrade in list(UPGRADES.items())[:3]:
        print(f"  - {name}: 价格={upgrade.price}")
    
    # 测试声望计算
    test_cookies = 1e12
    prestige = calculate_prestige(test_cookies)
    print(f"✓ 声望计算: {test_cookies:.0e} 饼干 = {prestige:.2f} 声望")


def test_simulator():
    """测试模拟器"""
    print("\n=== 测试模拟器 ===")
    
    # 创建模拟器
    simulator = GameSimulator()
    print(f"✓ 模拟器创建成功: {simulator}")
    
    # 测试点击
    initial_cookies = simulator.game_state.cookies
    simulator.click_cookie(10)
    print(f"✓ 点击测试: {initial_cookies} -> {simulator.game_state.cookies}")
    
    # 测试购买建筑物
    simulator.game_state.cookies = 1000  # 给足够的饼干
    initial_cursors = simulator.game_state.get_building_count('Cursor')
    success = simulator.buy_building('Cursor')
    new_cursors = simulator.game_state.get_building_count('Cursor')
    print(f"✓ 建筑物购买: {success}, 光标数量 {initial_cursors} -> {new_cursors}")
    
    # 测试CPS计算
    cps = simulator.cps_calculator.calculate_total_cps(simulator.game_state)
    print(f"✓ CPS计算: {cps:.2f}")
    
    # 测试模拟步骤
    initial_time = simulator.game_state.game_time
    simulator.simulate_step(10.0)  # 模拟10秒
    new_time = simulator.game_state.game_time
    print(f"✓ 模拟步骤: 时间 {initial_time} -> {new_time}")


def test_optimization():
    """测试优化功能"""
    print("\n=== 测试优化功能 ===")
    
    simulator = GameSimulator()
    simulator.game_state.cookies = 10000  # 给足够的饼干
    
    # 测试购买建议
    recommendations = simulator.get_purchase_recommendations(3)
    print(f"✓ 购买建议数量: {len(recommendations)}")
    for i, option in enumerate(recommendations, 1):
        print(f"  {i}. {option.type}: {option.name} (效率: {option.efficiency:.6f})")
    
    # 测试最佳购买
    best_option = simulator.purchase_optimizer.get_best_purchase(simulator.game_state)
    if best_option:
        print(f"✓ 最佳购买: {best_option.type} - {best_option.name}")
    else:
        print("✓ 无可购买项目")


def test_simulation_period():
    """测试时间段模拟"""
    print("\n=== 测试时间段模拟 ===")
    
    simulator = GameSimulator()
    simulator.game_state.cookies = 100  # 给一些初始饼干
    
    # 记录初始状态
    initial_state = {
        'cookies': simulator.game_state.cookies,
        'cps': simulator.game_state.cookies_per_second,
        'buildings': simulator.game_state.get_total_buildings()
    }
    
    # 模拟1分钟
    simulator.simulate_time_period(60)
    
    # 记录最终状态
    final_state = {
        'cookies': simulator.game_state.cookies,
        'cps': simulator.game_state.cookies_per_second,
        'buildings': simulator.game_state.get_total_buildings()
    }
    
    print(f"✓ 1分钟模拟完成:")
    print(f"  饼干: {initial_state['cookies']:.0f} -> {final_state['cookies']:.0f}")
    print(f"  CPS: {initial_state['cps']:.1f} -> {final_state['cps']:.1f}")
    print(f"  建筑物: {initial_state['buildings']} -> {final_state['buildings']}")
    
    # 获取模拟总结
    summary = simulator.get_simulation_summary()
    stats = summary['simulation_stats']
    print(f"  购买的建筑物: {stats['buildings_bought']}")
    print(f"  购买的升级: {stats['upgrades_bought']}")


def test_save_load():
    """测试保存和加载"""
    print("\n=== 测试保存和加载 ===")
    
    # 创建模拟器并运行一段时间
    simulator1 = GameSimulator()
    simulator1.game_state.cookies = 1000
    simulator1.simulate_time_period(30)
    
    # 保存状态
    saved_state = simulator1.save_state()
    print(f"✓ 状态保存成功")
    
    # 创建新模拟器并加载状态
    simulator2 = GameSimulator()
    simulator2.load_state(saved_state)
    print(f"✓ 状态加载成功")
    
    # 验证状态一致性
    state1 = simulator1.game_state
    state2 = simulator2.game_state
    
    cookies_match = abs(state1.cookies - state2.cookies) < 0.01
    cps_match = abs(state1.cookies_per_second - state2.cookies_per_second) < 0.01
    buildings_match = state1.buildings == state2.buildings
    
    print(f"  饼干匹配: {cookies_match}")
    print(f"  CPS匹配: {cps_match}")
    print(f"  建筑物匹配: {buildings_match}")
    
    if cookies_match and cps_match and buildings_match:
        print("✓ 保存/加载测试通过")
    else:
        print("✗ 保存/加载测试失败")


def run_performance_test():
    """运行性能测试"""
    print("\n=== 性能测试 ===")
    
    import time
    
    simulator = GameSimulator()
    simulator.game_state.cookies = 1e6  # 给大量饼干以触发更多购买
    
    # 测试模拟性能
    start_time = time.time()
    simulator.simulate_time_period(3600)  # 模拟1小时
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    simulation_ratio = 3600 / elapsed_time  # 模拟时间/实际时间
    
    print(f"✓ 性能测试完成:")
    print(f"  模拟1小时用时: {elapsed_time:.3f}秒")
    print(f"  模拟速度: {simulation_ratio:.0f}x 实时")
    
    # 显示最终状态
    summary = simulator.get_simulation_summary()
    game_state = summary['game_state']
    stats = summary['simulation_stats']
    
    print(f"  最终饼干: {game_state['cookies']:.2e}")
    print(f"  最终CPS: {game_state['cookies_per_second']:.2e}")
    print(f"  建筑物总数: {game_state['total_buildings']}")
    print(f"  购买次数: {stats['buildings_bought'] + stats['upgrades_bought']}")


if __name__ == "__main__":
    print("Cookie Clicker 模拟器测试")
    print("=" * 40)
    
    try:
        test_basic_functionality()
        test_simulator()
        test_optimization()
        test_simulation_period()
        test_save_load()
        run_performance_test()
        
        print("\n" + "=" * 40)
        print("✓ 所有测试完成!")
        print("\n模拟器已准备就绪，可以开始使用。")
        print("运行示例: python cookie_clicker_sim/examples/basic_simulation.py")
        
    except Exception as e:
        print(f"\n✗ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
