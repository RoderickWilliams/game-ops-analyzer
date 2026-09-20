"""
配置数据结构定义
使用 dataclass 定义清晰的配置模型，支持 YAML/JSON 加载
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChartConfig:
    """单个图表的配置"""
    chart_id: str
    chart_type: str  # line, bar, radar, doughnut, scatter
    title: str
    note: str = ""
    labels: list = field(default_factory=list)
    datasets: list = field(default_factory=list)
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "chart_id": self.chart_id,
            "chart_type": self.chart_type,
            "title": self.title,
            "note": self.note,
            "labels": self.labels,
            "datasets": self.datasets,
            "options": self.options,
        }


@dataclass
class StatCard:
    """Hero区域统计卡片"""
    value: str
    label: str


@dataclass
class PricingCard:
    """付费系统定价卡片"""
    price: str
    price_unit: str = ""
    note: str = ""
    featured: bool = False
    badge: str = ""
    items: list = field(default_factory=list)


@dataclass
class DataCard:
    """通用数据卡片"""
    label: str
    value: str
    desc: str = ""


@dataclass
class TimelineItem:
    """时间线条目"""
    date: str
    content: str
    highlight: bool = False


@dataclass
class AccordionItem:
    """手风琴折叠项"""
    title: str
    content: str
    active: bool = False


@dataclass
class CalloutItem:
    """提示框"""
    title: str
    content: str
    style: str = "info"  # info, warn, success


@dataclass
class ReferenceItem:
    """参考文献"""
    title: str
    url: str = ""


@dataclass
class ChapterConfig:
    """单个章节的配置"""
    chapter_id: str
    number: str  # e.g. "第一章"
    title: str
    description: str = ""
    intro: str = ""
    sections: list = field(default_factory=list)  # subsections: list of dict
    data_cards: list = field(default_factory=list)  # list[DataCard]
    pricing_cards: list = field(default_factory=list)  # list[PricingCard]
    timeline_items: list = field(default_factory=list)  # list[TimelineItem]
    accordion_items: list = field(default_factory=list)  # list[AccordionItem]
    callouts: list = field(default_factory=list)  # list[CalloutItem]
    tables: list = field(default_factory=list)  # list of {headers, rows}
    charts: list = field(default_factory=list)  # list[ChartConfig]
    paragraphs: list = field(default_factory=list)  # list of str (HTML paragraphs)
    bg_section: bool = False  # 是否使用灰色背景


@dataclass
class NavItem:
    """导航条目"""
    target: str  # e.g. "#ch1"
    label: str


@dataclass
class ReportConfig:
    """报告总配置"""
    game_name: str = ""
    game_name_en: str = ""
    subtitle: str = "运营情况深度分析报告"
    date_text: str = ""
    nav_items: list = field(default_factory=list)  # list[NavItem]
    hero_stats: list = field(default_factory=list)  # list[StatCard]
    chapters: list = field(default_factory=list)  # list[ChapterConfig]
    references: list = field(default_factory=list)  # list[ReferenceItem]
    footer_text: str = ""
    logo_base64: str = ""  # base64 encoded logo image
    mascot_base64: str = ""  # base64 encoded mascot image
    theme_primary: str = "#2B5F88"
    theme_accent: str = "#4A90D9"
    theme_light: str = "#E8F0F8"
    theme_bg: str = "#F0F5FA"
    theme_dark: str = "#1a4477"

    @classmethod
    def from_dict(cls, data: dict) -> "ReportConfig":
        """从字典构建配置"""
        config = cls()
        config.game_name = data.get("game_name", "")
        config.game_name_en = data.get("game_name_en", "")
        config.subtitle = data.get("subtitle", "运营情况深度分析报告")
        config.date_text = data.get("date_text", "")
        config.footer_text = data.get("footer_text", "")
        config.logo_base64 = data.get("logo_base64", "")
        config.mascot_base64 = data.get("mascot_base64", "")

        theme = data.get("theme", {})
        config.theme_primary = theme.get("primary", config.theme_primary)
        config.theme_accent = theme.get("accent", config.theme_accent)
        config.theme_light = theme.get("light", config.theme_light)
        config.theme_bg = theme.get("bg", config.theme_bg)
        config.theme_dark = theme.get("dark", config.theme_dark)

        for nav in data.get("nav_items", []):
            config.nav_items.append(NavItem(**nav))

        for stat in data.get("hero_stats", []):
            config.hero_stats.append(StatCard(**stat))

        for ref in data.get("references", []):
            config.references.append(ReferenceItem(**ref))

        for ch in data.get("chapters", []):
            chapter = ChapterConfig(
                chapter_id=ch["chapter_id"],
                number=ch["number"],
                title=ch["title"],
                description=ch.get("description", ""),
                intro=ch.get("intro", ""),
                bg_section=ch.get("bg_section", False),
            )
            for s in ch.get("sections", []):
                chapter.sections.append(s)
            for dc in ch.get("data_cards", []):
                chapter.data_cards.append(DataCard(**dc))
            for pc in ch.get("pricing_cards", []):
                chapter.pricing_cards.append(PricingCard(**pc))
            for ti in ch.get("timeline_items", []):
                chapter.timeline_items.append(TimelineItem(**ti))
            for ai in ch.get("accordion_items", []):
                chapter.accordion_items.append(AccordionItem(**ai))
            for cl in ch.get("callouts", []):
                chapter.callouts.append(CalloutItem(**cl))
            for tb in ch.get("tables", []):
                chapter.tables.append(tb)
            for cc in ch.get("charts", []):
                chapter.charts.append(ChartConfig(**cc))
            chapter.paragraphs = ch.get("paragraphs", [])
            config.chapters.append(chapter)

        return config
