"""
数据可视化演示

展示Cookie Clicker模拟器的图表绘制功能
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from cookie_clicker_sim import GameSimulator, GameState
from cookie_clicker_sim.analysis.visualizer import DataVisualizer
from cookie_clicker_sim.core.buildings import BUILDINGS
from cookie_clicker_sim.core.constants import calculate_prestige


class SimulationDataCollector:
    """模拟数据收集器"""
    
    def __init__(self, simulator):
        self.simulator = simulator
        self.time_data = []
        self.cookies_data = []
        self.cps_data = []
        self.buildings_data = []
        self.prestige_data = []
        
    def collect_data_point(self):
        """收集当前时刻的数据"""
        self.time_data.append(self.simulator.game_state.game_time)
        self.cookies_data.append(self.simulator.game_state.cookies)
        self.cps_data.append(self.simulator.game_state.cookies_per_second)
        self.buildings_data.append(self.simulator.game_state.buildings.copy())
        
        # 计算当前声望
        total_cookies = (self.simulator.game_state.cookies_reset + 
                        self.simulator.game_state.cookies_earned)
        prestige = calculate_prestige(total_cookies)
        self.prestige_data.append(prestige)
    
    def simulate_with_data_collection(self, duration, time_step=60):
        """模拟并收集数据"""
        steps = int(duration / time_step)
        
        # 收集初始数据
        self.collect_data_point()
        
        for i in range(steps):
            self.simulator.simulate_step(time_step)
            self.collect_data_point()
            
            # 每10%进度输出一次
            if (i + 1) % (steps // 10) == 0:
                progress = (i + 1) / steps * 100
                print(f"模拟进度: {progress:.0f}%")


def demo_progress_visualization():
    """演示进度可视化"""
    print("=== 进度可视化演示 ===")
    
    # 创建模拟器和数据收集器
    simulator = GameSimulator()
    collector = SimulationDataCollector(simulator)
    visualizer = DataVisualizer()
    
    # 给一些初始饼干
    simulator.game_state.cookies = 1000
    
    print("开始模拟2小时的游戏进程...")
    collector.simulate_with_data_collection(7200, time_step=120)  # 2小时，每2分钟记录一次
    
    # 绘制进度曲线
    fig1 = visualizer.plot_progress_curve(
        collector.time_data, 
        collector.cookies_data, 
        collector.cps_data,
        "Cookie Clicker 游戏进度曲线 (2小时)"
    )
    
    # 绘制最终建筑物分布
    final_buildings = collector.buildings_data[-1]
    fig2 = visualizer.plot_building_distribution(
        final_buildings,
        "最终建筑物分布"
    )
    
    # 绘制CPS分解
    cps_breakdown = simulator.get_cps_breakdown()
    fig3 = visualizer.plot_cps_breakdown(
        cps_breakdown,
        "CPS来源分析"
    )
    
    print(f"最终状态:")
    print(f"  饼干: {collector.cookies_data[-1]:.0f}")
    print(f"  CPS: {collector.cps_data[-1]:.1f}")
    print(f"  建筑物总数: {sum(final_buildings.values())}")
    
    return [fig1, fig2, fig3]


def demo_efficiency_analysis():
    """演示效率分析"""
    print("\n=== 效率分析演示 ===")
    
    simulator = GameSimulator()
    simulator.game_state.cookies = 1e6  # 给大量饼干用于分析
    visualizer = DataVisualizer()
    
    # 获取购买建议
    recommendations = simulator.get_purchase_recommendations(10)
    efficiency_data = [(option.name, option.efficiency) for option in recommendations]
    
    # 绘制效率对比
    fig1 = visualizer.plot_efficiency_comparison(
        efficiency_data,
        "当前购买效率对比"
    )
    
    # 分析特定建筑物的效率曲线
    building_name = 'Cursor'
    amounts = list(range(0, 50))
    efficiencies = []
    
    for amount in amounts:
        temp_state = simulator.game_state.copy()
        temp_state.buildings[building_name] = amount
        building = BUILDINGS[building_name]
        efficiency = building.get_efficiency(amount, temp_state)
        efficiencies.append(efficiency)
    
    fig2 = visualizer.plot_building_efficiency_curve(
        building_name, amounts, efficiencies
    )
    
    print(f"效率分析完成，共分析了{len(recommendations)}个购买选项")
    
    return [fig1, fig2]


def demo_strategy_comparison():
    """演示策略对比"""
    print("\n=== 策略对比演示 ===")
    
    visualizer = DataVisualizer()
    strategy_results = {}
    
    # 策略1: 只买光标
    print("测试策略1: 只买光标...")
    sim1 = GameSimulator()
    sim1.auto_buy_enabled = False
    sim1.game_state.cookies = 10000
    
    # 手动购买光标
    cursor_count = 0
    while sim1.game_state.cookies >= BUILDINGS['Cursor'].get_price(cursor_count):
        sim1.buy_building('Cursor')
        cursor_count += 1
    
    sim1.simulate_time_period(1800)  # 30分钟
    summary1 = sim1.get_simulation_summary()
    
    strategy_results['只买光标'] = {
        'final_cookies': summary1['game_state']['cookies'],
        'final_cps': summary1['game_state']['cookies_per_second'],
        'total_purchases': summary1['simulation_stats']['buildings_bought'],
        'efficiency': summary1['efficiency_metrics']['cookies_per_hour']
    }
    
    # 策略2: 自动优化
    print("测试策略2: 自动优化...")
    sim2 = GameSimulator()
    sim2.game_state.cookies = 10000
    sim2.simulate_time_period(1800)  # 30分钟
    summary2 = sim2.get_simulation_summary()
    
    strategy_results['自动优化'] = {
        'final_cookies': summary2['game_state']['cookies'],
        'final_cps': summary2['game_state']['cookies_per_second'],
        'total_purchases': (summary2['simulation_stats']['buildings_bought'] + 
                          summary2['simulation_stats']['upgrades_bought']),
        'efficiency': summary2['efficiency_metrics']['cookies_per_hour']
    }
    
    # 策略3: 只买奶奶
    print("测试策略3: 只买奶奶...")
    sim3 = GameSimulator()
    sim3.auto_buy_enabled = False
    sim3.game_state.cookies = 10000
    
    # 手动购买奶奶
    grandma_count = 0
    while sim3.game_state.cookies >= BUILDINGS['Grandma'].get_price(grandma_count):
        sim3.buy_building('Grandma')
        grandma_count += 1
    
    sim3.simulate_time_period(1800)  # 30分钟
    summary3 = sim3.get_simulation_summary()
    
    strategy_results['只买奶奶'] = {
        'final_cookies': summary3['game_state']['cookies'],
        'final_cps': summary3['game_state']['cookies_per_second'],
        'total_purchases': summary3['simulation_stats']['buildings_bought'],
        'efficiency': summary3['efficiency_metrics']['cookies_per_hour']
    }
    
    # 绘制策略对比图
    fig = visualizer.plot_strategy_comparison(
        strategy_results,
        "30分钟策略对比分析"
    )
    
    print("策略对比结果:")
    for strategy, results in strategy_results.items():
        print(f"  {strategy}:")
        print(f"    最终饼干: {results['final_cookies']:.0f}")
        print(f"    最终CPS: {results['final_cps']:.1f}")
        print(f"    购买次数: {results['total_purchases']}")
    
    return [fig]


def demo_prestige_analysis():
    """演示声望分析"""
    print("\n=== 声望分析演示 ===")
    
    simulator = GameSimulator()
    visualizer = DataVisualizer()
    
    # 模拟多次重生的过程
    cookies_history = []
    prestige_history = []
    
    # 快速获得大量饼干进行演示
    cookie_amounts = [1e10, 1e11, 1e12, 1e13, 1e14, 1e15]
    
    for cookies in cookie_amounts:
        simulator.game_state.cookies_earned = cookies
        total_cookies = simulator.game_state.cookies_reset + simulator.game_state.cookies_earned
        prestige = calculate_prestige(total_cookies)
        
        cookies_history.append(total_cookies)
        prestige_history.append(prestige)
    
    # 绘制声望分析图
    fig = visualizer.plot_prestige_analysis(
        cookies_history,
        prestige_history,
        "声望系统分析"
    )
    
    print("声望分析:")
    for i, (cookies, prestige) in enumerate(zip(cookies_history, prestige_history)):
        print(f"  {cookies:.2e} 饼干 -> {prestige:.1f} 声望")
    
    return [fig]


def demo_real_time_simulation():
    """演示实时模拟数据收集"""
    print("\n=== 实时模拟演示 ===")
    
    simulator = GameSimulator()
    collector = SimulationDataCollector(simulator)
    visualizer = DataVisualizer()
    
    # 给一些初始饼干
    simulator.game_state.cookies = 5000
    
    print("开始1小时实时模拟...")
    
    # 分段模拟，每10分钟绘制一次图表
    total_duration = 3600  # 1小时
    segment_duration = 600  # 10分钟
    segments = total_duration // segment_duration
    
    all_figures = []
    
    for segment in range(segments):
        print(f"\n--- 第 {segment + 1}/{segments} 段 (第{(segment + 1) * 10}分钟) ---")
        
        # 模拟这一段
        collector.simulate_with_data_collection(segment_duration, time_step=60)
        
        # 绘制当前进度
        fig = visualizer.plot_progress_curve(
            collector.time_data,
            collector.cookies_data,
            collector.cps_data,
            f"实时进度 - 第{(segment + 1) * 10}分钟"
        )
        
        all_figures.append(fig)
        
        # 显示当前状态
        current_cookies = collector.cookies_data[-1]
        current_cps = collector.cps_data[-1]
        current_buildings = sum(collector.buildings_data[-1].values())
        
        print(f"当前状态: 饼干={current_cookies:.0f}, CPS={current_cps:.1f}, 建筑物={current_buildings}")
    
    print(f"\n实时模拟完成，共生成了{len(all_figures)}个图表")
    return all_figures


def save_all_charts():
    """保存所有图表演示"""
    print("\n=== 保存图表演示 ===")
    
    visualizer = DataVisualizer()
    
    # 运行所有演示并收集图表
    print("生成所有图表...")
    
    figures = []
    figures.extend(demo_progress_visualization())
    figures.extend(demo_efficiency_analysis())
    figures.extend(demo_strategy_comparison())
    figures.extend(demo_prestige_analysis())
    
    # 保存所有图表
    chart_names = [
        "progress_curve.png",
        "building_distribution.png", 
        "cps_breakdown.png",
        "efficiency_comparison.png",
        "building_efficiency_curve.png",
        "strategy_comparison.png",
        "prestige_analysis.png"
    ]
    
    for i, (fig, name) in enumerate(zip(figures, chart_names)):
        filename = f"charts/{name}"
        os.makedirs("charts", exist_ok=True)
        visualizer.save_figure(fig, filename)
    
    print(f"所有图表已保存到 charts/ 目录")


if __name__ == "__main__":
    print("Cookie Clicker 数据可视化演示")
    print("=" * 50)
    
    try:
        # 检查matplotlib是否可用
        import matplotlib.pyplot as plt
        print("✓ matplotlib 可用")
        
        # 运行各种演示
        demo_progress_visualization()
        demo_efficiency_analysis()
        demo_strategy_comparison()
        demo_prestige_analysis()
        
        # 保存图表
        save_all_charts()
        
        print("\n" + "=" * 50)
        print("✓ 所有可视化演示完成!")
        print("\n可视化功能包括:")
        print("1. 📈 游戏进度曲线 (饼干数量和CPS)")
        print("2. 🥧 建筑物分布饼图")
        print("3. 📊 CPS来源分解柱状图")
        print("4. 📉 购买效率对比图")
        print("5. 📈 建筑物效率曲线")
        print("6. 🔄 策略对比分析")
        print("7. ⭐ 声望系统分析")
        print("8. 💾 图表保存功能")
        
        # 显示所有图表
        plt.show()
        
    except ImportError as e:
        print(f"✗ 缺少依赖库: {e}")
        print("请安装: pip install matplotlib seaborn pandas numpy")
    except Exception as e:
        print(f"✗ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
