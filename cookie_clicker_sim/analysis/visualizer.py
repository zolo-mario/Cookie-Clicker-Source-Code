"""
数据可视化工具

提供Cookie Clicker模拟数据的图表绘制功能
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import seaborn as sns

# 设置英文字体和样式
plt.rcParams['font.family'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("husl")


class DataVisualizer:
    """数据可视化器"""
    
    def __init__(self, figsize=(12, 8), dpi=100):
        self.figsize = figsize
        self.dpi = dpi
        self.colors = plt.cm.Set3(np.linspace(0, 1, 12))
        
    def plot_progress_curve(self, time_data: List[float], cookies_data: List[float],
                           cps_data: List[float], title: str = "Game Progress Curve") -> plt.Figure:
        """
        Plot game progress curve (cookies and CPS over time)
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, dpi=self.dpi)

        # Convert time to hours
        time_hours = [t / 3600 for t in time_data]

        # Cookies curve
        ax1.plot(time_hours, cookies_data, 'b-', linewidth=2, label='Cookies')
        ax1.set_ylabel('Cookies', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Use scientific notation for large numbers
        ax1.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

        # CPS curve
        ax2.plot(time_hours, cps_data, 'r-', linewidth=2, label='Cookies per Second (CPS)')
        ax2.set_xlabel('Time (hours)', fontsize=12)
        ax2.set_ylabel('CPS', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        plt.tight_layout()
        return fig
    
    def plot_building_distribution(self, buildings_data: Dict[str, int],
                                 title: str = "Building Distribution") -> plt.Figure:
        """
        Plot building quantity distribution pie chart
        """
        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        # Filter out buildings with 0 quantity
        filtered_data = {k: v for k, v in buildings_data.items() if v > 0}

        if not filtered_data:
            ax.text(0.5, 0.5, 'No Buildings', ha='center', va='center',
                   transform=ax.transAxes, fontsize=16)
            ax.set_title(title, fontsize=14, fontweight='bold')
            return fig

        names = list(filtered_data.keys())
        values = list(filtered_data.values())

        # Create pie chart
        wedges, texts, autotexts = ax.pie(values, labels=names, autopct='%1.1f%%',
                                         startangle=90, colors=self.colors[:len(names)])

        # Beautify text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title(title, fontsize=14, fontweight='bold')

        # Add legend
        ax.legend(wedges, [f'{name}: {value}' for name, value in zip(names, values)],
                 title="Building Count", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        return fig
    
    def plot_cps_breakdown(self, cps_breakdown: Dict[str, float],
                          title: str = "CPS Source Analysis") -> plt.Figure:
        """
        Plot CPS source breakdown bar chart
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Filter numeric data
        filtered_data = {}
        for k, v in cps_breakdown.items():
            if isinstance(v, (int, float)) and v > 0:
                filtered_data[k] = v

        if not filtered_data:
            ax.text(0.5, 0.5, 'No CPS Data', ha='center', va='center',
                   transform=ax.transAxes, fontsize=16)
            ax.set_title(title, fontsize=14, fontweight='bold')
            return fig

        names = list(filtered_data.keys())
        values = list(filtered_data.values())

        # Create bar chart
        bars = ax.bar(names, values, color=self.colors[:len(names)])

        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}', ha='center', va='bottom', fontweight='bold')

        ax.set_ylabel('CPS Contribution', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def plot_efficiency_comparison(self, efficiency_data: List[Tuple[str, float]],
                                 title: str = "Purchase Efficiency Comparison") -> plt.Figure:
        """
        Plot purchase efficiency comparison chart
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        if not efficiency_data:
            ax.text(0.5, 0.5, 'No Efficiency Data', ha='center', va='center',
                   transform=ax.transAxes, fontsize=16)
            ax.set_title(title, fontsize=14, fontweight='bold')
            return fig

        # Sort by efficiency
        efficiency_data.sort(key=lambda x: x[1], reverse=True)

        names = [item[0] for item in efficiency_data]
        values = [item[1] for item in efficiency_data]

        # Create horizontal bar chart
        bars = ax.barh(names, values, color=self.colors[:len(names)])

        # Add value labels
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{value:.6f}', ha='left', va='center', fontweight='bold')

        ax.set_xlabel('Efficiency (CPS Gain/Price)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        return fig
    
    def plot_prestige_analysis(self, cookies_data: List[float], prestige_data: List[float],
                             title: str = "Prestige Analysis") -> plt.Figure:
        """
        Plot prestige vs cookies relationship chart
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=self.dpi)

        # Prestige over time
        ax1.plot(range(len(prestige_data)), prestige_data, 'g-', linewidth=2, marker='o')
        ax1.set_xlabel('Time Steps', fontsize=12)
        ax1.set_ylabel('Prestige Level', fontsize=12)
        ax1.set_title('Prestige Level Changes', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Cookies vs prestige relationship
        ax2.scatter(cookies_data, prestige_data, alpha=0.6, c=range(len(cookies_data)),
                   cmap='viridis', s=50)
        ax2.set_xlabel('Cookies', fontsize=12)
        ax2.set_ylabel('Prestige Level', fontsize=12)
        ax2.set_title('Cookies vs Prestige Level', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))

        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_strategy_comparison(self, strategy_results: Dict[str, Dict[str, Any]],
                               title: str = "Strategy Comparison Analysis") -> plt.Figure:
        """
        Plot multi-strategy comparison chart
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12), dpi=self.dpi)

        strategies = list(strategy_results.keys())
        colors = self.colors[:len(strategies)]

        # Final cookies comparison
        final_cookies = [strategy_results[s]['final_cookies'] for s in strategies]
        bars1 = ax1.bar(strategies, final_cookies, color=colors)
        ax1.set_ylabel('Final Cookies', fontsize=12)
        ax1.set_title('Final Cookies Comparison', fontsize=12, fontweight='bold')
        ax1.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

        # Add value labels
        for bar, value in zip(bars1, final_cookies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2e}', ha='center', va='bottom', fontweight='bold')

        # Final CPS comparison
        final_cps = [strategy_results[s]['final_cps'] for s in strategies]
        bars2 = ax2.bar(strategies, final_cps, color=colors)
        ax2.set_ylabel('Final CPS', fontsize=12)
        ax2.set_title('Final CPS Comparison', fontsize=12, fontweight='bold')
        ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

        for bar, value in zip(bars2, final_cps):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2e}', ha='center', va='bottom', fontweight='bold')

        # Purchase count comparison
        purchases = [strategy_results[s]['total_purchases'] for s in strategies]
        bars3 = ax3.bar(strategies, purchases, color=colors)
        ax3.set_ylabel('Total Purchases', fontsize=12)
        ax3.set_title('Purchase Count Comparison', fontsize=12, fontweight='bold')

        for bar, value in zip(bars3, purchases):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value}', ha='center', va='bottom', fontweight='bold')

        # Efficiency comparison (cookies/time)
        efficiency = [strategy_results[s]['efficiency'] for s in strategies]
        bars4 = ax4.bar(strategies, efficiency, color=colors)
        ax4.set_ylabel('Efficiency (Cookies/Hour)', fontsize=12)
        ax4.set_title('Strategy Efficiency Comparison', fontsize=12, fontweight='bold')
        ax4.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

        for bar, value in zip(bars4, efficiency):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2e}', ha='center', va='bottom', fontweight='bold')

        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_building_efficiency_curve(self, building_name: str,
                                     amounts: List[int], efficiencies: List[float],
                                     title: str = None) -> plt.Figure:
        """
        Plot building efficiency curve
        """
        if title is None:
            title = f"{building_name} Efficiency Curve"

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        ax.plot(amounts, efficiencies, 'b-', linewidth=2, marker='o', markersize=4)
        ax.set_xlabel(f'{building_name} Count', fontsize=12)
        ax.set_ylabel('Purchase Efficiency (CPS Gain/Price)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Mark highest efficiency point
        max_idx = np.argmax(efficiencies)
        ax.annotate(f'Peak Efficiency\n({amounts[max_idx]}, {efficiencies[max_idx]:.6f})',
                   xy=(amounts[max_idx], efficiencies[max_idx]),
                   xytext=(amounts[max_idx] + len(amounts)*0.1, efficiencies[max_idx]),
                   arrowprops=dict(arrowstyle='->', color='red'),
                   fontsize=10, ha='left')
        
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """
        Save chart to file
        """
        fig.savefig(filename, dpi=dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        print(f"Chart saved to: {filename}")
    
    def show_all_figures(self):
        """
        Show all charts
        """
        plt.show()

    def close_all_figures(self):
        """
        Close all charts
        """
        plt.close('all')
