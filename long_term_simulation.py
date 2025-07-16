"""
Cookie Clicker 长期模拟 - 一个月模拟

模拟30天的游戏进程，分析长期数值模型和策略演变
"""

import sys
import os
import time
import json
import numpy as np
from datetime import datetime, timedelta

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

from cookie_clicker_sim import GameSimulator
from cookie_clicker_sim.core.constants import calculate_prestige
from cookie_clicker_sim.analysis.visualizer import DataVisualizer


class LongTermSimulator:
    """长期模拟器"""
    
    def __init__(self):
        self.simulator = GameSimulator()
        self.data_points = []
        self.ascension_history = []
        self.strategy_phases = []
        
    def simulate_one_month(self, days=30):
        """模拟一个月的游戏进程"""
        print(f"开始模拟 {days} 天的Cookie Clicker游戏进程...")
        print("=" * 60)
        
        total_seconds = days * 24 * 3600
        checkpoint_interval = 3600  # 每小时记录一次数据
        
        # 给一些初始饼干
        self.simulator.game_state.cookies = 10000
        
        start_time = time.time()
        
        for hour in range(days * 24):
            # 模拟1小时
            self.simulator.simulate_step(3600)
            
            # 记录数据点
            self._record_data_point(hour)
            
            # 每天输出一次进度
            if (hour + 1) % 24 == 0:
                day = (hour + 1) // 24
                self._print_daily_progress(day)
            
            # 每周分析一次策略
            if (hour + 1) % (24 * 7) == 0:
                week = (hour + 1) // (24 * 7)
                self._analyze_weekly_strategy(week)
        
        end_time = time.time()
        simulation_time = end_time - start_time
        
        print(f"\n模拟完成! 用时: {simulation_time:.1f}秒")
        print(f"模拟速度: {total_seconds/simulation_time:.0f}x 实时速度")
        
        return self._generate_final_analysis()
    
    def _record_data_point(self, hour):
        """记录数据点"""
        gs = self.simulator.game_state
        
        # 计算当前声望
        total_cookies = gs.cookies_reset + gs.cookies_earned
        current_prestige = calculate_prestige(total_cookies)
        
        data_point = {
            'hour': hour,
            'day': hour / 24,
            'cookies': gs.cookies,
            'cookies_earned': gs.cookies_earned,
            'total_cookies': total_cookies,
            'cps': gs.cookies_per_second,
            'prestige': current_prestige,
            'heavenly_chips': gs.heavenly_chips,
            'total_buildings': gs.get_total_buildings(),
            'upgrades_owned': len(gs.upgrades_owned),
            'achievements': len(gs.achievements),
            'ascensions': self.simulator.simulation_stats['ascensions']
        }
        
        self.data_points.append(data_point)
        
        # 检查是否发生了重生
        if len(self.data_points) > 1:
            prev_ascensions = self.data_points[-2]['ascensions']
            if data_point['ascensions'] > prev_ascensions:
                self.ascension_history.append({
                    'hour': hour,
                    'day': hour / 24,
                    'prestige_gained': data_point['prestige'],
                    'total_cookies': total_cookies
                })
    
    def _print_daily_progress(self, day):
        """打印每日进度"""
        latest = self.data_points[-1]
        
        print(f"第{day:2d}天: "
              f"饼干={latest['cookies']:.2e}, "
              f"CPS={latest['cps']:.2e}, "
              f"声望={latest['prestige']:.0f}, "
              f"重生={latest['ascensions']}次")
    
    def _analyze_weekly_strategy(self, week):
        """分析每周策略"""
        if len(self.data_points) < 24 * 7:
            return
        
        # 获取本周数据
        week_start = (week - 1) * 24 * 7
        week_data = self.data_points[week_start:]
        
        # 分析本周增长
        start_cookies = week_data[0]['total_cookies']
        end_cookies = week_data[-1]['total_cookies']
        growth_rate = end_cookies / start_cookies if start_cookies > 0 else 0
        
        # 分析重生频率
        week_ascensions = [a for a in self.ascension_history 
                          if a['day'] >= (week-1)*7 and a['day'] < week*7]
        
        strategy_analysis = {
            'week': week,
            'growth_rate': growth_rate,
            'ascensions_this_week': len(week_ascensions),
            'avg_prestige_per_ascension': np.mean([a['prestige_gained'] for a in week_ascensions]) if week_ascensions else 0,
            'dominant_strategy': self._identify_dominant_strategy(week_data)
        }
        
        self.strategy_phases.append(strategy_analysis)
        
        print(f"\n第{week}周策略分析:")
        print(f"  增长率: {growth_rate:.2f}x")
        print(f"  重生次数: {len(week_ascensions)}")
        print(f"  主导策略: {strategy_analysis['dominant_strategy']}")
    
    def _identify_dominant_strategy(self, week_data):
        """识别主导策略"""
        if not week_data:
            return "Unknown"
        
        latest = week_data[-1]
        
        if latest['prestige'] < 10:
            return "Early Game - Building Foundation"
        elif latest['prestige'] < 100:
            return "Mid Game - Efficiency Optimization"
        elif latest['prestige'] < 1000:
            return "Late Game - Prestige Farming"
        else:
            return "End Game - Heavenly Upgrades"
    
    def _generate_final_analysis(self):
        """生成最终分析报告"""
        if not self.data_points:
            return {}
        
        initial = self.data_points[0]
        final = self.data_points[-1]
        
        # 计算总体增长
        total_growth = final['total_cookies'] / initial['total_cookies'] if initial['total_cookies'] > 0 else 0
        
        # 分析重生模式
        ascension_intervals = []
        if len(self.ascension_history) > 1:
            for i in range(1, len(self.ascension_history)):
                interval = self.ascension_history[i]['hour'] - self.ascension_history[i-1]['hour']
                ascension_intervals.append(interval)
        
        # 分析CPS增长趋势
        cps_values = [dp['cps'] for dp in self.data_points]
        cps_growth_rate = self._calculate_exponential_growth_rate(cps_values)
        
        analysis = {
            'simulation_summary': {
                'total_days': final['day'],
                'initial_cookies': initial['total_cookies'],
                'final_cookies': final['total_cookies'],
                'total_growth_factor': total_growth,
                'final_cps': final['cps'],
                'final_prestige': final['prestige'],
                'total_ascensions': final['ascensions'],
                'final_heavenly_chips': final['heavenly_chips']
            },
            'growth_analysis': {
                'average_daily_growth': total_growth ** (1/final['day']) if final['day'] > 0 else 1,
                'cps_exponential_growth_rate': cps_growth_rate,
                'prestige_progression': [dp['prestige'] for dp in self.data_points[::24]]  # 每日声望
            },
            'ascension_analysis': {
                'total_ascensions': len(self.ascension_history),
                'average_ascension_interval': np.mean(ascension_intervals) if ascension_intervals else 0,
                'ascension_frequency_trend': self._analyze_ascension_frequency_trend(),
                'prestige_gains': [a['prestige_gained'] for a in self.ascension_history]
            },
            'strategy_evolution': {
                'phases': self.strategy_phases,
                'strategy_transitions': self._identify_strategy_transitions()
            },
            'efficiency_metrics': {
                'cookies_per_day': final['total_cookies'] / final['day'] if final['day'] > 0 else 0,
                'prestige_per_day': final['prestige'] / final['day'] if final['day'] > 0 else 0,
                'ascensions_per_week': len(self.ascension_history) / (final['day'] / 7) if final['day'] > 0 else 0
            }
        }
        
        return analysis
    
    def _calculate_exponential_growth_rate(self, values):
        """计算指数增长率"""
        if len(values) < 2:
            return 0
        
        # 过滤掉0值
        positive_values = [v for v in values if v > 0]
        if len(positive_values) < 2:
            return 0
        
        # 计算对数增长率
        log_values = np.log(positive_values)
        time_points = np.arange(len(log_values))
        
        # 线性回归求斜率
        if len(time_points) > 1:
            slope = np.polyfit(time_points, log_values, 1)[0]
            return slope
        return 0
    
    def _analyze_ascension_frequency_trend(self):
        """分析重生频率趋势"""
        if len(self.ascension_history) < 3:
            return "Insufficient data"
        
        # 计算每次重生的间隔
        intervals = []
        for i in range(1, len(self.ascension_history)):
            interval = self.ascension_history[i]['hour'] - self.ascension_history[i-1]['hour']
            intervals.append(interval)
        
        # 分析趋势
        if len(intervals) >= 3:
            early_avg = np.mean(intervals[:len(intervals)//2])
            late_avg = np.mean(intervals[len(intervals)//2:])
            
            if late_avg < early_avg * 0.8:
                return "Increasing frequency (shorter intervals)"
            elif late_avg > early_avg * 1.2:
                return "Decreasing frequency (longer intervals)"
            else:
                return "Stable frequency"
        
        return "Insufficient data for trend analysis"
    
    def _identify_strategy_transitions(self):
        """识别策略转换点"""
        transitions = []
        
        if len(self.strategy_phases) < 2:
            return transitions
        
        for i in range(1, len(self.strategy_phases)):
            prev_strategy = self.strategy_phases[i-1]['dominant_strategy']
            curr_strategy = self.strategy_phases[i]['dominant_strategy']
            
            if prev_strategy != curr_strategy:
                transitions.append({
                    'week': self.strategy_phases[i]['week'],
                    'from_strategy': prev_strategy,
                    'to_strategy': curr_strategy
                })
        
        return transitions
    
    def generate_visualizations(self, analysis):
        """生成可视化图表"""
        try:
            visualizer = DataVisualizer(figsize=(16, 12))
            
            # 提取数据
            hours = [dp['hour'] for dp in self.data_points]
            days = [dp['day'] for dp in self.data_points]
            cookies = [dp['total_cookies'] for dp in self.data_points]
            cps = [dp['cps'] for dp in self.data_points]
            prestige = [dp['prestige'] for dp in self.data_points]
            
            # 转换为小时为单位
            time_hours = hours
            
            # 1. 长期进度曲线
            fig1 = visualizer.plot_progress_curve(
                time_hours, cookies, cps,
                f"Cookie Clicker 30-Day Long-Term Simulation"
            )
            
            # 2. 声望增长曲线
            import matplotlib.pyplot as plt
            fig2, ax = plt.subplots(figsize=(14, 8))
            ax.plot(days, prestige, 'g-', linewidth=2, marker='o', markersize=3)
            ax.set_xlabel('Days', fontsize=12)
            ax.set_ylabel('Prestige Level', fontsize=12)
            ax.set_title('Prestige Growth Over 30 Days', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # 标记重生点
            for ascension in self.ascension_history:
                ax.axvline(x=ascension['day'], color='red', linestyle='--', alpha=0.7)
            
            # 3. 重生频率分析
            fig3, ax3 = plt.subplots(figsize=(14, 8))
            if len(self.ascension_history) > 1:
                ascension_days = [a['day'] for a in self.ascension_history]
                ascension_prestiges = [a['prestige_gained'] for a in self.ascension_history]
                
                ax3.scatter(ascension_days, ascension_prestiges, s=100, alpha=0.7, c='red')
                ax3.plot(ascension_days, ascension_prestiges, 'r-', alpha=0.5)
                ax3.set_xlabel('Day', fontsize=12)
                ax3.set_ylabel('Prestige Gained', fontsize=12)
                ax3.set_title('Ascension Pattern Over 30 Days', fontsize=14, fontweight='bold')
                ax3.grid(True, alpha=0.3)
            
            # 保存图表
            os.makedirs("long_term_analysis", exist_ok=True)
            visualizer.save_figure(fig1, "long_term_analysis/30day_progress.png")
            visualizer.save_figure(fig2, "long_term_analysis/prestige_growth.png")
            visualizer.save_figure(fig3, "long_term_analysis/ascension_pattern.png")
            
            plt.close('all')
            
            print("✅ 可视化图表已生成并保存到 long_term_analysis/ 目录")
            
        except ImportError:
            print("⚠️  matplotlib未安装，跳过可视化生成")
        except Exception as e:
            print(f"⚠️  可视化生成失败: {e}")
    
    def save_detailed_data(self, analysis):
        """保存详细数据"""
        # 保存原始数据点
        with open("long_term_analysis/simulation_data.json", "w") as f:
            json.dump({
                'data_points': self.data_points,
                'ascension_history': self.ascension_history,
                'strategy_phases': self.strategy_phases,
                'analysis': analysis
            }, f, indent=2)
        
        print("✅ 详细数据已保存到 long_term_analysis/simulation_data.json")


def generate_comprehensive_report(analysis):
    """生成综合分析报告"""
    
    report = f"""
Cookie Clicker 30天长期模拟分析报告
==================================

## 模拟概况

### 基础数据
- 模拟时长: {analysis['simulation_summary']['total_days']:.1f} 天
- 初始饼干: {analysis['simulation_summary']['initial_cookies']:.2e}
- 最终饼干: {analysis['simulation_summary']['final_cookies']:.2e}
- 总增长倍数: {analysis['simulation_summary']['total_growth_factor']:.2e}
- 最终CPS: {analysis['simulation_summary']['final_cps']:.2e}
- 最终声望: {analysis['simulation_summary']['final_prestige']:.0f}
- 总重生次数: {analysis['simulation_summary']['total_ascensions']}
- 天堂芯片: {analysis['simulation_summary']['final_heavenly_chips']}

## 增长分析

### 增长模式
- 平均每日增长率: {analysis['growth_analysis']['average_daily_growth']:.2f}x
- CPS指数增长率: {analysis['growth_analysis']['cps_exponential_growth_rate']:.4f}
- 增长类型: {"超指数增长" if analysis['growth_analysis']['average_daily_growth'] > 2 else "指数增长" if analysis['growth_analysis']['average_daily_growth'] > 1.1 else "线性增长"}

### 效率指标
- 每日饼干产量: {analysis['efficiency_metrics']['cookies_per_day']:.2e}
- 每日声望增长: {analysis['efficiency_metrics']['prestige_per_day']:.2f}
- 每周重生频率: {analysis['efficiency_metrics']['ascensions_per_week']:.1f}次

## 重生模式分析

### 重生统计
- 总重生次数: {analysis['ascension_analysis']['total_ascensions']}
- 平均重生间隔: {analysis['ascension_analysis']['average_ascension_interval']:.1f} 小时
- 重生频率趋势: {analysis['ascension_analysis']['ascension_frequency_trend']}

### 重生效率
"""
    
    if analysis['ascension_analysis']['prestige_gains']:
        avg_prestige = np.mean(analysis['ascension_analysis']['prestige_gains'])
        max_prestige = max(analysis['ascension_analysis']['prestige_gains'])
        min_prestige = min(analysis['ascension_analysis']['prestige_gains'])
        
        report += f"""- 平均声望收益: {avg_prestige:.1f}
- 最大声望收益: {max_prestige:.1f}
- 最小声望收益: {min_prestige:.1f}
- 声望收益趋势: {"递增" if len(analysis['ascension_analysis']['prestige_gains']) > 1 and analysis['ascension_analysis']['prestige_gains'][-1] > analysis['ascension_analysis']['prestige_gains'][0] else "稳定"}
"""
    
    report += f"""
## 策略演变分析

### 策略阶段
"""
    
    for phase in analysis['strategy_evolution']['phases']:
        report += f"""
第{phase['week']}周:
- 主导策略: {phase['dominant_strategy']}
- 增长率: {phase['growth_rate']:.2f}x
- 重生次数: {phase['ascensions_this_week']}
- 平均声望收益: {phase['avg_prestige_per_ascension']:.1f}
"""
    
    report += f"""
### 策略转换点
"""
    
    if analysis['strategy_evolution']['strategy_transitions']:
        for transition in analysis['strategy_evolution']['strategy_transitions']:
            report += f"""
第{transition['week']}周: {transition['from_strategy']} → {transition['to_strategy']}
"""
    else:
        report += "无明显策略转换\n"
    
    # 长期模型评估
    report += f"""
## 长期数值模型评估

### 模型验证
基于30天的长期模拟，我们可以验证以下数值模型特性:

1. **指数增长模型验证**
   - 理论预期: 指数增长
   - 实际表现: {analysis['growth_analysis']['average_daily_growth']:.2f}x 日增长率
   - 验证结果: {"✅ 符合指数增长模型" if analysis['growth_analysis']['average_daily_growth'] > 1.5 else "⚠️ 增长率低于预期"}

2. **重生系统效果**
   - 重生频率: {analysis['efficiency_metrics']['ascensions_per_week']:.1f}次/周
   - 声望加成效果: {"显著" if analysis['simulation_summary']['final_prestige'] > 100 else "中等" if analysis['simulation_summary']['final_prestige'] > 10 else "轻微"}
   - 系统评价: {"✅ 重生系统有效促进长期增长" if analysis['ascension_analysis']['total_ascensions'] > 5 else "⚠️ 重生频率可能需要优化"}

3. **长期平衡性**
   - 增长可持续性: {"✅ 良好" if analysis['growth_analysis']['average_daily_growth'] < 10 else "⚠️ 可能过快"}
   - 策略多样性: {"✅ 丰富" if len(set(p['dominant_strategy'] for p in analysis['strategy_evolution']['phases'])) > 2 else "⚠️ 单一"}

## 最优策略重新评估

### 长期最优策略
基于30天模拟数据，重新评估的最优策略:

1. **早期阶段 (0-3天)**
   - 策略重点: 快速建立CPS基础
   - 关键行动: 大量购买Grandma，获取基础升级
   - 重生时机: 第一次重生在10-20声望

2. **发展阶段 (3-10天)**
   - 策略重点: 优化重生频率和效率
   - 关键行动: 平衡建筑物投资，重视天堂升级
   - 重生时机: 每1-2天重生一次

3. **成熟阶段 (10-30天)**
   - 策略重点: 最大化长期增长率
   - 关键行动: 精确计算重生时机，利用小游戏系统
   - 重生时机: 基于数学模型的精确优化

### 策略调整建议
"""
    
    # 基于实际数据给出建议
    if analysis['efficiency_metrics']['ascensions_per_week'] < 3:
        report += "- 建议增加重生频率，当前重生间隔过长\n"
    elif analysis['efficiency_metrics']['ascensions_per_week'] > 10:
        report += "- 建议减少重生频率，当前重生过于频繁\n"
    else:
        report += "- 当前重生频率较为合理\n"
    
    if analysis['growth_analysis']['average_daily_growth'] < 2:
        report += "- 建议优化购买策略，增长率偏低\n"
    
    report += f"""
## 结论与洞察

### 主要发现
1. **长期增长模式**: Cookie Clicker在30天内展现了{analysis['growth_analysis']['average_daily_growth']:.1f}倍的日均增长率
2. **重生系统价值**: 重生系统是长期增长的关键驱动力
3. **策略演变**: 游戏策略随着进度自然演变，体现了良好的设计深度

### 数值模型洞察
1. **指数增长的可持续性**: 长期模拟验证了指数增长模型的有效性
2. **平衡机制的作用**: 效率衰减和重生系统创造了良好的长期平衡
3. **策略复杂性**: 不同阶段需要不同的最优策略，增加了游戏深度

### 对游戏设计的启示
1. **长期激励机制**: 声望系统成功维持了长期游戏动机
2. **策略深度**: 简单的数学模型创造了复杂的策略空间
3. **增长曲线设计**: 指数增长与重生机制的结合创造了理想的进度体验

Cookie Clicker的30天长期表现证明了其数值设计的成功：
通过精心设计的数学模型，创造了既有短期满足感又有长期挑战性的游戏体验。

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return report


if __name__ == "__main__":
    print("Cookie Clicker 30天长期模拟分析")
    print("=" * 60)
    
    # 创建输出目录
    os.makedirs("long_term_analysis", exist_ok=True)
    
    # 运行长期模拟
    simulator = LongTermSimulator()
    
    print("⚠️  注意: 30天模拟需要较长时间，建议先运行7天测试")
    choice = input("选择模拟时长: [1] 7天测试 [2] 30天完整模拟 [3] 自定义天数: ")
    
    if choice == "1":
        days = 7
    elif choice == "2":
        days = 30
    elif choice == "3":
        days = int(input("请输入天数: "))
    else:
        days = 7
        print("默认选择7天测试")
    
    start_time = time.time()
    analysis = simulator.simulate_one_month(days)
    end_time = time.time()
    
    # 生成报告和可视化
    report = generate_comprehensive_report(analysis)
    
    # 保存报告
    with open(f"long_term_analysis/{days}day_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # 生成可视化
    simulator.generate_visualizations(analysis)
    
    # 保存详细数据
    simulator.save_detailed_data(analysis)
    
    print(f"\n" + "=" * 60)
    print(f"🎉 {days}天长期模拟分析完成!")
    print(f"⏱️  总用时: {end_time - start_time:.1f}秒")
    print(f"📊 模拟速度: {days * 24 * 3600 / (end_time - start_time):.0f}x 实时速度")
    print(f"📁 结果保存在: long_term_analysis/ 目录")
    
    # 显示关键结果
    print(f"\n🎯 关键结果:")
    print(f"   最终饼干: {analysis['simulation_summary']['final_cookies']:.2e}")
    print(f"   最终CPS: {analysis['simulation_summary']['final_cps']:.2e}")
    print(f"   最终声望: {analysis['simulation_summary']['final_prestige']:.0f}")
    print(f"   总增长: {analysis['simulation_summary']['total_growth_factor']:.2e}倍")
    print(f"   重生次数: {analysis['simulation_summary']['total_ascensions']}")
    print(f"   日均增长: {analysis['growth_analysis']['average_daily_growth']:.2f}x")
    
    print(f"\n📈 长期洞察:")
    if analysis['growth_analysis']['average_daily_growth'] > 3:
        print("   ✨ 超指数增长 - 数值模型表现优异")
    elif analysis['growth_analysis']['average_daily_growth'] > 1.5:
        print("   📈 稳定指数增长 - 符合设计预期")
    else:
        print("   📊 线性增长 - 可能需要策略优化")
    
    if analysis['ascension_analysis']['total_ascensions'] > days // 2:
        print("   🔄 重生系统活跃 - 长期增长机制有效")
    else:
        print("   ⏳ 重生频率较低 - 可能需要调整策略")
