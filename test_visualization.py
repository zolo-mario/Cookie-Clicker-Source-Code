"""
可视化功能测试脚本

测试Cookie Clicker模拟器的图表绘制功能
"""

import sys
import os

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

def test_visualization_imports():
    """测试可视化模块导入"""
    print("=== 测试可视化模块导入 ===")
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib 导入成功")
    except ImportError:
        print("✗ matplotlib 未安装，请运行: pip install matplotlib")
        return False
    
    try:
        import seaborn as sns
        print("✓ seaborn 导入成功")
    except ImportError:
        print("✗ seaborn 未安装，请运行: pip install seaborn")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas 导入成功")
    except ImportError:
        print("✗ pandas 未安装，请运行: pip install pandas")
        return False
    
    try:
        import numpy as np
        print("✓ numpy 导入成功")
    except ImportError:
        print("✗ numpy 未安装，请运行: pip install numpy")
        return False
    
    try:
        from cookie_clicker_sim.analysis.visualizer import DataVisualizer
        print("✓ DataVisualizer 导入成功")
        return True
    except ImportError as e:
        print(f"✗ DataVisualizer 导入失败: {e}")
        return False


def test_basic_charts():
    """测试基础图表功能"""
    print("\n=== 测试基础图表功能 ===")
    
    try:
        from cookie_clicker_sim import GameSimulator
        from cookie_clicker_sim.analysis.visualizer import DataVisualizer
        import matplotlib.pyplot as plt
        
        # 创建模拟器和可视化器
        simulator = GameSimulator()
        visualizer = DataVisualizer()
        
        # 模拟一些数据
        simulator.game_state.cookies = 1000
        simulator.simulate_time_period(600)  # 10分钟
        
        # 测试进度曲线
        time_data = [0, 300, 600]
        cookies_data = [1000, 5000, 15000]
        cps_data = [0, 10, 50]
        
        fig1 = visualizer.plot_progress_curve(time_data, cookies_data, cps_data, "测试进度曲线")
        print("✓ 进度曲线绘制成功")
        
        # 测试建筑物分布
        buildings_data = simulator.game_state.buildings
        fig2 = visualizer.plot_building_distribution(buildings_data, "测试建筑物分布")
        print("✓ 建筑物分布图绘制成功")
        
        # 测试CPS分解
        cps_breakdown = simulator.get_cps_breakdown()
        fig3 = visualizer.plot_cps_breakdown(cps_breakdown, "测试CPS分解")
        print("✓ CPS分解图绘制成功")
        
        # 测试效率对比
        recommendations = simulator.get_purchase_recommendations(5)
        efficiency_data = [(option.name, option.efficiency) for option in recommendations]
        fig4 = visualizer.plot_efficiency_comparison(efficiency_data, "测试效率对比")
        print("✓ 效率对比图绘制成功")
        
        # 保存测试图表
        os.makedirs("test_charts", exist_ok=True)
        visualizer.save_figure(fig1, "test_charts/test_progress.png")
        visualizer.save_figure(fig2, "test_charts/test_buildings.png")
        visualizer.save_figure(fig3, "test_charts/test_cps.png")
        visualizer.save_figure(fig4, "test_charts/test_efficiency.png")
        print("✓ 图表保存成功")
        
        # 关闭图表
        plt.close('all')
        print("✓ 图表清理成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 图表测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_advanced_charts():
    """测试高级图表功能"""
    print("\n=== 测试高级图表功能 ===")
    
    try:
        from cookie_clicker_sim import GameSimulator
        from cookie_clicker_sim.analysis.visualizer import DataVisualizer
        from cookie_clicker_sim.core.constants import calculate_prestige
        import matplotlib.pyplot as plt
        
        visualizer = DataVisualizer()
        
        # 测试策略对比
        strategy_results = {
            '策略A': {
                'final_cookies': 1e6,
                'final_cps': 1000,
                'total_purchases': 50,
                'efficiency': 1e5
            },
            '策略B': {
                'final_cookies': 2e6,
                'final_cps': 2000,
                'total_purchases': 75,
                'efficiency': 2e5
            }
        }
        
        fig1 = visualizer.plot_strategy_comparison(strategy_results, "测试策略对比")
        print("✓ 策略对比图绘制成功")
        
        # 测试声望分析
        cookies_data = [1e12, 1e13, 1e14, 1e15]
        prestige_data = [calculate_prestige(c) for c in cookies_data]
        
        fig2 = visualizer.plot_prestige_analysis(cookies_data, prestige_data, "测试声望分析")
        print("✓ 声望分析图绘制成功")
        
        # 测试建筑物效率曲线
        amounts = list(range(0, 20))
        efficiencies = [1.0 / (i + 1) for i in amounts]  # 模拟递减效率
        
        fig3 = visualizer.plot_building_efficiency_curve("测试建筑", amounts, efficiencies)
        print("✓ 效率曲线绘制成功")
        
        # 保存高级图表
        visualizer.save_figure(fig1, "test_charts/test_strategy.png")
        visualizer.save_figure(fig2, "test_charts/test_prestige.png")
        visualizer.save_figure(fig3, "test_charts/test_curve.png")
        print("✓ 高级图表保存成功")
        
        # 关闭图表
        plt.close('all')
        
        return True
        
    except Exception as e:
        print(f"✗ 高级图表测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_collection():
    """测试数据收集功能"""
    print("\n=== 测试数据收集功能 ===")
    
    try:
        from cookie_clicker_sim import GameSimulator
        from cookie_clicker_sim.analysis.visualizer import DataVisualizer
        
        # 创建数据收集器类
        class SimpleDataCollector:
            def __init__(self, simulator):
                self.simulator = simulator
                self.data = {
                    'time': [],
                    'cookies': [],
                    'cps': [],
                    'buildings': []
                }
            
            def collect(self):
                self.data['time'].append(self.simulator.game_state.game_time)
                self.data['cookies'].append(self.simulator.game_state.cookies)
                self.data['cps'].append(self.simulator.game_state.cookies_per_second)
                self.data['buildings'].append(sum(self.simulator.game_state.buildings.values()))
        
        # 模拟数据收集
        simulator = GameSimulator()
        collector = SimpleDataCollector(simulator)
        visualizer = DataVisualizer()
        
        simulator.game_state.cookies = 2000
        
        # 收集30分钟的数据，每分钟一个点
        for minute in range(31):
            collector.collect()
            if minute < 30:
                simulator.simulate_step(60)  # 1分钟
        
        print(f"✓ 收集了 {len(collector.data['time'])} 个数据点")
        
        # 绘制收集的数据
        fig = visualizer.plot_progress_curve(
            collector.data['time'],
            collector.data['cookies'],
            collector.data['cps'],
            "数据收集测试 - 30分钟进度"
        )
        
        visualizer.save_figure(fig, "test_charts/test_collection.png")
        print("✓ 数据收集图表绘制成功")
        
        # 显示数据统计
        print(f"  初始饼干: {collector.data['cookies'][0]:.0f}")
        print(f"  最终饼干: {collector.data['cookies'][-1]:.0f}")
        print(f"  最终CPS: {collector.data['cps'][-1]:.1f}")
        print(f"  最终建筑物: {collector.data['buildings'][-1]}")
        
        import matplotlib.pyplot as plt
        plt.close('all')
        
        return True
        
    except Exception as e:
        print(f"✗ 数据收集测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_quick_demo():
    """运行快速演示"""
    print("\n=== 快速可视化演示 ===")
    
    try:
        from cookie_clicker_sim import GameSimulator
        from cookie_clicker_sim.analysis.visualizer import DataVisualizer
        import matplotlib.pyplot as plt
        
        # 创建模拟器
        simulator = GameSimulator()
        visualizer = DataVisualizer()
        
        # 快速模拟
        simulator.game_state.cookies = 5000
        simulator.simulate_time_period(1800)  # 30分钟
        
        # 获取最终状态
        summary = simulator.get_simulation_summary()
        
        print("快速演示结果:")
        print(f"  最终饼干: {summary['game_state']['cookies']:.0f}")
        print(f"  最终CPS: {summary['game_state']['cookies_per_second']:.1f}")
        print(f"  建筑物总数: {summary['game_state']['total_buildings']}")
        print(f"  购买次数: {summary['simulation_stats']['buildings_bought'] + summary['simulation_stats']['upgrades_bought']}")
        
        # 绘制最终状态图表
        buildings_data = simulator.game_state.buildings
        cps_breakdown = simulator.get_cps_breakdown()
        
        fig1 = visualizer.plot_building_distribution(buildings_data, "快速演示 - 建筑物分布")
        fig2 = visualizer.plot_cps_breakdown(cps_breakdown, "快速演示 - CPS分解")
        
        # 保存演示图表
        visualizer.save_figure(fig1, "test_charts/demo_buildings.png")
        visualizer.save_figure(fig2, "test_charts/demo_cps.png")
        
        print("✓ 快速演示完成，图表已保存")
        
        plt.close('all')
        return True
        
    except Exception as e:
        print(f"✗ 快速演示失败: {e}")
        return False


if __name__ == "__main__":
    print("Cookie Clicker 可视化功能测试")
    print("=" * 40)
    
    # 测试导入
    if not test_visualization_imports():
        print("\n请先安装必要的依赖库:")
        print("pip install matplotlib seaborn pandas numpy")
        sys.exit(1)
    
    # 创建测试目录
    os.makedirs("test_charts", exist_ok=True)
    
    # 运行测试
    tests = [
        test_basic_charts,
        test_advanced_charts,
        test_data_collection,
        run_quick_demo
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n" + "=" * 40)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有可视化功能测试通过!")
        print("\n可用的图表类型:")
        print("📈 进度曲线图 - 显示饼干和CPS随时间变化")
        print("🥧 建筑物分布饼图 - 显示各建筑物数量占比")
        print("📊 CPS分解柱状图 - 显示各CPS来源贡献")
        print("📉 效率对比图 - 显示购买选项效率排序")
        print("📈 效率曲线图 - 显示建筑物效率变化")
        print("🔄 策略对比图 - 对比不同策略效果")
        print("⭐ 声望分析图 - 分析声望与饼干关系")
        print("\n图表已保存到 test_charts/ 目录")
        print("运行完整演示: python cookie_clicker_sim/examples/visualization_demo.py")
    else:
        print("✗ 部分测试失败，请检查依赖库安装")
        print("需要安装: matplotlib, seaborn, pandas, numpy")
