"""
Cookie Clicker 游戏寿命分析

分析数值模型能支撑玩家游玩多久，包括技术限制、心理限制和设计限制
"""

import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

from cookie_clicker_sim.core.constants import calculate_prestige, calculate_cookies_for_prestige


class GameLongevityAnalyzer:
    """游戏寿命分析器"""
    
    def __init__(self):
        # JavaScript数值限制
        self.max_safe_integer = 2**53 - 1  # 9,007,199,254,740,991
        self.max_double = 1.7976931348623157e+308  # IEEE 754双精度最大值
        
        # 游戏内部限制
        self.max_building_amount = 5000  # 游戏设定的建筑物上限
        self.max_reasonable_prestige = 1000000  # 合理的声望上限
        
        # 心理学限制
        self.attention_span_days = 365  # 一般玩家注意力持续时间
        self.hardcore_player_days = 365 * 3  # 硬核玩家可能的游戏时间
        
    def analyze_technical_limits(self):
        """分析技术限制"""
        print("=== 技术限制分析 ===")
        
        # 1. JavaScript数值精度限制
        max_cookies_safe = self.max_safe_integer
        max_prestige_safe = calculate_prestige(max_cookies_safe)
        
        print(f"JavaScript安全整数限制:")
        print(f"  最大饼干数: {max_cookies_safe:.2e}")
        print(f"  对应声望: {max_prestige_safe:.0f}")
        
        # 2. 双精度浮点数限制
        max_cookies_double = self.max_double
        max_prestige_double = calculate_prestige(max_cookies_double)
        
        print(f"\n双精度浮点数限制:")
        print(f"  最大饼干数: {max_cookies_double:.2e}")
        print(f"  对应声望: {max_prestige_double:.0f}")
        
        # 3. 建筑物数量限制
        print(f"\n建筑物数量限制:")
        print(f"  最大建筑物数量: {self.max_building_amount}")
        
        # 计算达到这些限制需要的时间
        return {
            'safe_integer_limit': {
                'cookies': max_cookies_safe,
                'prestige': max_prestige_safe,
                'estimated_days': self._estimate_days_to_reach(max_cookies_safe)
            },
            'double_precision_limit': {
                'cookies': max_cookies_double,
                'prestige': max_prestige_double,
                'estimated_days': self._estimate_days_to_reach(max_cookies_double)
            },
            'building_limit': {
                'max_buildings': self.max_building_amount,
                'estimated_days': self._estimate_days_for_max_buildings()
            }
        }
    
    def _estimate_days_to_reach(self, target_cookies):
        """估算达到目标饼干数需要的天数"""
        # 基于我们的长期模拟数据：日均增长108倍
        daily_growth_rate = 108.45
        
        # 假设从1e12饼干开始（首次重生后的合理起点）
        starting_cookies = 1e12
        
        if target_cookies <= starting_cookies:
            return 0
        
        # 计算需要的天数：target = start * growth^days
        days_needed = math.log(target_cookies / starting_cookies) / math.log(daily_growth_rate)
        
        return max(0, days_needed)
    
    def _estimate_days_for_max_buildings(self):
        """估算达到最大建筑物数量需要的天数"""
        # 假设每天能购买50个建筑物（基于模拟数据）
        buildings_per_day = 50
        days_needed = self.max_building_amount / buildings_per_day
        return days_needed
    
    def analyze_psychological_limits(self):
        """分析心理学限制"""
        print("\n=== 心理学限制分析 ===")
        
        # 1. 数字增长的心理满足感衰减
        satisfaction_curve = self._calculate_satisfaction_curve()
        
        # 2. 重复性操作的疲劳度
        repetition_fatigue = self._calculate_repetition_fatigue()
        
        # 3. 成就感递减
        achievement_decay = self._calculate_achievement_decay()
        
        print(f"心理学因素分析:")
        print(f"  数字满足感半衰期: {satisfaction_curve['half_life']:.0f} 天")
        print(f"  重复疲劳阈值: {repetition_fatigue['threshold']:.0f} 天")
        print(f"  成就感显著衰减点: {achievement_decay['significant_decay']:.0f} 天")
        
        return {
            'satisfaction_curve': satisfaction_curve,
            'repetition_fatigue': repetition_fatigue,
            'achievement_decay': achievement_decay
        }
    
    def _calculate_satisfaction_curve(self):
        """计算数字增长满足感曲线"""
        # 基于心理学研究，数字增长的满足感遵循对数衰减
        # 满足感 = log(当前数字) - log(习惯数字)
        
        # 假设玩家对数字增长的满足感半衰期为60天
        half_life = 60
        
        return {
            'half_life': half_life,
            'model': 'logarithmic_decay',
            'description': '数字增长满足感随时间对数衰减'
        }
    
    def _calculate_repetition_fatigue(self):
        """计算重复操作疲劳度"""
        # 基于游戏心理学，重复性操作的疲劳阈值
        
        # Cookie Clicker的核心循环：购买->等待->重生
        # 估算疲劳阈值为90-180天
        threshold = 135  # 平均值
        
        return {
            'threshold': threshold,
            'factors': [
                '重复购买决策',
                '等待CPS增长',
                '重生时机计算',
                '数字观察'
            ]
        }
    
    def _calculate_achievement_decay(self):
        """计算成就感衰减"""
        # 成就感来源：新解锁、里程碑、优化发现
        
        # 主要成就感衰减点
        significant_decay = 200  # 约6-7个月
        
        return {
            'significant_decay': significant_decay,
            'decay_factors': [
                '新内容解锁完毕',
                '优化策略固化',
                '数字增长预期化',
                '社交分享价值降低'
            ]
        }
    
    def analyze_content_limits(self):
        """分析内容限制"""
        print("\n=== 内容限制分析 ===")
        
        # 1. 建筑物和升级数量
        total_buildings = 16  # 当前建筑物类型数量
        estimated_upgrades = 500  # 估算的升级总数
        
        # 2. 成就系统
        estimated_achievements = 400  # 估算的成就总数
        
        # 3. 小游戏内容
        minigames = 3  # 花园、魔法书、万神殿等
        
        print(f"内容数量统计:")
        print(f"  建筑物类型: {total_buildings}")
        print(f"  升级总数: ~{estimated_upgrades}")
        print(f"  成就总数: ~{estimated_achievements}")
        print(f"  小游戏数量: {minigames}")
        
        # 计算内容消耗时间
        content_consumption = self._calculate_content_consumption(
            total_buildings, estimated_upgrades, estimated_achievements, minigames
        )
        
        return content_consumption
    
    def _calculate_content_consumption(self, buildings, upgrades, achievements, minigames):
        """计算内容消耗时间"""
        
        # 解锁所有建筑物需要的时间
        buildings_unlock_days = buildings * 2  # 平均每个建筑物需要2天解锁
        
        # 获得所有升级需要的时间
        upgrades_unlock_days = upgrades * 0.5  # 平均每个升级需要0.5天
        
        # 完成所有成就需要的时间
        achievements_days = achievements * 1  # 平均每个成就需要1天
        
        # 掌握所有小游戏需要的时间
        minigames_days = minigames * 30  # 每个小游戏需要30天掌握
        
        total_content_days = max(buildings_unlock_days, upgrades_unlock_days, 
                               achievements_days, minigames_days)
        
        return {
            'buildings_unlock_days': buildings_unlock_days,
            'upgrades_unlock_days': upgrades_unlock_days,
            'achievements_days': achievements_days,
            'minigames_mastery_days': minigames_days,
            'total_content_days': total_content_days,
            'bottleneck': 'achievements' if achievements_days == total_content_days else 'other'
        }
    
    def analyze_player_retention_curve(self):
        """分析玩家留存曲线"""
        print("\n=== 玩家留存分析 ===")
        
        # 基于典型增量游戏的留存数据
        retention_data = {
            'day_1': 0.8,    # 第1天留存率
            'day_7': 0.4,    # 第7天留存率
            'day_30': 0.15,  # 第30天留存率
            'day_90': 0.05,  # 第90天留存率
            'day_180': 0.02, # 第180天留存率
            'day_365': 0.01  # 第365天留存率
        }
        
        # 计算不同类型玩家的预期游戏时长
        player_types = {
            'casual': {
                'percentage': 0.7,
                'avg_playtime_days': 14,
                'description': '休闲玩家，体验新鲜感后离开'
            },
            'regular': {
                'percentage': 0.25,
                'avg_playtime_days': 90,
                'description': '普通玩家，完成主要内容后离开'
            },
            'hardcore': {
                'percentage': 0.05,
                'avg_playtime_days': 365,
                'description': '硬核玩家，追求极限优化'
            }
        }
        
        print(f"玩家类型分析:")
        for player_type, data in player_types.items():
            print(f"  {player_type}: {data['percentage']*100:.0f}% 玩家, "
                  f"平均游戏 {data['avg_playtime_days']} 天")
        
        return {
            'retention_data': retention_data,
            'player_types': player_types
        }
    
    def calculate_theoretical_endgame(self):
        """计算理论上的游戏终点"""
        print("\n=== 理论终点分析 ===")
        
        # 1. 数值上限终点
        numerical_endgame = self._estimate_days_to_reach(self.max_safe_integer)
        
        # 2. 内容完成终点
        content_endgame = 400  # 基于内容分析
        
        # 3. 心理疲劳终点
        psychological_endgame = 135  # 基于心理学分析
        
        # 4. 实际终点（最早到达的限制）
        actual_endgame = min(numerical_endgame, content_endgame, psychological_endgame)
        
        print(f"各种终点分析:")
        print(f"  数值限制终点: {numerical_endgame:.1f} 天")
        print(f"  内容完成终点: {content_endgame} 天")
        print(f"  心理疲劳终点: {psychological_endgame} 天")
        print(f"  实际游戏终点: {actual_endgame:.1f} 天 ({actual_endgame/30:.1f} 个月)")
        
        return {
            'numerical_limit': numerical_endgame,
            'content_limit': content_endgame,
            'psychological_limit': psychological_endgame,
            'actual_endgame': actual_endgame,
            'limiting_factor': self._identify_limiting_factor(
                numerical_endgame, content_endgame, psychological_endgame
            )
        }
    
    def _identify_limiting_factor(self, numerical, content, psychological):
        """识别限制因素"""
        limits = {
            'numerical': numerical,
            'content': content,
            'psychological': psychological
        }
        
        limiting_factor = min(limits, key=limits.get)
        return limiting_factor
    
    def generate_longevity_projections(self):
        """生成游戏寿命预测"""
        print("\n=== 游戏寿命预测 ===")
        
        # 不同场景下的游戏寿命
        scenarios = {
            'pessimistic': {
                'days': 30,
                'description': '悲观场景：快速失去兴趣',
                'probability': 0.6
            },
            'realistic': {
                'days': 135,
                'description': '现实场景：心理疲劳限制',
                'probability': 0.3
            },
            'optimistic': {
                'days': 400,
                'description': '乐观场景：完成所有内容',
                'probability': 0.1
            }
        }
        
        # 计算加权平均游戏寿命
        weighted_average = sum(
            scenario['days'] * scenario['probability'] 
            for scenario in scenarios.values()
        )
        
        print(f"游戏寿命预测:")
        for name, scenario in scenarios.items():
            print(f"  {name}: {scenario['days']} 天 "
                  f"({scenario['days']/30:.1f} 个月) - {scenario['description']}")
        
        print(f"\n加权平均游戏寿命: {weighted_average:.0f} 天 ({weighted_average/30:.1f} 个月)")
        
        return {
            'scenarios': scenarios,
            'weighted_average_days': weighted_average,
            'weighted_average_months': weighted_average / 30
        }
    
    def create_longevity_visualization(self):
        """创建游戏寿命可视化图表"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # 1. 不同限制因素的时间线
            factors = ['Psychological\nFatigue', 'Content\nCompletion', 'Numerical\nLimit']
            days = [135, 400, float('inf')]  # 数值限制设为无穷大表示不可达
            colors = ['red', 'orange', 'green']
            
            # 将无穷大替换为一个大数用于显示
            display_days = [d if d != float('inf') else 10000 for d in days]
            
            bars = ax1.barh(factors, display_days, color=colors, alpha=0.7)
            ax1.set_xlabel('Days to Reach Limit')
            ax1.set_title('Game Longevity Limiting Factors', fontweight='bold')
            ax1.set_xscale('log')
            
            # 添加标签
            for bar, day in zip(bars, days):
                width = bar.get_width()
                label = f'{day:.0f}' if day != float('inf') else '∞'
                ax1.text(width/2, bar.get_y() + bar.get_height()/2,
                        label, ha='center', va='center', fontweight='bold')
            
            # 2. 玩家留存曲线
            days_retention = [1, 7, 30, 90, 180, 365]
            retention_rates = [80, 40, 15, 5, 2, 1]
            
            ax2.plot(days_retention, retention_rates, 'b-', linewidth=3, marker='o', markersize=8)
            ax2.set_xlabel('Days')
            ax2.set_ylabel('Player Retention (%)')
            ax2.set_title('Player Retention Curve', fontweight='bold')
            ax2.set_xscale('log')
            ax2.grid(True, alpha=0.3)
            
            # 标注关键点
            for day, rate in zip(days_retention[::2], retention_rates[::2]):
                ax2.annotate(f'{rate}%', xy=(day, rate), xytext=(day*1.5, rate+5),
                           arrowprops=dict(arrowstyle='->', color='red'),
                           fontsize=9, fontweight='bold')
            
            # 3. 内容消耗时间线
            content_types = ['Buildings', 'Upgrades', 'Achievements', 'Minigames']
            unlock_days = [32, 250, 400, 90]
            
            ax3.bar(content_types, unlock_days, color=['blue', 'green', 'red', 'purple'], alpha=0.7)
            ax3.set_ylabel('Days to Complete')
            ax3.set_title('Content Completion Timeline', fontweight='bold')
            ax3.grid(True, alpha=0.3, axis='y')
            
            # 添加数值标签
            for bar, days in zip(ax3.patches, unlock_days):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 10,
                        f'{days}d', ha='center', va='bottom', fontweight='bold')
            
            plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
            
            # 4. 游戏寿命预测分布
            scenarios = ['Pessimistic\n(30d)', 'Realistic\n(135d)', 'Optimistic\n(400d)']
            probabilities = [60, 30, 10]
            scenario_colors = ['red', 'orange', 'green']
            
            wedges, texts, autotexts = ax4.pie(probabilities, labels=scenarios, autopct='%1.1f%%',
                                              colors=scenario_colors, startangle=90)
            ax4.set_title('Game Longevity Prediction Distribution', fontweight='bold')
            
            # 美化饼图文本
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            # 保存图表
            os.makedirs("longevity_analysis", exist_ok=True)
            plt.savefig("longevity_analysis/game_longevity_analysis.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print("✅ 游戏寿命分析图表已生成: longevity_analysis/game_longevity_analysis.png")
            
        except ImportError:
            print("⚠️ matplotlib未安装，跳过可视化生成")
    
    def generate_comprehensive_report(self):
        """生成综合分析报告"""
        print("\n" + "="*60)
        print("Cookie Clicker 游戏寿命综合分析")
        print("="*60)
        
        # 执行各项分析
        technical_limits = self.analyze_technical_limits()
        psychological_limits = self.analyze_psychological_limits()
        content_limits = self.analyze_content_limits()
        retention_analysis = self.analyze_player_retention_curve()
        endgame_analysis = self.calculate_theoretical_endgame()
        longevity_projections = self.generate_longevity_projections()
        
        # 生成可视化
        self.create_longevity_visualization()
        
        return {
            'technical_limits': technical_limits,
            'psychological_limits': psychological_limits,
            'content_limits': content_limits,
            'retention_analysis': retention_analysis,
            'endgame_analysis': endgame_analysis,
            'longevity_projections': longevity_projections
        }


if __name__ == "__main__":
    print("Cookie Clicker 游戏寿命分析")
    print("=" * 50)
    
    analyzer = GameLongevityAnalyzer()
    analysis = analyzer.generate_comprehensive_report()
    
    print(f"\n" + "=" * 50)
    print("🎯 关键结论:")
    
    endgame = analysis['endgame_analysis']
    projections = analysis['longevity_projections']
    
    print(f"   实际游戏寿命: {endgame['actual_endgame']:.0f} 天 ({endgame['actual_endgame']/30:.1f} 个月)")
    print(f"   限制因素: {endgame['limiting_factor']}")
    print(f"   加权平均寿命: {projections['weighted_average_days']:.0f} 天")
    
    print(f"\n📊 寿命分析:")
    if endgame['actual_endgame'] < 60:
        print("   ⚠️ 游戏寿命较短，主要受心理因素限制")
    elif endgame['actual_endgame'] < 200:
        print("   📈 游戏寿命中等，平衡了内容和心理因素")
    else:
        print("   ✅ 游戏寿命较长，内容丰富度是主要因素")
    
    print(f"\n💡 设计建议:")
    if endgame['limiting_factor'] == 'psychological':
        print("   🧠 增加心理激励机制，如社交功能、竞争元素")
    elif endgame['limiting_factor'] == 'content':
        print("   📚 扩展游戏内容，添加新建筑物、升级、小游戏")
    else:
        print("   🔢 当前数值设计已经足够支撑长期游戏")
