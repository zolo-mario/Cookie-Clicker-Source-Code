"""
Cookie Clicker 快速数值分析

快速分析核心数值模型和策略
"""

import sys
import os
import math

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'cookie_clicker_sim'))

from cookie_clicker_sim.core.buildings import BUILDINGS
from cookie_clicker_sim.core.constants import *


def analyze_building_efficiency():
    """分析建筑物基础效率"""
    print("=== 建筑物基础效率分析 ===")
    
    efficiencies = []
    
    for name, building in BUILDINGS.items():
        base_efficiency = building.base_cps / building.base_price
        efficiencies.append((name, building.base_price, building.base_cps, base_efficiency))
    
    # 按效率排序
    efficiencies.sort(key=lambda x: x[3], reverse=True)
    
    print("建筑物效率排名 (CPS/价格):")
    for i, (name, price, cps, efficiency) in enumerate(efficiencies, 1):
        print(f"{i:2d}. {name:15s} | 价格: {price:>12,} | CPS: {cps:>8.1f} | 效率: {efficiency:.8f}")
    
    return efficiencies


def analyze_price_growth():
    """分析价格增长模型"""
    print("\n=== 价格增长模型分析 ===")
    
    multiplier = BUILDING_PRICE_MULTIPLIER
    print(f"价格增长倍数: {multiplier}")
    print(f"每个建筑物价格增长: {(multiplier-1)*100:.1f}%")
    
    # 计算翻倍周期
    doubling_time = math.log(2) / math.log(multiplier)
    print(f"价格翻倍周期: {doubling_time:.1f} 个建筑物")
    
    # 示例：光标价格增长
    print(f"\n光标价格增长示例:")
    cursor = BUILDINGS['Cursor']
    for amount in [0, 5, 10, 20, 50]:
        price = cursor.get_price(amount)
        efficiency = cursor.base_cps / price
        print(f"  {amount:2d}个光标时: 价格={price:>8,.0f}, 效率={efficiency:.8f}")


def analyze_prestige_model():
    """分析声望系统"""
    print("\n=== 声望系统分析 ===")
    
    print("声望公式: prestige = (total_cookies / 1e12)^(1/3)")
    print("模型类型: 立方根增长 (递减边际收益)")
    
    print("\n声望等级示例:")
    prestige_levels = [1, 10, 50, 100, 500, 1000]
    for prestige in prestige_levels:
        cookies_needed = calculate_cookies_for_prestige(prestige)
        print(f"  {prestige:4d}级声望需要: {cookies_needed:.2e} 饼干")
    
    print("\n饼干数量对应声望:")
    cookie_amounts = [1e12, 1e15, 1e18, 1e21, 1e24]
    for cookies in cookie_amounts:
        prestige = calculate_prestige(cookies)
        print(f"  {cookies:.0e} 饼干 = {prestige:6.1f} 声望")


def analyze_efficiency_decay():
    """分析效率衰减"""
    print("\n=== 效率衰减分析 ===")
    
    # 以Grandma为例分析效率衰减
    grandma = BUILDINGS['Grandma']
    print(f"以{grandma.name}为例 (最高效建筑物):")
    print(f"基础价格: {grandma.base_price}, 基础CPS: {grandma.base_cps}")
    
    print("\n效率衰减曲线:")
    print("数量 | 价格      | 效率")
    print("-" * 25)
    
    for amount in [0, 1, 5, 10, 20, 50]:
        price = grandma.get_price(amount)
        efficiency = grandma.base_cps / price
        print(f"{amount:4d} | {price:>9,.0f} | {efficiency:.8f}")
    
    # 计算效率减半点
    initial_efficiency = grandma.base_cps / grandma.base_price
    target_efficiency = initial_efficiency / 2
    
    for amount in range(1, 20):
        price = grandma.get_price(amount)
        efficiency = grandma.base_cps / price
        if efficiency <= target_efficiency:
            print(f"\n效率减半点: {amount} 个建筑物")
            break


def analyze_optimal_strategies():
    """分析最优策略"""
    print("\n=== 最优策略分析 ===")
    
    print("1. 早期策略 (0-1小时):")
    print("   - 目标: 建立基础CPS")
    print("   - 优先级: Grandma > Farm > Cursor")
    print("   - 原因: Grandma有最高的基础效率")
    print("   - 升级: 购买所有可用升级")
    
    print("\n2. 中期策略 (1-10小时):")
    print("   - 目标: 平衡效率和解锁新内容")
    print("   - 策略: 效率优先，而非最便宜优先")
    print("   - 重点: Factory, Bank, Temple解锁")
    print("   - 重生: 考虑第一次重生(10-50声望)")
    
    print("\n3. 后期策略 (10小时+):")
    print("   - 目标: 最大化声望收益")
    print("   - 策略: 优化重生时机")
    print("   - 重点: 天堂升级和小游戏")
    print("   - 频率: 每2-24小时重生一次")
    
    print("\n4. 核心原则:")
    print("   - 效率优先: 选择CPS增长/价格最高的选项")
    print("   - 平衡投资: 建筑物 vs 升级")
    print("   - 适时重生: 声望增长 >= 当前声望 × 50%")


def calculate_theoretical_limits():
    """计算理论极限"""
    print("\n=== 理论极限分析 ===")
    
    max_safe_integer = 2**53 - 1
    max_prestige = calculate_prestige(max_safe_integer)
    
    print(f"JavaScript最大安全整数: {max_safe_integer:.2e}")
    print(f"理论最大声望等级: {max_prestige:.0f}")
    
    # 计算理论最大CPS
    max_building_amount = 5000  # 游戏限制
    total_base_cps = sum(building.base_cps for building in BUILDINGS.values())
    theoretical_max_cps = total_base_cps * max_building_amount * 1000  # 估算倍数
    
    print(f"理论最大CPS: {theoretical_max_cps:.2e}")
    
    # 计算达到不同声望等级的时间估算
    print(f"\n声望里程碑时间估算 (基于指数增长):")
    milestones = [100, 1000, 10000]
    for milestone in milestones:
        cookies_needed = calculate_cookies_for_prestige(milestone)
        # 假设平均CPS为1M，估算时间
        estimated_hours = cookies_needed / (1e6 * 3600)
        print(f"  {milestone:5d}声望: {cookies_needed:.2e} 饼干, 约{estimated_hours:.0f}小时")


def generate_quick_summary():
    """生成快速总结"""
    print("\n" + "="*60)
    print("Cookie Clicker 数值模型核心洞察")
    print("="*60)
    
    print("\n🔢 数学模型:")
    print("   • 建筑物价格: 指数增长 (1.15^n)")
    print("   • CPS增长: 线性叠加 + 倍数效果")
    print("   • 声望系统: 立方根增长")
    print("   • 效率衰减: 自然的平衡机制")
    
    print("\n🎯 最优策略:")
    print("   • 早期: 专注Grandma (最高基础效率)")
    print("   • 中期: 效率优先 + 平衡投资")
    print("   • 后期: 优化重生时机")
    print("   • 核心: 始终选择效率最高的选项")
    
    print("\n🧮 设计智慧:")
    print("   • 简单公式创造复杂策略空间")
    print("   • 效率衰减防止单一策略过强")
    print("   • 声望系统提供长期动机")
    print("   • 心理激励与数学模型完美结合")
    
    print("\n💡 关键数值:")
    print("   • 最高效建筑物: Grandma (0.01 CPS/Cookie)")
    print("   • 价格翻倍周期: 5个建筑物")
    print("   • 效率减半点: 5个建筑物")
    print("   • 最优重生时机: 声望增长 >= 50%")


if __name__ == "__main__":
    print("Cookie Clicker 快速数值分析")
    print("=" * 50)
    
    # 执行各项分析
    building_efficiencies = analyze_building_efficiency()
    analyze_price_growth()
    analyze_prestige_model()
    analyze_efficiency_decay()
    analyze_optimal_strategies()
    calculate_theoretical_limits()
    generate_quick_summary()
    
    print(f"\n✅ 快速分析完成!")
    print(f"📊 分析了 {len(BUILDINGS)} 个建筑物")
    print(f"🎯 核心洞察: Grandma是最高效的建筑物")
    print(f"📈 关键策略: 效率优先 + 适时重生")
