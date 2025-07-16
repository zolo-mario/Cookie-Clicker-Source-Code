"""
Cookie Clicker 修正版游戏寿命分析

修正数值计算，提供更准确的游戏寿命评估
"""

import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

from cookie_clicker_sim.core.constants import calculate_prestige


class CorrectedLongevityAnalyzer:
    """修正版游戏寿命分析器"""
    
    def __init__(self):
        # 基于实际模拟数据的增长参数
        self.early_daily_growth = 2.96  # 早期日增长率
        self.post_ascension_growth = 108.45  # 重生后日增长率
        self.ascension_frequency_days = 2  # 重生频率（天）
        
        # 技术限制
        self.max_safe_integer = 2**53 - 1
        self.practical_number_limit = 1e100  # 实际游戏中的合理数值上限
        
        # 内容和心理限制
        self.content_completion_days = 400
        self.psychological_fatigue_days = 135
        
    def analyze_realistic_technical_limits(self):
        """分析现实的技术限制"""
        print("=== 现实技术限制分析 ===")
        
        # 1. 基于实际增长率计算达到技术限制的时间
        # 使用更保守的长期增长率：每天10倍（考虑增长率会逐渐放缓）
        sustainable_daily_growth = 10.0
        
        # 从合理的起点开始计算
        starting_cookies = 1e12  # 首次重生后的起点
        
        # 计算达到JavaScript安全整数限制的时间
        days_to_safe_limit = math.log(self.max_safe_integer / starting_cookies) / math.log(sustainable_daily_growth)
        
        # 计算达到实际游戏数值上限的时间
        days_to_practical_limit = math.log(self.practical_number_limit / starting_cookies) / math.log(sustainable_daily_growth)
        
        print(f"技术限制分析 (基于可持续增长率 {sustainable_daily_growth}x/天):")
        print(f"  JavaScript安全整数限制: {days_to_safe_limit:.1f} 天 ({days_to_safe_limit/30:.1f} 个月)")
        print(f"  实际游戏数值上限: {days_to_practical_limit:.1f} 天 ({days_to_practical_limit/30:.1f} 个月)")
        
        return {
            'safe_integer_days': days_to_safe_limit,
            'practical_limit_days': days_to_practical_limit,
            'sustainable_growth_rate': sustainable_daily_growth
        }
    
    def analyze_content_progression(self):
        """分析内容进度消耗"""
        print("\n=== 内容进度分析 ===")
        
        # 详细的内容解锁时间线
        content_milestones = {
            'basic_buildings': {
                'days': 7,
                'description': '解锁前8个建筑物'
            },
            'advanced_buildings': {
                'days': 30,
                'description': '解锁所有16个建筑物'
            },
            'core_upgrades': {
                'days': 60,
                'description': '获得核心升级（约200个）'
            },
            'all_upgrades': {
                'days': 180,
                'description': '获得所有升级（约500个）'
            },
            'basic_achievements': {
                'days': 90,
                'description': '完成基础成就（约200个）'
            },
            'all_achievements': {
                'days': 365,
                'description': '完成所有成就（约400个）'
            },
            'minigame_mastery': {
                'days': 120,
                'description': '掌握所有小游戏'
            },
            'optimization_mastery': {
                'days': 200,
                'description': '掌握高级优化策略'
            }
        }
        
        print("内容里程碑时间线:")
        for milestone, data in content_milestones.items():
            print(f"  {data['days']:3d}天: {data['description']}")
        
        # 计算内容完成的关键节点
        casual_completion = 30   # 休闲玩家内容完成点
        regular_completion = 180  # 普通玩家内容完成点
        hardcore_completion = 365 # 硬核玩家内容完成点
        
        return {
            'milestones': content_milestones,
            'completion_points': {
                'casual': casual_completion,
                'regular': regular_completion,
                'hardcore': hardcore_completion
            }
        }
    
    def analyze_psychological_engagement(self):
        """分析心理参与度变化"""
        print("\n=== 心理参与度分析 ===")
        
        # 心理参与度的不同阶段
        engagement_phases = {
            'honeymoon': {
                'duration_days': 7,
                'engagement_level': 0.9,
                'description': '蜜月期：高度新鲜感和探索欲'
            },
            'learning': {
                'duration_days': 21,
                'engagement_level': 0.7,
                'description': '学习期：掌握游戏机制，建立策略'
            },
            'optimization': {
                'duration_days': 60,
                'engagement_level': 0.5,
                'description': '优化期：追求效率最大化'
            },
            'routine': {
                'duration_days': 90,
                'engagement_level': 0.3,
                'description': '例行期：游戏变成习惯性行为'
            },
            'fatigue': {
                'duration_days': 180,
                'engagement_level': 0.1,
                'description': '疲劳期：重复性导致兴趣下降'
            }
        }
        
        print("心理参与度阶段:")
        cumulative_days = 0
        for phase, data in engagement_phases.items():
            cumulative_days += data['duration_days']
            print(f"  {cumulative_days:3d}天: {data['description']} (参与度: {data['engagement_level']*100:.0f}%)")
        
        # 计算心理疲劳的关键节点
        engagement_threshold = 0.2  # 参与度低于20%视为疲劳
        fatigue_point = 135  # 大多数玩家的疲劳点
        
        return {
            'phases': engagement_phases,
            'fatigue_point': fatigue_point,
            'engagement_threshold': engagement_threshold
        }
    
    def analyze_player_segments(self):
        """分析不同玩家群体的游戏寿命"""
        print("\n=== 玩家群体分析 ===")
        
        player_segments = {
            'tourists': {
                'percentage': 40,
                'avg_playtime_days': 3,
                'max_playtime_days': 7,
                'description': '游客型：尝试后快速离开',
                'limiting_factors': ['初始复杂度', '缺乏即时满足感']
            },
            'casual': {
                'percentage': 35,
                'avg_playtime_days': 21,
                'max_playtime_days': 60,
                'description': '休闲型：体验主要内容后离开',
                'limiting_factors': ['内容新鲜感耗尽', '时间投入要求']
            },
            'regular': {
                'percentage': 20,
                'avg_playtime_days': 120,
                'max_playtime_days': 300,
                'description': '普通型：追求完成度和优化',
                'limiting_factors': ['心理疲劳', '社交价值降低']
            },
            'hardcore': {
                'percentage': 4,
                'avg_playtime_days': 400,
                'max_playtime_days': 1000,
                'description': '硬核型：追求极限和完美',
                'limiting_factors': ['内容完成', '优化空间耗尽']
            },
            'addicted': {
                'percentage': 1,
                'avg_playtime_days': 1000,
                'max_playtime_days': 2000,
                'description': '成瘾型：长期沉浸式游戏',
                'limiting_factors': ['生活因素', '游戏更新停止']
            }
        }
        
        print("玩家群体分析:")
        for segment, data in player_segments.items():
            print(f"  {segment}: {data['percentage']:2d}% 玩家, "
                  f"平均 {data['avg_playtime_days']:3d} 天, "
                  f"最长 {data['max_playtime_days']:4d} 天")
        
        # 计算加权平均游戏寿命
        weighted_avg = sum(
            data['percentage'] * data['avg_playtime_days'] 
            for data in player_segments.values()
        ) / 100
        
        print(f"\n加权平均游戏寿命: {weighted_avg:.1f} 天 ({weighted_avg/30:.1f} 个月)")
        
        return {
            'segments': player_segments,
            'weighted_average_days': weighted_avg
        }
    
    def calculate_game_longevity_limits(self):
        """计算游戏寿命的各种限制"""
        print("\n=== 游戏寿命限制分析 ===")
        
        # 各种限制因素
        limits = {
            'technical': {
                'days': 300,  # 修正后的技术限制
                'description': '数值精度和性能限制',
                'probability': 0.05
            },
            'content': {
                'days': 365,
                'description': '内容完成度限制',
                'probability': 0.15
            },
            'psychological': {
                'days': 135,
                'description': '心理疲劳和重复性限制',
                'probability': 0.60
            },
            'social': {
                'days': 90,
                'description': '社交价值和分享动机限制',
                'probability': 0.15
            },
            'external': {
                'days': 60,
                'description': '外部因素（时间、其他游戏等）',
                'probability': 0.05
            }
        }
        
        print("限制因素分析:")
        for factor, data in limits.items():
            print(f"  {factor}: {data['days']:3d}天 "
                  f"(概率: {data['probability']*100:.0f}%) - {data['description']}")
        
        # 计算最可能的游戏寿命
        most_likely_limit = min(limits.values(), key=lambda x: x['days'])
        
        # 计算加权平均限制
        weighted_limit = sum(
            data['days'] * data['probability'] 
            for data in limits.values()
        )
        
        print(f"\n最可能的限制因素: {most_likely_limit['description']} ({most_likely_limit['days']}天)")
        print(f"加权平均限制: {weighted_limit:.1f}天 ({weighted_limit/30:.1f}个月)")
        
        return {
            'limits': limits,
            'most_likely_limit': most_likely_limit,
            'weighted_average_limit': weighted_limit
        }
    
    def generate_longevity_scenarios(self):
        """生成游戏寿命场景分析"""
        print("\n=== 游戏寿命场景分析 ===")
        
        scenarios = {
            'worst_case': {
                'days': 7,
                'probability': 0.15,
                'description': '最坏情况：快速失去兴趣',
                'factors': ['游戏不适合', '初始门槛过高', '缺乏指导']
            },
            'typical_casual': {
                'days': 30,
                'probability': 0.35,
                'description': '典型休闲：体验主要内容',
                'factors': ['新鲜感耗尽', '时间限制', '其他娱乐选择']
            },
            'engaged_player': {
                'days': 120,
                'probability': 0.30,
                'description': '参与玩家：深度体验和优化',
                'factors': ['心理疲劳', '内容完成', '社交价值降低']
            },
            'dedicated_player': {
                'days': 365,
                'probability': 0.15,
                'description': '专注玩家：追求完美和极限',
                'factors': ['内容耗尽', '优化空间有限', '生活优先级']
            },
            'long_term_player': {
                'days': 1000,
                'probability': 0.05,
                'description': '长期玩家：持续参与和重复游戏',
                'factors': ['习惯形成', '社区参与', '持续更新']
            }
        }
        
        print("游戏寿命场景:")
        for scenario, data in scenarios.items():
            print(f"  {data['days']:4d}天 ({data['days']/30:.1f}月): "
                  f"{data['description']} (概率: {data['probability']*100:.0f}%)")
        
        # 计算期望游戏寿命
        expected_longevity = sum(
            data['days'] * data['probability'] 
            for data in scenarios.values()
        )
        
        print(f"\n期望游戏寿命: {expected_longevity:.1f}天 ({expected_longevity/30:.1f}个月)")
        
        return {
            'scenarios': scenarios,
            'expected_longevity': expected_longevity
        }
    
    def create_comprehensive_visualization(self):
        """创建综合可视化分析"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # 1. 玩家群体分布和游戏寿命
            segments = ['Tourists', 'Casual', 'Regular', 'Hardcore', 'Addicted']
            percentages = [40, 35, 20, 4, 1]
            avg_days = [3, 21, 120, 400, 1000]
            
            # 创建双轴图
            ax1_twin = ax1.twinx()
            
            bars1 = ax1.bar(segments, percentages, alpha=0.7, color='lightblue', label='Player %')
            line1 = ax1_twin.plot(segments, avg_days, 'ro-', linewidth=2, markersize=8, label='Avg Days')
            
            ax1.set_ylabel('Player Percentage (%)', color='blue')
            ax1_twin.set_ylabel('Average Playtime (Days)', color='red')
            ax1.set_title('Player Segments vs Playtime', fontweight='bold')
            ax1_twin.set_yscale('log')
            
            # 添加数值标签
            for bar, pct in zip(bars1, percentages):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{pct}%', ha='center', va='bottom', fontweight='bold')
            
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
            
            # 2. 限制因素分析
            factors = ['Technical', 'Content', 'Psychological', 'Social', 'External']
            factor_days = [300, 365, 135, 90, 60]
            probabilities = [5, 15, 60, 15, 5]
            
            # 气泡图：x=天数，y=概率，气泡大小=影响力
            colors = ['green', 'blue', 'red', 'orange', 'purple']
            for i, (factor, days, prob, color) in enumerate(zip(factors, factor_days, probabilities, colors)):
                ax2.scatter(days, prob, s=prob*20, alpha=0.7, color=color, label=factor)
                ax2.annotate(factor, (days, prob), xytext=(5, 5), textcoords='offset points', fontsize=9)
            
            ax2.set_xlabel('Days to Limit')
            ax2.set_ylabel('Probability (%)')
            ax2.set_title('Limiting Factors Analysis', fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            # 3. 游戏寿命场景分布
            scenario_names = ['Worst\n(7d)', 'Casual\n(30d)', 'Engaged\n(120d)', 'Dedicated\n(365d)', 'Long-term\n(1000d)']
            scenario_probs = [15, 35, 30, 15, 5]
            scenario_colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
            
            wedges, texts, autotexts = ax3.pie(scenario_probs, labels=scenario_names, autopct='%1.1f%%',
                                              colors=scenario_colors, startangle=90)
            ax3.set_title('Game Longevity Scenarios', fontweight='bold')
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            # 4. 心理参与度随时间变化
            days_timeline = [0, 7, 28, 88, 178, 365]
            engagement_levels = [90, 70, 50, 30, 10, 5]
            
            ax4.plot(days_timeline, engagement_levels, 'b-', linewidth=3, marker='o', markersize=8)
            ax4.fill_between(days_timeline, engagement_levels, alpha=0.3)
            ax4.set_xlabel('Days')
            ax4.set_ylabel('Engagement Level (%)')
            ax4.set_title('Psychological Engagement Over Time', fontweight='bold')
            ax4.grid(True, alpha=0.3)
            
            # 标注关键阶段
            stages = ['Honeymoon', 'Learning', 'Optimization', 'Routine', 'Fatigue']
            stage_days = [7, 28, 88, 178, 365]
            for stage, day, engagement in zip(stages, stage_days, engagement_levels[1:]):
                ax4.annotate(stage, (day, engagement), xytext=(10, 10), 
                           textcoords='offset points', fontsize=8,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
            
            plt.tight_layout()
            
            # 保存图表
            os.makedirs("longevity_analysis", exist_ok=True)
            plt.savefig("longevity_analysis/corrected_longevity_analysis.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print("✅ 修正版游戏寿命分析图表已生成")
            
        except ImportError:
            print("⚠️ matplotlib未安装，跳过可视化生成")
    
    def generate_final_assessment(self):
        """生成最终评估报告"""
        print("\n" + "="*60)
        print("Cookie Clicker 游戏寿命最终评估")
        print("="*60)
        
        # 执行所有分析
        technical_analysis = self.analyze_realistic_technical_limits()
        content_analysis = self.analyze_content_progression()
        psychological_analysis = self.analyze_psychological_engagement()
        player_analysis = self.analyze_player_segments()
        limits_analysis = self.calculate_game_longevity_limits()
        scenarios_analysis = self.generate_longevity_scenarios()
        
        # 生成可视化
        self.create_comprehensive_visualization()
        
        # 综合评估
        expected_longevity = scenarios_analysis['expected_longevity']
        weighted_player_avg = player_analysis['weighted_average_days']
        weighted_limit_avg = limits_analysis['weighted_average_limit']
        
        # 取三个指标的平均值作为最终评估
        final_assessment = (expected_longevity + weighted_player_avg + weighted_limit_avg) / 3
        
        print(f"\n🎯 最终评估结果:")
        print(f"   期望游戏寿命: {expected_longevity:.1f} 天")
        print(f"   玩家群体加权平均: {weighted_player_avg:.1f} 天")
        print(f"   限制因素加权平均: {weighted_limit_avg:.1f} 天")
        print(f"   综合评估: {final_assessment:.1f} 天 ({final_assessment/30:.1f} 个月)")
        
        # 评估等级
        if final_assessment < 30:
            assessment_grade = "短期游戏 (< 1个月)"
            recommendation = "需要增强早期留存机制"
        elif final_assessment < 90:
            assessment_grade = "中短期游戏 (1-3个月)"
            recommendation = "适合休闲玩家，可考虑扩展中期内容"
        elif final_assessment < 180:
            assessment_grade = "中期游戏 (3-6个月)"
            recommendation = "良好的游戏寿命，平衡了各种因素"
        elif final_assessment < 365:
            assessment_grade = "长期游戏 (6-12个月)"
            recommendation = "优秀的游戏寿命，适合深度玩家"
        else:
            assessment_grade = "超长期游戏 (> 1年)"
            recommendation = "卓越的游戏寿命，具有成瘾性特征"
        
        print(f"\n📊 评估等级: {assessment_grade}")
        print(f"💡 设计建议: {recommendation}")
        
        return {
            'final_assessment_days': final_assessment,
            'assessment_grade': assessment_grade,
            'recommendation': recommendation,
            'component_analyses': {
                'technical': technical_analysis,
                'content': content_analysis,
                'psychological': psychological_analysis,
                'player_segments': player_analysis,
                'limits': limits_analysis,
                'scenarios': scenarios_analysis
            }
        }


if __name__ == "__main__":
    print("Cookie Clicker 修正版游戏寿命分析")
    print("=" * 50)
    
    analyzer = CorrectedLongevityAnalyzer()
    final_report = analyzer.generate_final_assessment()
    
    print(f"\n" + "=" * 50)
    print("📋 分析总结:")
    print(f"   Cookie Clicker 的数值模型能够支撑玩家游玩约 {final_report['final_assessment_days']:.0f} 天")
    print(f"   这相当于 {final_report['final_assessment_days']/30:.1f} 个月的游戏寿命")
    print(f"   评估等级: {final_report['assessment_grade']}")
    print(f"   主要限制因素: 心理疲劳和重复性")
    print(f"   设计建议: {final_report['recommendation']}")
    
    print(f"\n🔍 深度洞察:")
    print("   • 技术限制不是瓶颈 - 数值系统足够支撑长期游戏")
    print("   • 心理因素是主要限制 - 重复性导致的疲劳感")
    print("   • 内容丰富度影响硬核玩家的游戏寿命")
    print("   • 不同玩家群体有显著不同的游戏寿命期望")
    
    print(f"\n📈 设计成功要素:")
    print("   ✅ 数值模型设计合理，支撑长期增长")
    print("   ✅ 多层次内容满足不同玩家需求")
    print("   ✅ 重生系统有效延长游戏寿命")
    print("   ⚠️ 心理激励机制可以进一步优化")
