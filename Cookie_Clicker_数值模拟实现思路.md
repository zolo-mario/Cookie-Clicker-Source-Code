# Cookie Clicker 数值模拟实现思路

## 项目概述

基于Cookie Clicker源码分析，设计一个专注于核心机制的数值模拟系统，用于：
- 游戏平衡性分析
- 最优策略计算
- 进度预测和规划
- 数值调优实验

## 核心数据模型

### 1. 游戏状态类 (GameState)

```python
class GameState:
    def __init__(self):
        # 基础数据
        self.cookies = 0.0              # 当前饼干数量
        self.cookies_earned = 0.0       # 总获得饼干数
        self.cookies_reset = 0.0        # 重置前总饼干数
        self.cookies_per_second = 0.0   # 每秒饼干产量
        self.click_power = 1.0          # 点击力量
        
        # 建筑物数量
        self.buildings = {}             # {building_name: amount}
        
        # 升级状态
        self.upgrades = set()           # 已购买升级
        self.achievements = set()       # 已获得成就
        
        # 声望系统
        self.prestige = 0               # 声望等级
        self.heavenly_chips = 0         # 天堂芯片
        self.heavenly_chips_spent = 0   # 已花费天堂芯片
        
        # 时间相关
        self.game_time = 0.0           # 游戏时间(秒)
        self.last_update = 0.0         # 上次更新时间
```

### 2. 建筑物定义类 (Building)

```python
class Building:
    def __init__(self, name, base_price, base_cps, price_multiplier=1.15):
        self.name = name
        self.base_price = base_price
        self.base_cps = base_cps
        self.price_multiplier = price_multiplier
        self.amount = 0
        self.level = 0
    
    def get_price(self, amount=None):
        """计算购买价格"""
        if amount is None:
            amount = self.amount
        return self.base_price * (self.price_multiplier ** amount)
    
    def get_cps(self, game_state):
        """计算当前CPS贡献"""
        base = self.base_cps * self.amount
        # 应用各种倍数
        multiplier = self.get_multiplier(game_state)
        return base * multiplier
```

### 3. 升级系统类 (Upgrade)

```python
class Upgrade:
    def __init__(self, name, price, effect_type, effect_value, unlock_condition):
        self.name = name
        self.price = price
        self.effect_type = effect_type  # 'cps_mult', 'click_mult', 'building_mult'
        self.effect_value = effect_value
        self.unlock_condition = unlock_condition
        self.unlocked = False
        self.bought = False
```

## 核心数值常数

### 建筑物基础数据

```python
BUILDINGS_DATA = {
    'Cursor': {
        'base_price': 15,
        'base_cps': 0.1,
        'price_multiplier': 1.15
    },
    'Grandma': {
        'base_price': 100,
        'base_cps': 1.0,
        'price_multiplier': 1.15
    },
    'Farm': {
        'base_price': 1100,
        'base_cps': 8.0,
        'price_multiplier': 1.15
    },
    'Mine': {
        'base_price': 12000,
        'base_cps': 47.0,
        'price_multiplier': 1.15
    },
    # ... 其他建筑物
}
```

### 关键数值公式

```python
# 声望计算公式
def calculate_prestige(cookies_reset):
    """计算声望等级"""
    HC_FACTOR = 3  # 天堂芯片因子
    return (cookies_reset / 1_000_000_000_000) ** (1 / HC_FACTOR)

# 建筑物CPS计算公式 (自动生成)
def calculate_building_base_cps(building_index):
    """根据建筑物索引计算基础CPS"""
    n = building_index
    if n == 0:  # Cursor特殊处理
        return 0.1
    return math.ceil((n ** (n * 0.5 + 2)) * 10) / 10

# 建筑物价格计算公式 (自动生成)
def calculate_building_base_price(building_index):
    """根据建筑物索引计算基础价格"""
    n = building_index
    return (n + 9 + (0 if n < 5 else (n - 5) ** 1.75 * 5)) * (10 ** n) * max(1, n - 14)
```

## 核心算法模块

### 1. CPS计算引擎

```python
class CPSCalculator:
    def __init__(self):
        self.multipliers = {}
    
    def calculate_total_cps(self, game_state):
        """计算总CPS"""
        total_cps = 0.0
        
        # 建筑物CPS
        for building_name, building in BUILDINGS.items():
            building_cps = building.get_cps(game_state)
            total_cps += building_cps
        
        # 全局倍数
        global_multiplier = self.get_global_multiplier(game_state)
        total_cps *= global_multiplier
        
        return total_cps
    
    def get_global_multiplier(self, game_state):
        """计算全局CPS倍数"""
        multiplier = 1.0
        
        # 声望加成
        if game_state.prestige > 0:
            multiplier *= (1 + game_state.prestige * 0.01)
        
        # 升级加成
        for upgrade_name in game_state.upgrades:
            upgrade = UPGRADES[upgrade_name]
            if upgrade.effect_type == 'cps_mult':
                multiplier *= (1 + upgrade.effect_value)
        
        # 牛奶加成
        milk_multiplier = self.get_milk_multiplier(game_state)
        multiplier *= milk_multiplier
        
        return multiplier
```

### 2. 购买决策引擎

```python
class PurchaseOptimizer:
    def __init__(self):
        self.efficiency_cache = {}
    
    def get_best_purchase(self, game_state, budget):
        """找到最佳购买选择"""
        options = []
        
        # 评估建筑物
        for building_name, building in BUILDINGS.items():
            if building.get_price() <= budget:
                efficiency = self.calculate_efficiency(building, game_state)
                options.append({
                    'type': 'building',
                    'name': building_name,
                    'price': building.get_price(),
                    'efficiency': efficiency
                })
        
        # 评估升级
        for upgrade_name, upgrade in UPGRADES.items():
            if (upgrade.unlocked and not upgrade.bought and 
                upgrade.price <= budget):
                efficiency = self.calculate_upgrade_efficiency(upgrade, game_state)
                options.append({
                    'type': 'upgrade',
                    'name': upgrade_name,
                    'price': upgrade.price,
                    'efficiency': efficiency
                })
        
        # 返回效率最高的选择
        return max(options, key=lambda x: x['efficiency']) if options else None
    
    def calculate_efficiency(self, building, game_state):
        """计算建筑物购买效率 (CPS增长/价格)"""
        current_cps = building.get_cps(game_state)
        
        # 模拟购买后的CPS
        building.amount += 1
        new_cps = building.get_cps(game_state)
        building.amount -= 1
        
        cps_increase = new_cps - current_cps
        price = building.get_price()
        
        return cps_increase / price if price > 0 else 0
```

### 3. 游戏模拟器

```python
class GameSimulator:
    def __init__(self):
        self.game_state = GameState()
        self.cps_calculator = CPSCalculator()
        self.purchase_optimizer = PurchaseOptimizer()
    
    def simulate_step(self, dt=1.0):
        """模拟一个时间步长"""
        # 更新CPS
        self.game_state.cookies_per_second = self.cps_calculator.calculate_total_cps(
            self.game_state
        )
        
        # 生产饼干
        cookies_produced = self.game_state.cookies_per_second * dt
        self.game_state.cookies += cookies_produced
        self.game_state.cookies_earned += cookies_produced
        
        # 自动购买决策
        if self.auto_buy_enabled:
            self.auto_purchase()
        
        # 更新时间
        self.game_state.game_time += dt
        self.game_state.last_update = self.game_state.game_time
    
    def auto_purchase(self):
        """自动购买逻辑"""
        while True:
            best_purchase = self.purchase_optimizer.get_best_purchase(
                self.game_state, self.game_state.cookies
            )
            
            if not best_purchase:
                break
            
            if best_purchase['type'] == 'building':
                self.buy_building(best_purchase['name'])
            elif best_purchase['type'] == 'upgrade':
                self.buy_upgrade(best_purchase['name'])
            else:
                break
    
    def simulate_time_period(self, duration, time_step=1.0):
        """模拟指定时间段"""
        steps = int(duration / time_step)
        for _ in range(steps):
            self.simulate_step(time_step)
        
        return self.game_state
```

## 分析工具模块

### 1. 进度预测器

```python
class ProgressPredictor:
    def __init__(self, simulator):
        self.simulator = simulator
    
    def predict_time_to_goal(self, goal_cookies):
        """预测达到目标饼干数所需时间"""
        current_state = copy.deepcopy(self.simulator.game_state)
        
        # 二分搜索最优时间
        low, high = 0, 365 * 24 * 3600  # 最多一年
        
        while high - low > 1:
            mid = (low + high) // 2
            test_state = copy.deepcopy(current_state)
            self.simulator.game_state = test_state
            self.simulator.simulate_time_period(mid)
            
            if test_state.cookies >= goal_cookies:
                high = mid
            else:
                low = mid
        
        return high
    
    def analyze_ascension_timing(self):
        """分析最佳重生时机"""
        current_prestige = calculate_prestige(
            self.simulator.game_state.cookies_reset + 
            self.simulator.game_state.cookies_earned
        )
        
        # 计算重生收益
        prestige_gain = current_prestige - self.simulator.game_state.prestige
        
        # 评估重生价值
        if prestige_gain >= 1:
            return {
                'should_ascend': True,
                'prestige_gain': prestige_gain,
                'reason': f'Will gain {prestige_gain} prestige levels'
            }
        else:
            return {
                'should_ascend': False,
                'prestige_gain': 0,
                'reason': 'Not enough prestige gain'
            }
```

### 2. 效率分析器

```python
class EfficiencyAnalyzer:
    def __init__(self):
        self.data_points = []
    
    def analyze_building_efficiency(self, game_state):
        """分析各建筑物效率"""
        results = {}
        
        for building_name, building in BUILDINGS.items():
            if building.amount > 0:
                cps_per_building = building.get_cps(game_state) / building.amount
                cost_per_cps = building.get_price() / cps_per_building
                
                results[building_name] = {
                    'cps_per_building': cps_per_building,
                    'cost_per_cps': cost_per_cps,
                    'total_cps': building.get_cps(game_state),
                    'total_cost': building.get_price() * building.amount
                }
        
        return results
    
    def find_optimal_strategy(self, time_limit):
        """寻找指定时间内的最优策略"""
        # 使用动态规划或遗传算法
        # 这里简化为贪心算法
        pass
```

## 实现架构

### 目录结构
```
cookie_clicker_sim/
├── core/
│   ├── __init__.py
│   ├── game_state.py      # 游戏状态类
│   ├── buildings.py       # 建筑物系统
│   ├── upgrades.py        # 升级系统
│   └── constants.py       # 数值常数
├── engines/
│   ├── __init__.py
│   ├── cps_calculator.py  # CPS计算引擎
│   ├── purchase_optimizer.py  # 购买优化器
│   └── simulator.py       # 游戏模拟器
├── analysis/
│   ├── __init__.py
│   ├── predictor.py       # 进度预测器
│   ├── efficiency.py     # 效率分析器
│   └── strategy.py       # 策略分析器
├── utils/
│   ├── __init__.py
│   ├── math_utils.py     # 数学工具
│   └── data_export.py    # 数据导出
└── examples/
    ├── basic_simulation.py
    ├── strategy_comparison.py
    └── ascension_analysis.py
```

### 技术栈选择
- **Python 3.8+**: 主要开发语言
- **NumPy**: 数值计算
- **Pandas**: 数据分析
- **Matplotlib**: 数据可视化
- **Pytest**: 单元测试
- **Jupyter**: 交互式分析

## 应用场景

### 1. 策略优化
- 比较不同购买策略的效率
- 分析最优重生时机
- 评估升级优先级

### 2. 平衡性测试
- 测试数值调整对游戏进度的影响
- 分析建筑物之间的平衡性
- 评估新内容的影响

### 3. 进度规划
- 预测达到特定目标的时间
- 制定长期发展计划
- 优化游戏体验曲线

这个数值模拟系统将为Cookie Clicker的深度分析和优化提供强大的工具支持。
