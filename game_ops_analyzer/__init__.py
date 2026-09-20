"""
Game Operations Analysis Agent
一个可配置的游戏运营情况分析Agent，生成SaaS式互动可视化HTML报告
"""

from .agent import GameOpsAgent
from .config import ReportConfig, ChapterConfig, ChartConfig
from .generator import ReportGenerator

__version__ = "1.0.0"
__author__ = "RoderickWilliams"
__all__ = ["GameOpsAgent", "ReportConfig", "ChapterConfig", "ChartConfig", "ReportGenerator"]
