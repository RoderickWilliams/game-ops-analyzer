"""
演示脚本 - 使用配置文件生成报告
"""
import os
import sys

# 将项目根目录加入路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_ops_analyzer import GameOpsAgent


def demo_with_config():
    """方式一：使用JSON配置文件"""
    agent = GameOpsAgent()
    config_path = os.path.join(os.path.dirname(__file__), "config_template.json")
    agent.load_config(config_path)
    output = os.path.join(os.path.dirname(__file__), "demo_report.html")
    agent.generate(output)
    print(f"报告已生成: {output}")


def demo_with_code():
    """方式二：使用代码链式构建"""
    from game_ops_analyzer import ChartConfig

    agent = GameOpsAgent(game_name="我的游戏")
    agent.set_subtitle("运营情况分析报告")
    agent.set_date("截至 2026年9月20日")
    agent.set_theme(primary="#2B5F88", accent="#4A90D9")

    agent.add_hero_stat("100万", "DAU")
    agent.add_hero_stat("3", "赛季数")
    agent.add_nav_item("#ch1", "背景")
    agent.add_nav_item("#ch2", "数据")

    ch = agent.add_chapter("ch1", "第一章", "研究背景", "研究目标")
    ch.intro = "本报告对游戏运营情况进行分析。"
    ch.paragraphs.append("游戏于2026年上线，运营至今。")

    ch2 = agent.add_chapter("ch2", "第二章", "数据分析", "DAU趋势", bg_section=True)
    ch2.charts.append(ChartConfig(
        chart_id="dau",
        chart_type="line",
        title="DAU趋势图",
        labels=["1月", "2月", "3月", "4月", "5月"],
        datasets=[{
            "label": "DAU（万）",
            "data": [100, 120, 90, 85, 80],
            "fill": True,
        }],
    ))

    agent.add_reference("游戏官网", "https://example.com")

    output = os.path.join(os.path.dirname(__file__), "code_report.html")
    agent.generate(output)
    print(f"报告已生成: {output}")


def demo_with_logo():
    """方式三：使用自定义Logo"""
    agent = GameOpsAgent(game_name="带Logo的游戏")

    # 如果有logo图片文件，可以自动转base64嵌入
    # agent.set_logo("path/to/logo.png")
    # agent.set_mascot("path/to/mascot.png")

    agent.set_subtitle("运营分析报告")
    agent.set_date("截至 2026年9月20日")
    agent.add_hero_stat("500万", "DAU")
    agent.add_nav_item("#ch1", "概况")

    ch = agent.add_chapter("ch1", "第一章", "游戏概况", "基本信息")
    ch.intro = "游戏基本信息概述。"

    output = os.path.join(os.path.dirname(__file__), "logo_report.html")
    agent.generate(output)
    print(f"报告已生成: {output}")


if __name__ == "__main__":
    print("=== 演示一：JSON配置文件 ===")
    demo_with_config()
    print("\n=== 演示二：代码链式构建 ===")
    demo_with_code()
    print("\n=== 演示三：自定义Logo ===")
    demo_with_logo()
    print("\n所有演示完成！")
