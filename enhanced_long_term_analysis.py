"""
增强版长期分析

修正重生机制，进行更准确的长期数值模型分析
"""

import sys
import os
import time
import math

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

from cookie_clicker_sim import GameSimulator
from cookie_clicker_sim.core.constants import calculate_prestige, calculate_cookies_for_prestige


class EnhancedLongTermAnalyzer:
    """增强版长期分析器"""
    
    def __init__(self):
        self.simulator = GameSimulator()
        self.timeline = []
        self.ascension_log = []
        
    def run_enhanced_simulation(self, days=7):
        """运行增强版模拟"""
        print(f"开始增强版 {days} 天长期模拟...")
        print("=" * 50)
        
        # 初始设置
        self.simulator.game_state.cookies = 10000
        self.simulator.auto_ascend_enabled = False  # 手动控制重生
        
        total_hours = days * 24
        
        for hour in range(total_hours):
            # 模拟1小时
            self.simulator.simulate_step(3600)
            
            # 记录数据
            self._record_timeline_data(hour)
            
            # 检查重生条件
            self._check_ascension_opportunity(hour)
            
            # 每天输出进度
            if (hour + 1) % 24 == 0:
                day = (hour + 1) // 24
                self._print_daily_summary(day)
        
        return self._generate_enhanced_analysis()
    
    def _record_timeline_data(self, hour):
        """记录时间线数据"""
        gs = self.simulator.game_state
        total_cookies = gs.cookies_reset + gs.cookies_earned
        current_prestige = calculate_prestige(total_cookies)
        
        data = {
            'hour': hour,
            'day': hour / 24,
            'cookies': gs.cookies,
            'cookies_earned': gs.cookies_earned,
            'total_cookies': total_cookies,
            'cps': gs.cookies_per_second,
            'prestige': current_prestige,
            'heavenly_chips': gs.heavenly_chips,
            'buildings': gs.get_total_buildings(),
            'upgrades': len(gs.upgrades_owned),
            'ascensions': len(self.ascension_log)
        }
        
        self.timeline.append(data)
    
    def _check_ascension_opportunity(self, hour):
        """检查重生机会"""
        gs = self.simulator.game_state
        total_cookies = gs.cookies_reset + gs.cookies_earned
        potential_prestige = calculate_prestige(total_cookies)
        current_prestige = gs.prestige
        
        # 重生条件：能获得至少5个声望等级，或者当前声望的50%
        prestige_gain = potential_prestige - current_prestige
        min_gain_threshold = max(5, current_prestige * 0.5)
        
        # 额外条件：至少游戏了6小时
        if hour >= 6 and prestige_gain >= min_gain_threshold:
            self._perform_ascension(hour, prestige_gain)
    
    def _perform_ascension(self, hour, prestige_gain):
        """执行重生"""
        gs = self.simulator.game_state
        
        # 记录重生信息
        ascension_info = {
            'hour': hour,
            'day': hour / 24,
            'prestige_before': gs.prestige,
            'prestige_gained': prestige_gain,
            'total_cookies': gs.cookies_reset + gs.cookies_earned,
            'heavenly_chips_before': gs.heavenly_chips
        }
        
        # 执行重生
        self.simulator.ascend()
        
        # 更新重生信息
        ascension_info['prestige_after'] = gs.prestige
        ascension_info['heavenly_chips_after'] = gs.heavenly_chips
        
        self.ascension_log.append(ascension_info)
        
        print(f"  🔄 第{hour}小时重生: +{prestige_gain:.1f}声望 (总计{gs.prestige:.0f})")
    
    def _print_daily_summary(self, day):
        """打印每日总结"""
        latest = self.timeline[-1]
        
        print(f"第{day:2d}天: "
              f"饼干={latest['cookies']:.2e}, "
              f"CPS={latest['cps']:.2e}, "
              f"声望={latest['prestige']:.0f}, "
              f"重生={latest['ascensions']}次")
    
    def _generate_enhanced_analysis(self):
        """生成增强分析"""
        if not self.timeline:
            return {}
        
        initial = self.timeline[0]
        final = self.timeline[-1]
        
        # 计算增长指标
        total_growth = final['total_cookies'] / max(initial['total_cookies'], 1)
        daily_growth = total_growth ** (1 / final['day']) if final['day'] > 0 else 1
        
        # 分析CPS增长趋势
        cps_values = [t['cps'] for t in self.timeline if t['cps'] > 0]
        cps_growth_rate = self._calculate_exponential_rate(cps_values)
        
        # 分析重生效率
        ascension_analysis = self._analyze_ascensions()
        
        # 分析不同阶段的表现
        phase_analysis = self._analyze_game_phases()
        
        return {
            'simulation_summary': {
                'total_days': final['day'],
                'initial_cookies': initial['total_cookies'],
                'final_cookies': final['total_cookies'],
                'total_growth_factor': total_growth,
                'daily_growth_rate': daily_growth,
                'final_cps': final['cps'],
                'final_prestige': final['prestige'],
                'total_ascensions': len(self.ascension_log),
                'final_heavenly_chips': final['heavenly_chips']
            },
            'growth_metrics': {
                'cps_exponential_rate': cps_growth_rate,
                'prestige_progression_rate': final['prestige'] / final['day'] if final['day'] > 0 else 0,
                'ascension_frequency': len(self.ascension_log) / (final['day'] / 7) if final['day'] > 0 else 0
            },
            'ascension_analysis': ascension_analysis,
            'phase_analysis': phase_analysis,
            'efficiency_metrics': self._calculate_efficiency_metrics()
        }
    
    def _calculate_exponential_rate(self, values):
        """计算指数增长率"""
        if len(values) < 2:
            return 0
        
        # 使用对数回归
        import numpy as np
        log_values = [math.log(max(v, 1)) for v in values]
        x = np.arange(len(log_values))
        
        if len(x) > 1:
            slope = np.polyfit(x, log_values, 1)[0]
            return slope
        return 0
    
    def _analyze_ascensions(self):
        """分析重生模式"""
        if not self.ascension_log:
            return {
                'total_ascensions': 0,
                'average_interval': 0,
                'average_prestige_gain': 0,
                'efficiency_trend': 'No ascensions'
            }
        
        # 计算重生间隔
        intervals = []
        for i in range(1, len(self.ascension_log)):
            interval = self.ascension_log[i]['hour'] - self.ascension_log[i-1]['hour']
            intervals.append(interval)
        
        # 计算声望收益
        prestige_gains = [a['prestige_gained'] for a in self.ascension_log]
        
        # 分析效率趋势
        if len(prestige_gains) >= 3:
            early_avg = sum(prestige_gains[:len(prestige_gains)//2]) / (len(prestige_gains)//2)
            late_avg = sum(prestige_gains[len(prestige_gains)//2:]) / (len(prestige_gains) - len(prestige_gains)//2)
            
            if late_avg > early_avg * 1.5:
                efficiency_trend = "Improving (increasing prestige gains)"
            elif late_avg < early_avg * 0.7:
                efficiency_trend = "Declining (decreasing prestige gains)"
            else:
                efficiency_trend = "Stable"
        else:
            efficiency_trend = "Insufficient data"
        
        return {
            'total_ascensions': len(self.ascension_log),
            'average_interval': sum(intervals) / len(intervals) if intervals else 0,
            'average_prestige_gain': sum(prestige_gains) / len(prestige_gains),
            'prestige_gains': prestige_gains,
            'efficiency_trend': efficiency_trend,
            'first_ascension_hour': self.ascension_log[0]['hour'] if self.ascension_log else None
        }
    
    def _analyze_game_phases(self):
        """分析游戏阶段"""
        phases = {
            'early_game': {'hours': '0-24', 'data': []},
            'mid_game': {'hours': '24-72', 'data': []},
            'late_game': {'hours': '72+', 'data': []}
        }
        
        for data in self.timeline:
            hour = data['hour']
            if hour < 24:
                phases['early_game']['data'].append(data)
            elif hour < 72:
                phases['mid_game']['data'].append(data)
            else:
                phases['late_game']['data'].append(data)
        
        # 分析每个阶段的特征
        for phase_name, phase_info in phases.items():
            if phase_info['data']:
                start_data = phase_info['data'][0]
                end_data = phase_info['data'][-1]
                
                phase_growth = end_data['total_cookies'] / max(start_data['total_cookies'], 1)
                phase_duration = end_data['hour'] - start_data['hour']
                
                phase_info['analysis'] = {
                    'duration_hours': phase_duration,
                    'growth_factor': phase_growth,
                    'hourly_growth_rate': phase_growth ** (1/phase_duration) if phase_duration > 0 else 1,
                    'cps_start': start_data['cps'],
                    'cps_end': end_data['cps'],
                    'prestige_gained': end_data['prestige'] - start_data['prestige']
                }
            else:
                phase_info['analysis'] = None
        
        return phases
    
    def _calculate_efficiency_metrics(self):
        """计算效率指标"""
        if not self.timeline:
            return {}
        
        final = self.timeline[-1]
        
        # 计算各种效率指标
        cookies_per_hour = final['total_cookies'] / final['hour'] if final['hour'] > 0 else 0
        prestige_per_hour = final['prestige'] / final['hour'] if final['hour'] > 0 else 0
        
        # 计算重生效率
        if self.ascension_log:
            total_prestige_gained = sum(a['prestige_gained'] for a in self.ascension_log)
            prestige_per_ascension = total_prestige_gained / len(self.ascension_log)
        else:
            prestige_per_ascension = 0
        
        return {
            'cookies_per_hour': cookies_per_hour,
            'prestige_per_hour': prestige_per_hour,
            'prestige_per_ascension': prestige_per_ascension,
            'cps_efficiency': final['cps'] / max(final['buildings'], 1),
            'heavenly_chip_efficiency': final['heavenly_chips'] / max(final['hour'], 1)
        }


def generate_enhanced_report(analysis):
    """生成增强分析报告"""
    
    report = f"""
Cookie Clicker 增强版长期分析报告
================================

## 📊 模拟概况

### 基础数据
- 模拟时长: {analysis['simulation_summary']['total_days']:.1f} 天
- 初始饼干: {analysis['simulation_summary']['initial_cookies']:.2e}
- 最终饼干: {analysis['simulation_summary']['final_cookies']:.2e}
- 总增长倍数: {analysis['simulation_summary']['total_growth_factor']:.2e}
- 日均增长率: {analysis['simulation_summary']['daily_growth_rate']:.2f}x
- 最终CPS: {analysis['simulation_summary']['final_cps']:.2e}
- 最终声望: {analysis['simulation_summary']['final_prestige']:.0f}
- 总重生次数: {analysis['simulation_summary']['total_ascensions']}

## 📈 增长模式分析

### 增长特征
- CPS指数增长率: {analysis['growth_metrics']['cps_exponential_rate']:.4f}
- 声望增长率: {analysis['growth_metrics']['prestige_progression_rate']:.2f}/天
- 重生频率: {analysis['growth_metrics']['ascension_frequency']:.1f}次/周

### 增长类型判定
"""
    
    daily_growth = analysis['simulation_summary']['daily_growth_rate']
    if daily_growth > 3:
        growth_type = "🚀 超指数增长"
        growth_assessment = "优异"
    elif daily_growth > 1.5:
        growth_type = "📈 指数增长"
        growth_assessment = "良好"
    elif daily_growth > 1.1:
        growth_type = "📊 亚指数增长"
        growth_assessment = "中等"
    else:
        growth_type = "📉 线性增长"
        growth_assessment = "需要优化"
    
    report += f"- 增长类型: {growth_type}\n"
    report += f"- 表现评估: {growth_assessment}\n"
    
    # 重生分析
    ascension = analysis['ascension_analysis']
    report += f"""
## 🔄 重生系统分析

### 重生统计
- 总重生次数: {ascension['total_ascensions']}
- 平均重生间隔: {ascension['average_interval']:.1f} 小时
- 平均声望收益: {ascension['average_prestige_gain']:.1f}
- 效率趋势: {ascension['efficiency_trend']}
"""
    
    if ascension['first_ascension_hour']:
        report += f"- 首次重生时机: 第{ascension['first_ascension_hour']}小时\n"
    
    # 阶段分析
    phases = analysis['phase_analysis']
    report += f"""
## 🎮 游戏阶段分析

### 早期阶段 (0-24小时)
"""
    
    if phases['early_game']['analysis']:
        early = phases['early_game']['analysis']
        report += f"""- 持续时间: {early['duration_hours']:.0f} 小时
- 增长倍数: {early['growth_factor']:.2f}x
- 小时增长率: {early['hourly_growth_rate']:.2f}x
- CPS增长: {early['cps_start']:.2e} → {early['cps_end']:.2e}
- 声望获得: {early['prestige_gained']:.1f}
"""
    
    report += f"""
### 中期阶段 (24-72小时)
"""
    
    if phases['mid_game']['analysis']:
        mid = phases['mid_game']['analysis']
        report += f"""- 持续时间: {mid['duration_hours']:.0f} 小时
- 增长倍数: {mid['growth_factor']:.2f}x
- 小时增长率: {mid['hourly_growth_rate']:.2f}x
- CPS增长: {mid['cps_start']:.2e} → {mid['cps_end']:.2e}
- 声望获得: {mid['prestige_gained']:.1f}
"""
    
    # 效率指标
    efficiency = analysis['efficiency_metrics']
    report += f"""
## ⚡ 效率指标分析

### 核心效率
- 饼干产出效率: {efficiency['cookies_per_hour']:.2e} 饼干/小时
- 声望获得效率: {efficiency['prestige_per_hour']:.2f} 声望/小时
- 单次重生效率: {efficiency['prestige_per_ascension']:.1f} 声望/次
- CPS建筑效率: {efficiency['cps_efficiency']:.2e} CPS/建筑
- 天堂芯片效率: {efficiency['heavenly_chip_efficiency']:.2f} 芯片/小时

## 🎯 数值模型重新评估

### 长期增长模型验证
"""
    
    # 模型验证
    if daily_growth > 2:
        report += "✅ **指数增长模型得到验证** - 长期增长表现符合预期\n"
    else:
        report += "⚠️ **增长模型需要调整** - 实际增长低于理论预期\n"
    
    if ascension['total_ascensions'] > 0:
        report += "✅ **重生系统有效运作** - 重生机制促进了长期增长\n"
    else:
        report += "❌ **重生系统未激活** - 需要调整重生策略\n"
    
    # 策略建议
    report += f"""
## 💡 最优策略重新评估

### 基于长期数据的策略调整
"""
    
    if ascension['total_ascensions'] == 0:
        report += """
1. **重生策略调整**
   - 当前问题: 未进行重生，错失长期增长机会
   - 建议: 在获得10-20声望时进行首次重生
   - 理由: 重生是长期增长的关键驱动力
"""
    elif ascension['average_interval'] > 48:
        report += """
1. **重生频率优化**
   - 当前问题: 重生间隔过长
   - 建议: 缩短重生间隔至24-36小时
   - 理由: 更频繁的重生能带来更好的长期收益
"""
    
    if daily_growth < 1.5:
        report += """
2. **购买策略优化**
   - 当前问题: 增长率偏低
   - 建议: 更严格地执行效率优先策略
   - 理由: 数据显示当前策略效率有待提升
"""
    
    # 数值模型洞察
    report += f"""
## 🔬 数值模型深度洞察

### 长期平衡性评估
1. **增长可持续性**: {"✅ 优秀" if daily_growth > 2 and daily_growth < 10 else "⚠️ 需要调整"}
2. **重生系统平衡**: {"✅ 良好" if 0 < ascension['total_ascensions'] < 20 else "⚠️ 需要优化"}
3. **策略复杂性**: {"✅ 丰富" if len(phases) > 1 else "⚠️ 单一"}

### 设计成功要素
- **指数增长机制**: {"有效" if daily_growth > 1.5 else "需要改进"}
- **重生激励系统**: {"成功" if ascension['total_ascensions'] > 0 else "失效"}
- **长期可玩性**: {"优秀" if analysis['simulation_summary']['final_prestige'] > 50 else "中等"}

## 📋 结论与建议

### 主要发现
1. **长期增长模式**: {growth_type}，日均增长{daily_growth:.2f}倍
2. **重生系统效果**: {"关键驱动力" if ascension['total_ascensions'] > 0 else "未充分利用"}
3. **策略优化空间**: {"较小" if daily_growth > 3 else "较大"}

### 对数值设计的启示
1. **重生阈值设计**: {"合理" if ascension['total_ascensions'] > 0 else "过高，需要降低"}
2. **增长曲线平衡**: {"良好" if 1.5 < daily_growth < 5 else "需要调整"}
3. **长期激励机制**: {"有效" if analysis['simulation_summary']['final_prestige'] > 20 else "需要加强"}

Cookie Clicker的长期表现{"验证了其数值设计的成功" if daily_growth > 2 else "揭示了数值设计的改进空间"}。
通过{analysis['simulation_summary']['total_days']:.0f}天的深度模拟，我们看到了{"一个精心设计的增长系统" if daily_growth > 2 else "一个需要优化的增长系统"}。

生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return report


if __name__ == "__main__":
    print("Cookie Clicker 增强版长期分析")
    print("=" * 50)
    
    # 创建分析器
    analyzer = EnhancedLongTermAnalyzer()
    
    # 运行模拟
    start_time = time.time()
    analysis = analyzer.run_enhanced_simulation(7)  # 7天测试
    end_time = time.time()
    
    # 生成报告
    report = generate_enhanced_report(analysis)
    
    # 保存报告
    os.makedirs("enhanced_analysis", exist_ok=True)
    with open("enhanced_analysis/enhanced_7day_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n" + "=" * 50)
    print("🎉 增强版长期分析完成!")
    print(f"⏱️  用时: {end_time - start_time:.1f}秒")
    print(f"📁 报告保存在: enhanced_analysis/enhanced_7day_report.txt")
    
    # 显示关键结果
    print(f"\n🎯 关键发现:")
    print(f"   最终饼干: {analysis['simulation_summary']['final_cookies']:.2e}")
    print(f"   日均增长: {analysis['simulation_summary']['daily_growth_rate']:.2f}x")
    print(f"   最终声望: {analysis['simulation_summary']['final_prestige']:.0f}")
    print(f"   重生次数: {analysis['simulation_summary']['total_ascensions']}")
    
    # 评估结果
    daily_growth = analysis['simulation_summary']['daily_growth_rate']
    ascensions = analysis['simulation_summary']['total_ascensions']
    
    print(f"\n📊 模型评估:")
    if daily_growth > 2:
        print("   ✅ 指数增长模型验证成功")
    else:
        print("   ⚠️ 增长率低于预期，需要策略优化")
    
    if ascensions > 0:
        print("   ✅ 重生系统正常运作")
    else:
        print("   ❌ 重生系统未激活，需要调整阈值")
    
    print(f"\n💡 主要建议:")
    if ascensions == 0:
        print("   🔄 降低重生阈值，激活重生系统")
    if daily_growth < 1.5:
        print("   📈 优化购买策略，提高增长效率")
    if daily_growth > 2 and ascensions > 0:
        print("   🎉 当前策略表现良好，可继续优化细节")
