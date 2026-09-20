"""
Game Operations Analysis Agent
主Agent类 - 编排数据收集、分析、报告生成的完整流程
"""

import json
import os
import base64
from typing import Optional
from .config import ReportConfig, ChapterConfig, ChartConfig
from .generator import ReportGenerator


class GameOpsAgent:
    """
    游戏运营分析Agent

    用法:
        agent = GameOpsAgent()
        agent.load_config("config.json")
        agent.run(output_path="report.html")

    或链式构建:
        agent = GameOpsAgent(game_name="洛克王国：世界")
        agent.add_chapter(...)
        agent.set_logo("logo.png")
        agent.generate("report.html")
    """

    def __init__(self, game_name: str = "", game_name_en: str = ""):
        self.config = ReportConfig(
            game_name=game_name,
            game_name_en=game_name_en,
        )
        self._chapter_index = 0

    # ===== Configuration Loading =====

    def load_config(self, config_path: str) -> "GameOpsAgent":
        """从JSON/YAML文件加载配置"""
        with open(config_path, "r", encoding="utf-8") as f:
            if config_path.endswith((".yaml", ".yml")):
                import yaml
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        self.config = ReportConfig.from_dict(data)
        self._chapter_index = len(self.config.chapters)
        return self

    def load_config_dict(self, data: dict) -> "GameOpsAgent":
        """从字典加载配置"""
        self.config = ReportConfig.from_dict(data)
        self._chapter_index = len(self.config.chapters)
        return self

    # ===== Basic Setup =====

    def set_game_name(self, name: str, name_en: str = "") -> "GameOpsAgent":
        self.config.game_name = name
        if name_en:
            self.config.game_name_en = name_en
        return self

    def set_subtitle(self, subtitle: str) -> "GameOpsAgent":
        self.config.subtitle = subtitle
        return self

    def set_date(self, date_text: str) -> "GameOpsAgent":
        self.config.date_text = date_text
        return self

    def set_footer(self, footer: str) -> "GameOpsAgent":
        self.config.footer_text = footer
        return self

    def set_theme(self, primary: str = "#2B5F88", accent: str = "#4A90D9",
                  light: str = "#E8F0F8", bg: str = "#F0F5FA",
                  dark: str = "#1a4477") -> "GameOpsAgent":
        self.config.theme_primary = primary
        self.config.theme_accent = accent
        self.config.theme_light = light
        self.config.theme_bg = bg
        self.config.theme_dark = dark
        return self

    # ===== Logo & Images =====

    def set_logo(self, image_path: str) -> "GameOpsAgent":
        """设置导航栏logo（自动转为base64）"""
        self.config.logo_base64 = self._image_to_base64(image_path)
        return self

    def set_mascot(self, image_path: str) -> "GameOpsAgent":
        """设置Hero区域吉祥物图标（自动转为base64）"""
        self.config.mascot_base64 = self._image_to_base64(image_path)
        return self

    def set_logo_base64(self, base64_str: str) -> "GameOpsAgent":
        self.config.logo_base64 = base64_str
        return self

    def set_mascot_base64(self, base64_str: str) -> "GameOpsAgent":
        self.config.mascot_base64 = base64_str
        return self

    @staticmethod
    def _image_to_base64(image_path: str) -> str:
        """将图片文件转为base64字符串"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # ===== Hero Stats =====

    def add_hero_stat(self, value: str, label: str) -> "GameOpsAgent":
        from .config import StatCard
        self.config.hero_stats.append(StatCard(value=value, label=label))
        return self

    # ===== Navigation =====

    def add_nav_item(self, target: str, label: str) -> "GameOpsAgent":
        from .config import NavItem
        self.config.nav_items.append(NavItem(target=target, label=label))
        return self

    # ===== Chapters =====

    def add_chapter(self, chapter_id: str, number: str, title: str,
                    description: str = "", intro: str = "",
                    bg_section: bool = False) -> ChapterConfig:
        """添加章节并返回章节配置对象，可链式追加内容"""
        chapter = ChapterConfig(
            chapter_id=chapter_id,
            number=number,
            title=title,
            description=description,
            intro=intro,
            bg_section=bg_section,
        )
        self.config.chapters.append(chapter)
        self._chapter_index += 1
        return chapter

    def add_chapter_from_dict(self, ch_data: dict) -> "GameOpsAgent":
        """从字典添加完整章节"""
        from .config import (DataCard, PricingCard, TimelineItem,
                              AccordionItem, CalloutItem, ChartConfig)

        chapter = ChapterConfig(
            chapter_id=ch_data["chapter_id"],
            number=ch_data["number"],
            title=ch_data["title"],
            description=ch_data.get("description", ""),
            intro=ch_data.get("intro", ""),
            bg_section=ch_data.get("bg_section", False),
        )
        chapter.sections = ch_data.get("sections", [])
        chapter.paragraphs = ch_data.get("paragraphs", [])

        for dc in ch_data.get("data_cards", []):
            chapter.data_cards.append(DataCard(**dc))
        for pc in ch_data.get("pricing_cards", []):
            chapter.pricing_cards.append(PricingCard(**pc))
        for ti in ch_data.get("timeline_items", []):
            chapter.timeline_items.append(TimelineItem(**ti))
        for ai in ch_data.get("accordion_items", []):
            chapter.accordion_items.append(AccordionItem(**ai))
        for cl in ch_data.get("callouts", []):
            chapter.callouts.append(CalloutItem(**cl))
        for tb in ch_data.get("tables", []):
            chapter.tables.append(tb)
        for cc in ch_data.get("charts", []):
            chapter.charts.append(ChartConfig(**cc))

        self.config.chapters.append(chapter)
        self._chapter_index += 1
        return self

    # ===== References =====

    def add_reference(self, title: str, url: str = "") -> "GameOpsAgent":
        from .config import ReferenceItem
        self.config.references.append(ReferenceItem(title=title, url=url))
        return self

    # ===== Generation =====

    def generate(self, output_path: str) -> str:
        """生成HTML报告"""
        generator = ReportGenerator(self.config)
        return generator.generate(output_path)

    def run(self, output_path: str = "report.html") -> str:
        """运行完整流程并生成报告"""
        return self.generate(output_path)

    # ===== Export Config =====

    def export_config(self, path: str) -> str:
        """导出当前配置为JSON文件"""
        data = {
            "game_name": self.config.game_name,
            "game_name_en": self.config.game_name_en,
            "subtitle": self.config.subtitle,
            "date_text": self.config.date_text,
            "footer_text": self.config.footer_text,
            "theme": {
                "primary": self.config.theme_primary,
                "accent": self.config.theme_accent,
                "light": self.config.theme_light,
                "bg": self.config.theme_bg,
                "dark": self.config.theme_dark,
            },
            "nav_items": [{"target": n.target, "label": n.label} for n in self.config.nav_items],
            "hero_stats": [{"value": s.value, "label": s.label} for s in self.config.hero_stats],
            "references": [{"title": r.title, "url": r.url} for r in self.config.references],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
