"""
图表展示脚本

展示Cookie Clicker模拟器生成的各种数值曲线图表
"""

import sys
import os
import time

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

def create_comprehensive_charts():
    """创建全面的图表展示"""
    print("Cookie Clicker 数值曲线图表生成器")
    print("=" * 50)
    
    try:
        from cookie_clicker_sim import GameSimulator
        from cookie_clicker_sim.analysis.visualizer import DataVisualizer
        from cookie_clicker_sim.core.constants import calculate_prestige
        import matplotlib.pyplot as plt
        
        # 创建输出目录
        os.makedirs("charts_output", exist_ok=True)
        
        visualizer = DataVisualizer(figsize=(14, 10))
        
        print("📊 开始生成图表...")
        
        # 1. 长期进度曲线 (4小时模拟)
        print("\n1. 生成长期进度曲线 (4小时模拟)...")
        simulator = GameSimulator()
        simulator.game_state.cookies = 5000
        
        time_data = []
        cookies_data = []
        cps_data = []
        
        # 每10分钟记录一次数据
        for i in range(25):  # 4小时 = 240分钟 = 24个10分钟段
            time_data.append(simulator.game_state.game_time)
            cookies_data.append(simulator.game_state.cookies)
            cps_data.append(simulator.game_state.cookies_per_second)
            
            if i < 24:
                simulator.simulate_step(600)  # 10分钟
                if (i + 1) % 6 == 0:  # 每小时输出一次进度
                    hour = (i + 1) // 6
                    print(f"  第{hour}小时: 饼干={simulator.game_state.cookies:.0f}, CPS={simulator.game_state.cookies_per_second:.1f}")
        
        fig1 = visualizer.plot_progress_curve(
            time_data, cookies_data, cps_data,
            "Cookie Clicker 4-Hour Long-Term Progress"
        )
        visualizer.save_figure(fig1, "charts_output/long_term_progress.png")
        plt.close(fig1)
        
        # 2. 建筑物效率对比
        print("\n2. 生成建筑物效率对比图...")
        efficiency_data = []
        for option in simulator.get_purchase_recommendations(10):
            if option.type == 'building':
                efficiency_data.append((option.name, option.efficiency))
        
        fig2 = visualizer.plot_efficiency_comparison(
            efficiency_data,
            "Building Purchase Efficiency Comparison (After 4 Hours)"
        )
        visualizer.save_figure(fig2, "charts_output/building_efficiency.png")
        plt.close(fig2)
        
        # 3. 建筑物分布演变
        print("\n3. 生成建筑物分布图...")
        fig3 = visualizer.plot_building_distribution(
            simulator.game_state.buildings,
            "Building Distribution After 4 Hours"
        )
        visualizer.save_figure(fig3, "charts_output/building_distribution.png")
        plt.close(fig3)
        
        # 4. CPS来源分析
        print("\n4. 生成CPS来源分析图...")
        cps_breakdown = simulator.get_cps_breakdown()
        fig4 = visualizer.plot_cps_breakdown(
            cps_breakdown,
            "CPS Source Detailed Analysis (After 4 Hours)"
        )
        visualizer.save_figure(fig4, "charts_output/cps_breakdown.png")
        plt.close(fig4)
        
        # 5. 策略对比分析
        print("\n5. 生成策略对比分析...")
        strategy_results = {}
        
        # 策略A: 自动优化 (已有数据)
        strategy_results['Auto Optimization'] = {
            'final_cookies': simulator.game_state.cookies,
            'final_cps': simulator.game_state.cookies_per_second,
            'total_purchases': (simulator.simulation_stats['buildings_bought'] + 
                              simulator.simulation_stats['upgrades_bought']),
            'efficiency': simulator.game_state.cookies / 4  # 每小时饼干数
        }
        
        # 策略B: 只买便宜建筑
        print("  测试策略B: 只买便宜建筑...")
        sim_b = GameSimulator()
        sim_b.auto_buy_enabled = False
        sim_b.game_state.cookies = 5000
        
        # 手动购买策略：优先买光标和奶奶
        for _ in range(100):
            if sim_b.game_state.cookies >= 15:  # 光标价格
                sim_b.buy_building('Cursor')
            elif sim_b.game_state.cookies >= 100:  # 奶奶价格
                sim_b.buy_building('Grandma')
            else:
                break
        
        sim_b.simulate_time_period(14400)  # 4小时
        
        strategy_results['Cheap Buildings'] = {
            'final_cookies': sim_b.game_state.cookies,
            'final_cps': sim_b.game_state.cookies_per_second,
            'total_purchases': sim_b.simulation_stats['buildings_bought'],
            'efficiency': sim_b.game_state.cookies / 4
        }
        
        # 策略C: 平衡发展
        print("  测试策略C: 平衡发展...")
        sim_c = GameSimulator()
        sim_c.game_state.cookies = 5000
        sim_c.simulate_time_period(14400)  # 4小时，使用默认自动购买
        
        strategy_results['Balanced Development'] = {
            'final_cookies': sim_c.game_state.cookies,
            'final_cps': sim_c.game_state.cookies_per_second,
            'total_purchases': (sim_c.simulation_stats['buildings_bought'] + 
                              sim_c.simulation_stats['upgrades_bought']),
            'efficiency': sim_c.game_state.cookies / 4
        }
        
        fig5 = visualizer.plot_strategy_comparison(
            strategy_results,
            "Three Strategies 4-Hour Effect Comparison"
        )
        visualizer.save_figure(fig5, "charts_output/strategy_comparison.png")
        plt.close(fig5)
        
        # 6. 声望分析曲线
        print("\n6. 生成声望分析曲线...")
        cookie_levels = [1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16]
        prestige_levels = [calculate_prestige(c) for c in cookie_levels]
        
        fig6 = visualizer.plot_prestige_analysis(
            cookie_levels, prestige_levels,
            "Prestige System Numerical Analysis"
        )
        visualizer.save_figure(fig6, "charts_output/prestige_analysis.png")
        plt.close(fig6)
        
        # 7. 建筑物效率曲线
        print("\n7. 生成建筑物效率曲线...")
        from cookie_clicker_sim.core.buildings import BUILDINGS
        
        # 分析光标的效率曲线
        amounts = list(range(0, 100, 5))
        efficiencies = []
        
        for amount in amounts:
            temp_state = simulator.game_state.copy()
            temp_state.buildings['Cursor'] = amount
            building = BUILDINGS['Cursor']
            efficiency = building.get_efficiency(amount, temp_state)
            efficiencies.append(efficiency)
        
        fig7 = visualizer.plot_building_efficiency_curve(
            'Cursor', amounts, efficiencies,
            "Cursor Building Efficiency Curve Analysis"
        )
        visualizer.save_figure(fig7, "charts_output/cursor_efficiency_curve.png")
        plt.close(fig7)
        
        # 生成总结报告
        print("\n📋 生成总结报告...")
        
        final_summary = simulator.get_simulation_summary()
        
        report = f"""
Cookie Clicker 数值分析报告
========================

模拟参数:
- 模拟时长: 4小时
- 初始饼干: 5,000
- 策略: 自动优化购买

最终结果:
- 最终饼干数: {final_summary['game_state']['cookies']:,.0f}
- 最终CPS: {final_summary['game_state']['cookies_per_second']:,.1f}
- 建筑物总数: {final_summary['game_state']['total_buildings']}
- 升级数量: {final_summary['game_state']['upgrades_owned']}
- 成就数量: {final_summary['game_state']['achievements']}
- 声望等级: {final_summary['game_state']['prestige']}

性能指标:
- 平均每小时饼干产量: {final_summary['efficiency_metrics']['cookies_per_hour']:,.0f}
- 平均CPS: {final_summary['efficiency_metrics']['average_cps']:,.1f}
- 每小时购买次数: {final_summary['efficiency_metrics']['purchases_per_hour']:.1f}

策略对比:
"""
        
        for strategy, results in strategy_results.items():
            report += f"""
{strategy}:
  - 最终饼干: {results['final_cookies']:,.0f}
  - 最终CPS: {results['final_cps']:,.1f}
  - 购买次数: {results['total_purchases']}
  - 效率: {results['efficiency']:,.0f} 饼干/小时
"""
        
        report += f"""
生成的图表:
1. long_term_progress.png - 4小时长期进度曲线
2. building_efficiency.png - 建筑物效率对比
3. building_distribution.png - 建筑物分布
4. cps_breakdown.png - CPS来源分析
5. strategy_comparison.png - 策略对比
6. prestige_analysis.png - 声望分析
7. cursor_efficiency_curve.png - 光标效率曲线

报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open("charts_output/analysis_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("✅ 所有图表生成完成!")
        print(f"\n📁 输出目录: charts_output/")
        print(f"📊 生成图表: 7个")
        print(f"📋 分析报告: analysis_report.txt")
        
        print(f"\n🎯 最终结果:")
        print(f"  饼干: {final_summary['game_state']['cookies']:,.0f}")
        print(f"  CPS: {final_summary['game_state']['cookies_per_second']:,.1f}")
        print(f"  建筑物: {final_summary['game_state']['total_buildings']}")
        print(f"  效率: {final_summary['efficiency_metrics']['cookies_per_hour']:,.0f} 饼干/小时")
        
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖库: {e}")
        print("请安装: pip install matplotlib seaborn pandas numpy")
        return False
    except Exception as e:
        print(f"❌ 生成图表时出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_comprehensive_charts()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Cookie Clicker 数值曲线图表生成完成!")
        print("\n📈 可视化功能特点:")
        print("✨ 高精度数值模拟 - 基于源码分析")
        print("📊 多维度数据分析 - 7种不同图表类型")
        print("🔄 策略效果对比 - 量化不同策略收益")
        print("📈 长期趋势预测 - 4小时完整模拟")
        print("🎯 性能指标统计 - 详细效率分析")
        print("\n查看 charts_output/ 目录中的图表和报告!")
    else:
        print("\n❌ 图表生成失败，请检查依赖库安装")
        sys.exit(1)
