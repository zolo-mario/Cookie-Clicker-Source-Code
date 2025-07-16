# Cookie Clicker 数值模拟器

基于Cookie Clicker源码分析的高精度数值模拟系统，用于游戏策略优化、平衡性分析和进度预测。

## 🎯 项目特点

### ✨ 核心功能
- **精确数值还原**: 基于源码分析的准确游戏机制
- **完整游戏模拟**: 支持建筑物、升级、声望、成就等所有系统
- **智能购买优化**: 自动计算最优购买策略
- **策略分析工具**: 比较不同策略的效果
- **进度预测**: 预测达成目标所需时间

### 🔧 技术特色
- **模块化设计**: 清晰的代码结构，易于扩展
- **高性能模拟**: 56000x实时速度的模拟性能
- **事件驱动**: 支持自定义事件回调
- **状态管理**: 完整的保存/加载功能

## 📁 项目结构

```
cookie_clicker_sim/
├── core/                   # 核心数据模型
│   ├── game_state.py      # 游戏状态管理
│   ├── buildings.py       # 建筑物系统
│   ├── upgrades.py        # 升级系统
│   └── constants.py       # 数值常数
├── engines/                # 计算引擎
│   ├── cps_calculator.py  # CPS计算引擎
│   ├── purchase_optimizer.py  # 购买优化器
│   └── simulator.py       # 游戏模拟器
└── examples/               # 使用示例
    └── basic_simulation.py
```

## 🚀 快速开始

### 基础使用

```python
from cookie_clicker_sim import GameSimulator

# 创建模拟器
simulator = GameSimulator()

# 手动点击获得初始饼干
simulator.click_cookie(100)

# 购买建筑物
simulator.buy_building('Cursor')

# 模拟1小时游戏进程
simulator.simulate_time_period(3600)

# 查看结果
summary = simulator.get_simulation_summary()
print(f"饼干: {summary['game_state']['cookies']:.0f}")
print(f"CPS: {summary['game_state']['cookies_per_second']:.1f}")
```

### 策略优化

```python
# 获取购买建议
recommendations = simulator.get_purchase_recommendations(5)
for option in recommendations:
    print(f"{option.type}: {option.name} (效率: {option.efficiency:.6f})")

# 自动优化购买
simulator.auto_buy_enabled = True
simulator.simulate_time_period(1800)  # 30分钟自动优化
```

### 进度分析

```python
# CPS详细分解
breakdown = simulator.get_cps_breakdown()
for source, cps in breakdown.items():
    print(f"{source}: {cps:.1f}")

# 声望分析
from cookie_clicker_sim.core.constants import calculate_prestige
total_cookies = simulator.game_state.cookies_reset + simulator.game_state.cookies_earned
prestige = calculate_prestige(total_cookies)
print(f"当前可获得声望: {prestige:.0f}")
```

## 📊 核心数值公式

### 建筑物价格
```python
price = base_price * (1.15 ^ amount)
```

### 声望计算
```python
prestige = (cookies_reset / 1e12) ^ (1/3)
```

### CPS计算
```python
total_cps = sum(building_cps) * global_multiplier * buff_multiplier
```

## 🎮 模拟器功能

### 自动化功能
- **自动购买**: 基于效率的智能购买决策
- **自动点击**: 可配置的自动点击功能
- **自动重生**: 智能重生时机判断

### 分析工具
- **效率分析**: 计算建筑物和升级的购买效率
- **策略比较**: 对比不同策略的效果
- **时间预测**: 预测达成目标所需时间
- **最优配比**: 计算建筑物的最优数量配比

### 事件系统
```python
def on_purchase(game_state, data):
    print(f"购买了: {data.name}")

simulator.set_event_callback('purchase', on_purchase)
```

## 📈 性能指标

- **模拟速度**: 56000x 实时速度
- **内存使用**: 轻量级设计，低内存占用
- **精度**: 基于源码的高精度数值计算
- **稳定性**: 完整的错误处理和状态管理

## 🔬 应用场景

### 游戏策略优化
- 寻找最高效的购买顺序
- 分析不同建筑物的投资回报率
- 优化重生时机选择

### 数值平衡分析
- 测试游戏平衡性
- 分析新内容对游戏进度的影响
- 评估数值调整的效果

### 进度规划
- 预测达成特定目标的时间
- 制定长期发展计划
- 优化游戏体验曲线

### 教育研究
- 理解增量游戏的数学原理
- 研究指数增长模型
- 分析游戏经济系统

## 🧪 测试结果

运行测试脚本验证功能：

```bash
python test_simulator.py
```

测试覆盖：
- ✅ 基础功能测试
- ✅ 模拟器核心功能
- ✅ 优化算法测试
- ✅ 时间段模拟测试
- ✅ 保存/加载功能
- ✅ 性能测试

## 📝 示例演示

运行完整演示：

```bash
python cookie_clicker_sim/examples/basic_simulation.py
```

演示内容：
1. **基础模拟演示** - 展示核心功能
2. **策略比较演示** - 对比不同策略效果
3. **声望分析演示** - 重生机制分析
4. **事件回调演示** - 事件系统使用

## 🔮 扩展可能

### 小游戏系统
- 花园系统模拟
- 魔法书系统模拟
- 万神殿系统模拟

### 高级功能
- 机器学习优化策略
- 多目标优化算法
- 实时数据可视化
- Web界面支持

### 数据分析
- 统计数据导出
- 图表生成
- 趋势分析
- 对比报告

## 🤝 贡献指南

欢迎贡献代码和建议！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢

- **Orteil** - Cookie Clicker原作者
- **Cookie Clicker社区** - 提供游戏机制分析
- **开源社区** - 提供技术支持和灵感

## 📊 数据可视化功能

### 🎨 图表类型
- **📈 进度曲线图** - 显示饼干数量和CPS随时间变化
- **🥧 建筑物分布饼图** - 显示各建筑物数量占比
- **📊 CPS分解柱状图** - 显示各CPS来源贡献
- **📉 效率对比图** - 显示购买选项效率排序
- **📈 效率曲线图** - 显示建筑物效率变化
- **🔄 策略对比图** - 对比不同策略效果
- **⭐ 声望分析图** - 分析声望与饼干关系

### 🚀 快速生成图表

```bash
# 生成完整的数值分析图表
python show_charts.py

# 测试可视化功能
python test_visualization.py

# 运行带可视化的演示
python cookie_clicker_sim/examples/basic_simulation.py
```

### 📈 实际测试结果

**4小时模拟测试结果**：
- 🍪 **最终饼干**: 66.7亿
- ⚡ **最终CPS**: 491万/秒
- 🏗️ **建筑物总数**: 234个
- 📊 **效率**: 28.8亿饼干/小时

**策略对比效果**：
- 🥇 **自动优化策略**: 66.7亿饼干 (效率最高)
- 🥈 **平衡发展策略**: 114万饼干
- 🥉 **便宜建筑策略**: 4万饼干

### 🎯 可视化特色
- **高精度模拟** - 基于源码的准确数值计算
- **多维度分析** - 7种不同类型的专业图表
- **策略量化** - 数据驱动的策略效果对比
- **长期预测** - 完整的时间序列分析
- **自动报告** - 详细的分析报告生成
- **英文标签** - 避免中文字体乱码问题
- **高分辨率** - 300 DPI专业级图表输出
- **科学计数法** - 自动处理大数值显示

---

**Cookie Clicker数值模拟器** - 让数据驱动你的饼干帝国！ 🍪📊
