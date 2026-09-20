# Game Operations Analysis Agent

一个可配置的**游戏运营分析Agent**，自动生成 SaaS 式互动可视化 HTML 报告。

适用于游戏行业研究者、运营从业者、数据分析师，对任意游戏产品的运营情况进行结构化分析并输出专业报告。

## 核心特性

- **互动式 HTML 报告**：不是静态 PDF，而是类似 SaaS 产品官网的可视化报告
- **Chart.js 集成**：支持折线图、柱状图、雷达图等多种图表类型
- **完全可配置**：通过 JSON/YAML 配置文件定义报告内容，无需修改代码
- **组件化设计**：数据卡片、定价卡片、时间线、手风琴折叠面板、提示框等组件
- **品牌定制**：支持自定义 Logo、吉祥物图标、主题配色
- **滚动动画**：fade-in 动画 + 滚动进度条 + 导航高亮
- **响应式布局**：适配桌面端和移动端

## 快速开始

### 安装

```bash
git clone https://github.com/RoderickWilliams/game-ops-analyzer.git
cd game-ops-analyzer
pip install -r requirements.txt
```

### 最简使用

```python
from game_ops_analyzer import GameOpsAgent

agent = GameOpsAgent(game_name="你的游戏名称")
agent.set_subtitle("运营情况深度分析报告")
agent.set_date("截至 2026年9月20日")

# 添加 Hero 统计卡片
agent.add_hero_stat("500万+", "当前DAU（估算）")
agent.add_hero_stat("4", "已完成赛季数")

# 添加章节
ch = agent.add_chapter("ch1", "第一章", "研究背景与方法论", "研究目标与数据来源")
ch.intro = "本报告旨在对游戏运营情况进行系统性回顾与分析。"
ch.paragraphs.append("游戏于2026年3月26日开启公测...")

# 添加图表
from game_ops_analyzer import ChartConfig
ch.charts.append(ChartConfig(
    chart_id="dau",
    chart_type="line",
    title="DAU演变趋势（估算）",
    labels=["3月", "4月", "5月", "6月", "7月", "8月", "9月"],
    datasets=[{
        "label": "DAU（万人）",
        "data": [1300, 900, 750, 520, 560, 580, 600],
        "fill": True,
    }],
))

# 生成报告
agent.generate("report.html")
```

### 使用 JSON 配置文件

```python
from game_ops_analyzer import GameOpsAgent

agent = GameOpsAgent()
agent.load_config("examples/config_template.json")
agent.generate("output/report.html")
```

## 报告结构

生成的报告包含以下区域：

```
┌──────────────────────────────────────────┐
│  导航栏（Logo + 章节导航）                    │
├──────────────────────────────────────────┤
│                                          │
│  Hero 区域                                │
│  ┌──────────┐  游戏名称                   │
│  │ 吉祥物Logo │  副标题                     │
│  └──────────┘  日期                       │
│  ┌─────┬─────┬─────┬─────┐               │
│  │统计卡│统计卡│统计卡│统计卡│              │
│  └─────┴─────┴─────┴─────┘               │
│                                          │
├──────────────────────────────────────────┤
│  第一章 研究背景与方法论                       │
│  - 章节介绍                                │
│  - 小节标题 + 段落                         │
│  - 数据卡片网格                             │
│  - 图表（Chart.js）                       │
│  - 表格                                   │
│  - 时间线                                  │
│  - 手风琴折叠面板                           │
│  - 提示框（info/warn/success）             │
├──────────────────────────────────────────┤
│  第二章 ...                               │
│  ...                                     │
├──────────────────────────────────────────┤
│  参考资料                                  │
├──────────────────────────────────────────┤
│  页脚                                     │
└──────────────────────────────────────────┘
```

## 配置说明

完整的 JSON 配置文件结构：

```json
{
  "game_name": "游戏名称",
  "game_name_en": "Game Name (English)",
  "subtitle": "运营情况深度分析报告",
  "date_text": "截至 2026年9月20日",
  "footer_text": "自定义页脚文字",
  "theme": {
    "primary": "#2B5F88",
    "accent": "#4A90D9",
    "light": "#E8F0F8",
    "bg": "#F0F5FA",
    "dark": "#1a4477"
  },
  "nav_items": [
    {"target": "#ch1", "label": "背景"},
    {"target": "#ch2", "label": "概况"}
  ],
  "hero_stats": [
    {"value": "400+", "label": "可收集精灵总数"},
    {"value": "500万+", "label": "当前DAU"}
  ],
  "chapters": [
    {
      "chapter_id": "ch1",
      "number": "第一章",
      "title": "研究背景与方法论",
      "description": "研究目标与数据来源",
      "intro": "章节介绍文字...",
      "bg_section": false,
      "sections": [
        {"title": "1.1 研究背景", "body": "段落内容..."}
      ],
      "paragraphs": ["独立段落..."],
      "data_cards": [
        {"label": "官方信源", "value": "12+", "desc": "说明文字"}
      ],
      "pricing_cards": [
        {
          "price": "30", "price_unit": "元/月", "note": "月卡",
          "items": ["300洛克钻", "4500分光水晶"]
        },
        {
          "price": "128", "price_unit": "元", "note": "豪华版",
          "featured": true, "badge": "豪华版",
          "items": ["异色宠物蛋", "立升10级"]
        }
      ],
      "timeline_items": [
        {"date": "2026.03.26", "content": "公测上线", "highlight": true}
      ],
      "accordion_items": [
        {"title": "问题一", "content": "详细内容...", "active": true}
      ],
      "callouts": [
        {"title": "分析观点", "content": "观点内容...", "style": "info"}
      ],
      "tables": [
        {
          "headers": ["项目", "内容"],
          "rows": [["类型", "开放世界"]]
        }
      ],
      "charts": [
        {
          "chart_id": "dau",
          "chart_type": "line",
          "title": "DAU趋势图",
          "note": "注：估算数据",
          "labels": ["3月", "4月", "5月"],
          "datasets": [{
            "label": "DAU",
            "data": [1300, 900, 750],
            "fill": true
          }],
          "options": {
            "scales": {
              "y": {"beginAtZero": true}
            }
          }
        }
      ]
    }
  ],
  "references": [
    {"title": "游戏官方网站", "url": "https://example.com"}
  ]
}
```

## 支持的图表类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `line` | 折线图 | DAU趋势、流水变化 |
| `bar` | 柱状图 | 赛季对比、内容量对比 |
| `radar` | 雷达图 | 竞品多维度对比 |
| `doughnut` | 环形图 | 占比分布（非饼图） |
| `scatter` | 散点图 | 相关性分析 |
| `horizontalBar` | 水平柱状图 | 反馈分布对比 |

## API 参考

### GameOpsAgent

| 方法 | 说明 |
|------|------|
| `set_game_name(name, name_en)` | 设置游戏名称 |
| `set_subtitle(text)` | 设置副标题 |
| `set_date(text)` | 设置日期文字 |
| `set_theme(primary, accent, ...)` | 自定义主题配色 |
| `set_logo(path)` | 设置导航栏Logo（自动转base64） |
| `set_mascot(path)` | 设置Hero区域吉祥物（自动转base64） |
| `add_hero_stat(value, label)` | 添加Hero统计卡片 |
| `add_nav_item(target, label)` | 添加导航条目 |
| `add_chapter(id, number, title, ...)` | 添加章节（返回ChapterConfig） |
| `add_reference(title, url)` | 添加参考文献 |
| `load_config(path)` | 从JSON/YAML加载配置 |
| `generate(path)` | 生成HTML报告 |
| `export_config(path)` | 导出当前配置为JSON |

### ChapterConfig

章节配置对象，支持链式追加内容：

```python
ch = agent.add_chapter("ch3", "第三章", "用户规模分析", bg_section=True)
ch.intro = "章节介绍..."
ch.paragraphs.append("分析段落...")
ch.data_cards.append(DataCard(label="峰值DAU", value="1300万", desc="公测首日"))
ch.charts.append(ChartConfig(chart_id="dau", chart_type="line", ...))
ch.callouts.append(CalloutItem(title="观点", content="分析...", style="warn"))
```

## 项目结构

```
game-ops-analyzer/
├── game_ops_analyzer/          # 核心包
│   ├── __init__.py             # 包入口
│   ├── agent.py                # 主Agent类
│   ├── config.py               # 配置数据结构
│   └── generator.py            # HTML报告生成器
├── examples/                   # 示例
│   ├── config_template.json    # 配置模板
│   └── demo.py                 # 演示脚本
├── docs/                       # 文档
│   └── architecture.md         # 架构说明
├── README.md                   # 项目说明
├── LICENSE                     # MIT许可证
├── requirements.txt            # Python依赖
└── setup.py                    # 安装配置
```

## 技术栈

- **Python 3.8+**：核心运行时
- **Chart.js 4.4.0**（通过CDN加载）：图表渲染
- **纯HTML/CSS/JS**：无前端框架依赖，输出自包含HTML文件

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 作者

**RoderickWilliams** - [GitHub](https://github.com/RoderickWilliams)
