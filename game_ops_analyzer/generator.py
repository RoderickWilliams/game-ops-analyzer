"""
HTML报告生成器
将配置渲染为SaaS式互动可视化HTML报告
"""

import os
import json
from typing import Optional
from .config import ReportConfig, ChapterConfig


class ReportGenerator:
    """HTML报告生成器"""

    def __init__(self, config: ReportConfig):
        self.config = config
        self._css_cache = None
        self._js_cache = None

    def generate(self, output_path: str) -> str:
        """生成HTML报告并保存到指定路径"""
        html = self._build_html()
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path

    def _build_html(self) -> str:
        """构建完整HTML文档"""
        parts = [
            self._build_head(),
            '<body>',
            self._build_progress_bar(),
            self._build_navbar(),
            self._build_hero(),
        ]
        for chapter in self.config.chapters:
            parts.append(self._build_chapter(chapter))
        parts.append(self._build_references())
        parts.append(self._build_footer())
        parts.append(self._build_scripts())
        parts.append('</body>')
        parts.append('</html>')
        return '\n'.join(parts)

    # ===== HTML Head =====
    def _build_head(self) -> str:
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{self.config.game_name} · {self.config.subtitle}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
{self._build_css()}
</style>
</head>'''

    # ===== CSS =====
    def _build_css(self) -> str:
        c = self.config
        return f''':root {{
  --blue-dark: {c.theme_dark};
  --blue-primary: {c.theme_primary};
  --blue-accent: {c.theme_accent};
  --blue-light: {c.theme_light};
  --blue-bg: {c.theme_bg};
  --text-primary: #1a1a1a;
  --text-secondary: #4a4a4a;
  --text-tertiary: #8a8a8a;
  --bg-white: #ffffff;
  --bg-section: #fafbfc;
  --border-color: #e4e7ec;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.10);
  --radius: 8px;
  --radius-lg: 12px;
  --font-cn: "Microsoft YaHei", "微软雅黑", "PingFang SC", sans-serif;
  --font-en: "Times New Roman", "Times", serif;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; font-size: 16px; }}
body {{ font-family: var(--font-cn); color: var(--text-primary); background: var(--bg-white); line-height: 1.75; overflow-x: hidden; }}
body::-webkit-scrollbar {{ width: 8px; }}
body::-webkit-scrollbar-track {{ background: var(--bg-section); }}
body::-webkit-scrollbar-thumb {{ background: var(--blue-accent); border-radius: 4px; }}

#progress-bar {{ position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--blue-dark), var(--blue-accent)); width: 0%; z-index: 9999; transition: width 0.1s; }}

.navbar {{ position: fixed; top: 0; left: 0; right: 0; height: 56px; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border-color); z-index: 1000; display: flex; align-items: center; padding: 0 24px; gap: 32px; }}
.nav-logo {{ height: 40px; display: flex; align-items: center; flex-shrink: 0; }}
.nav-logo img {{ max-height: 36px; width: auto; }}
.nav-links {{ display: flex; gap: 4px; list-style: none; overflow-x: auto; scrollbar-width: none; flex: 1; }}
.nav-links::-webkit-scrollbar {{ display: none; }}
.nav-links li a {{ display: block; padding: 6px 12px; font-size: 13px; color: var(--text-secondary); text-decoration: none; border-radius: 6px; white-space: nowrap; transition: var(--transition); }}
.nav-links li a:hover, .nav-links li a.active {{ color: var(--blue-primary); background: var(--blue-light); }}

.hero {{ min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background: linear-gradient(135deg, #f8fbff 0%, #eef5fb 100%); padding: 80px 20px 60px; position: relative; overflow: hidden; }}
.hero::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 30% 40%, rgba(74,144,217,0.08) 0%, transparent 50%), radial-gradient(circle at 70% 60%, rgba(43,95,136,0.06) 0%, transparent 50%); pointer-events: none; }}
.hero-content {{ text-align: center; max-width: 900px; position: relative; z-index: 1; }}
.hero-logo {{ width: 120px; height: 120px; margin: 0 auto 24px; }}
.hero-logo img {{ width: 100%; height: 100%; object-fit: contain; }}
.hero h1 {{ font-size: 2.8rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; letter-spacing: 2px; }}
.hero .subtitle {{ font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 4px; }}
.hero .date {{ font-size: 0.9rem; color: var(--text-tertiary); margin-bottom: 40px; }}
.hero-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; max-width: 800px; margin: 0 auto; }}
.stat-card {{ background: rgba(255,255,255,0.8); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px 16px; text-align: center; transition: var(--transition); backdrop-filter: blur(4px); }}
.stat-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--blue-accent); }}
.stat-card .stat-value {{ font-size: 2rem; font-weight: 700; color: var(--blue-primary); font-family: var(--font-en); line-height: 1.2; }}
.stat-card .stat-label {{ font-size: 0.8rem; color: var(--text-tertiary); margin-top: 4px; }}
.scroll-hint {{ position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); font-size: 0.75rem; color: var(--text-tertiary); animation: bounce 2s infinite; }}
@keyframes bounce {{ 0%, 100% {{ transform: translateX(-50%) translateY(0); }} 50% {{ transform: translateX(-50%) translateY(-8px); }} }}

.section {{ padding: 64px 20px; max-width: 1100px; margin: 0 auto; }}
.section-header {{ margin-bottom: 32px; border-left: 4px solid var(--blue-primary); padding-left: 16px; }}
.section-num {{ font-size: 0.8rem; color: var(--blue-accent); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }}
.section-title {{ font-size: 1.75rem; font-weight: 700; color: var(--text-primary); }}
.section-desc {{ font-size: 0.95rem; color: var(--text-tertiary); margin-top: 4px; }}

.chapter-intro {{ background: var(--blue-bg); border-radius: var(--radius-lg); padding: 20px 24px; margin-bottom: 28px; font-size: 0.95rem; color: var(--text-secondary); border-left: 3px solid var(--blue-accent); }}
.subsection-title {{ font-size: 1.2rem; font-weight: 600; color: var(--text-primary); margin: 28px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border-color); }}
.subsection-title::before {{ content: '▎'; color: var(--blue-primary); margin-right: 6px; }}
p {{ margin-bottom: 14px; font-size: 0.95rem; color: var(--text-secondary); }}
strong {{ color: var(--text-primary); }}
.highlight {{ background: var(--blue-light); padding: 1px 4px; border-radius: 3px; }}

.data-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 20px 0; }}
.data-card {{ background: var(--bg-white); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px; transition: var(--transition); }}
.data-card:hover {{ box-shadow: var(--shadow-md); border-color: var(--blue-accent); }}
.data-card .card-label {{ font-size: 0.8rem; color: var(--text-tertiary); }}
.data-card .card-value {{ font-size: 1.6rem; font-weight: 700; color: var(--blue-primary); font-family: var(--font-en); margin: 4px 0; }}
.data-card .card-desc {{ font-size: 0.85rem; color: var(--text-tertiary); }}

.pricing-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 24px 0; }}
.pricing-card {{ background: var(--bg-white); border: 2px solid var(--border-color); border-radius: var(--radius-lg); padding: 24px 20px; text-align: center; transition: var(--transition); position: relative; }}
.pricing-card.featured {{ border-color: var(--blue-primary); box-shadow: 0 4px 20px rgba(43,95,136,0.1); }}
.pricing-card .badge {{ position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--blue-primary); color: white; font-size: 0.7rem; padding: 2px 12px; border-radius: 20px; white-space: nowrap; }}
.pricing-card .price {{ font-size: 1.8rem; font-weight: 700; color: var(--text-primary); font-family: var(--font-en); margin: 8px 0; }}
.pricing-card .price-unit {{ font-size: 0.85rem; color: var(--text-tertiary); }}
.pricing-card .price-note {{ font-size: 0.75rem; color: var(--text-tertiary); margin-top: 4px; }}
.pricing-card ul {{ list-style: none; text-align: left; margin-top: 16px; font-size: 0.85rem; }}
.pricing-card ul li {{ padding: 4px 0; color: var(--text-secondary); border-bottom: 1px dashed var(--border-color); }}
.pricing-card ul li:last-child {{ border-bottom: none; }}
.pricing-card ul li::before {{ content: '\\2713 '; color: var(--blue-accent); font-weight: 700; }}

.table-wrap {{ overflow-x: auto; margin: 20px 0; border-radius: var(--radius); border: 1px solid var(--border-color); }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
th {{ background: var(--blue-bg); color: var(--text-primary); font-weight: 600; padding: 10px 14px; text-align: left; border-bottom: 2px solid var(--border-color); white-space: nowrap; }}
td {{ padding: 8px 14px; border-bottom: 1px solid var(--border-color); color: var(--text-secondary); }}
tr:last-child td {{ border-bottom: none; }}
tr:hover td {{ background: var(--blue-bg); }}

.timeline {{ position: relative; padding-left: 32px; margin: 24px 0; }}
.timeline::before {{ content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: var(--blue-accent); opacity: 0.3; }}
.timeline-item {{ position: relative; margin-bottom: 24px; }}
.timeline-item::before {{ content: ''; position: absolute; left: -28px; top: 4px; width: 12px; height: 12px; border-radius: 50%; background: var(--blue-accent); border: 2px solid white; box-shadow: 0 0 0 2px var(--blue-accent); }}
.timeline-date {{ font-size: 0.8rem; color: var(--blue-primary); font-weight: 600; font-family: var(--font-en); }}
.timeline-content {{ margin-top: 4px; font-size: 0.9rem; color: var(--text-secondary); }}
.timeline-content strong {{ color: var(--text-primary); }}

.chart-container {{ background: var(--bg-white); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px; margin: 20px 0; box-shadow: var(--shadow-sm); }}
.chart-title {{ font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }}
.chart-note {{ font-size: 0.75rem; color: var(--text-tertiary); margin-bottom: 12px; }}
.chart-canvas-wrap {{ position: relative; width: 100%; }}
.chart-canvas-wrap canvas {{ max-height: 400px; }}

.accordion {{ margin: 20px 0; border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border-color); }}
.accordion-item {{ border-bottom: 1px solid var(--border-color); }}
.accordion-item:last-child {{ border-bottom: none; }}
.accordion-header {{ padding: 12px 16px; cursor: pointer; font-weight: 600; font-size: 0.9rem; color: var(--text-primary); background: var(--bg-section); display: flex; justify-content: space-between; align-items: center; transition: var(--transition); }}
.accordion-header:hover {{ background: var(--blue-bg); }}
.accordion-header .arrow {{ transition: transform 0.3s; font-size: 0.75rem; color: var(--text-tertiary); }}
.accordion-item.active .accordion-header .arrow {{ transform: rotate(180deg); }}
.accordion-body {{ max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }}
.accordion-item.active .accordion-body {{ max-height: 2000px; }}
.accordion-content {{ padding: 16px; font-size: 0.88rem; color: var(--text-secondary); }}

.callout {{ background: var(--blue-bg); border-left: 4px solid var(--blue-primary); padding: 16px 20px; margin: 20px 0; border-radius: 0 var(--radius) var(--radius) 0; font-size: 0.9rem; color: var(--text-secondary); }}
.callout.warn {{ background: #fff5f5; border-left-color: #c0392b; }}
.callout.success {{ background: #f0fbf4; border-left-color: #27ae60; }}
.callout-title {{ font-weight: 700; color: var(--text-primary); margin-bottom: 4px; font-size: 0.9rem; }}

.quote-block {{ border-left: 3px solid var(--blue-accent); padding: 8px 16px; margin: 16px 0; font-size: 0.88rem; color: var(--text-tertiary); font-style: italic; background: var(--bg-section); border-radius: 0 var(--radius) var(--radius) 0; }}

.references {{ background: var(--bg-section); border-radius: var(--radius-lg); padding: 28px; margin: 40px 0; }}
.references h3 {{ font-size: 1.1rem; margin-bottom: 12px; }}
.ref-list {{ list-style: none; counter-reset: ref-counter; }}
.ref-list li {{ counter-increment: ref-counter; padding: 6px 0 6px 28px; position: relative; font-size: 0.82rem; color: var(--text-secondary); border-bottom: 1px dashed var(--border-color); }}
.ref-list li::before {{ content: counter(ref-counter); position: absolute; left: 0; top: 6px; font-size: 0.75rem; color: var(--blue-accent); font-weight: 700; }}
.ref-list a {{ color: var(--blue-accent); text-decoration: none; }}
.ref-list a:hover {{ text-decoration: underline; }}

.footer {{ text-align: center; padding: 40px 20px; background: var(--bg-section); border-top: 1px solid var(--border-color); }}
.footer p {{ font-size: 0.8rem; color: var(--text-tertiary); }}

.fade-in {{ opacity: 0; transform: translateY(20px); transition: opacity 0.6s, transform 0.6s; }}
.fade-in.visible {{ opacity: 1; transform: translateY(0); }}

@media (max-width: 768px) {{
  .hero h1 {{ font-size: 2rem; }}
  .hero-stats {{ grid-template-columns: repeat(2, 1fr); }}
  .section {{ padding: 48px 16px; }}
  .nav-links {{ display: none; }}
}}'''

    # ===== Progress Bar =====
    def _build_progress_bar(self) -> str:
        return '<div id="progress-bar"></div>'

    # ===== Navbar =====
    def _build_navbar(self) -> str:
        logo_html = ""
        if self.config.logo_base64:
            logo_html = f'<div class="nav-logo"><img src="data:image/png;base64,{self.config.logo_base64}" alt="{self.config.game_name}"></div>'
        else:
            logo_html = f'<div class="nav-logo" style="font-weight:700;font-size:18px;color:var(--blue-primary);">{self.config.game_name}</div>'

        nav_links = ""
        for item in self.config.nav_items:
            nav_links += f'<li><a href="{item.target}">{item.label}</a></li>\n'

        return f'''<nav class="navbar">
{logo_html}
<ul class="nav-links">
{nav_links}
</ul>
</nav>'''

    # ===== Hero =====
    def _build_hero(self) -> str:
        mascot_html = ""
        if self.config.mascot_base64:
            mascot_html = f'<div class="hero-logo"><img src="data:image/png;base64,{self.config.mascot_base64}" alt="logo"></div>'

        stats_html = '<div class="hero-stats">'
        for stat in self.config.hero_stats:
            stats_html += f'''<div class="stat-card">
<div class="stat-value">{stat.value}</div>
<div class="stat-label">{stat.label}</div>
</div>'''
        stats_html += '</div>'

        return f'''<header class="hero">
<div class="hero-content">
{mascot_html}
<h1>{self.config.game_name}</h1>
<p class="subtitle">{self.config.subtitle}</p>
<p class="date">{self.config.date_text}</p>
{stats_html}
</div>
<div class="scroll-hint">向下滚动浏览报告 ↓</div>
</header>'''

    # ===== Chapter =====
    def _build_chapter(self, ch: ChapterConfig) -> str:
        bg_style = ' style="background: var(--bg-section);"' if ch.bg_section else ''
        parts = [f'<section id="{ch.chapter_id}" class="section"{bg_style}>']

        # Section header
        parts.append(f'''<div class="section-header fade-in">
<div class="section-num">{ch.number}</div>
<h2 class="section-title">{ch.title}</h2>
<p class="section-desc">{ch.description}</p>
</div>''')

        # Chapter intro
        if ch.intro:
            parts.append(f'<div class="chapter-intro fade-in">{ch.intro}</div>')

        # Subsections
        for s in ch.sections:
            if isinstance(s, dict):
                title = s.get("title", "")
                body = s.get("body", "")
                parts.append(f'<h3 class="subsection-title fade-in">{title}</h3>')
                if body:
                    parts.append(f'<p class="fade-in">{body}</p>')
            elif isinstance(s, str):
                parts.append(f'<h3 class="subsection-title fade-in">{s}</h3>')

        # Paragraphs
        for p in ch.paragraphs:
            parts.append(f'<p class="fade-in">{p}</p>')

        # Data cards
        if ch.data_cards:
            parts.append('<div class="data-grid fade-in">')
            for dc in ch.data_cards:
                parts.append(f'''<div class="data-card">
<div class="card-label">{dc.label}</div>
<div class="card-value">{dc.value}</div>
<div class="card-desc">{dc.desc}</div>
</div>''')
            parts.append('</div>')

        # Pricing cards
        if ch.pricing_cards:
            parts.append('<div class="pricing-grid fade-in">')
            for pc in ch.pricing_cards:
                featured_class = " featured" if pc.featured else ""
                badge_html = f'<div class="badge">{pc.badge}</div>' if pc.badge else ""
                items_html = ""
                if pc.items:
                    items_html = "<ul>"
                    for item in pc.items:
                        items_html += f"<li>{item}</li>"
                    items_html += "</ul>"
                parts.append(f'''<div class="pricing-card{featured_class}">
{badge_html}
<div class="price">{pc.price}<span class="price-unit">{pc.price_unit}</span></div>
<div class="price-note">{pc.note}</div>
{items_html}
</div>''')
            parts.append('</div>')

        # Timeline
        if ch.timeline_items:
            parts.append('<div class="timeline fade-in">')
            for ti in ch.timeline_items:
                parts.append(f'''<div class="timeline-item">
<div class="timeline-date">{ti.date}</div>
<div class="timeline-content">{ti.content}</div>
</div>''')
            parts.append('</div>')

        # Charts
        for chart in ch.charts:
            parts.append(self._build_chart(chart))

        # Tables
        for table in ch.tables:
            parts.append(self._build_table(table))

        # Accordion
        if ch.accordion_items:
            parts.append('<div class="accordion fade-in">')
            for ai in ch.accordion_items:
                active_class = " active" if ai.active else ""
                parts.append(f'''<div class="accordion-item{active_class}">
<div class="accordion-header" onclick="toggleAccordion(this)">
<span>{ai.title}</span>
<span class="arrow">▼</span>
</div>
<div class="accordion-body">
<div class="accordion-content">{ai.content}</div>
</div>
</div>''')
            parts.append('</div>')

        # Callouts
        for cl in ch.callouts:
            style_class = f" {cl.style}" if cl.style != "info" else ""
            parts.append(f'''<div class="callout{style_class} fade-in">
<div class="callout-title">{cl.title}</div>
{cl.content}
</div>''')

        parts.append('</section>')
        return '\n'.join(parts)

    # ===== Chart =====
    def _build_chart(self, chart) -> str:
        """构建图表容器（HTML部分）"""
        chart_id = chart.chart_id if hasattr(chart, 'chart_id') else chart.get('chart_id', '')
        title = chart.title if hasattr(chart, 'title') else chart.get('title', '')
        note = chart.note if hasattr(chart, 'note') else chart.get('note', '')

        # Store chart data as JSON for JS to pick up
        chart_data = chart.to_dict() if hasattr(chart, 'to_dict') else chart
        chart_json = json.dumps(chart_data, ensure_ascii=False)

        return f'''<div class="chart-container fade-in">
<div class="chart-title">{title}</div>
<div class="chart-note">{note}</div>
<div class="chart-canvas-wrap">
<canvas id="chart-{chart_id}"></canvas>
</div>
<script class="chart-data" type="application/json" data-chart-id="{chart_id}">
{chart_json}
</script>
</div>'''

    # ===== Table =====
    def _build_table(self, table: dict) -> str:
        headers = table.get("headers", [])
        rows = table.get("rows", [])
        html = '<div class="table-wrap fade-in"><table><tr>'
        for h in headers:
            html += f'<th>{h}</th>'
        html += '</tr>'
        for row in rows:
            html += '<tr>'
            for cell in row:
                html += f'<td>{cell}</td>'
            html += '</tr>'
        html += '</table></div>'
        return html

    # ===== References =====
    def _build_references(self) -> str:
        if not self.config.references:
            return ''
        items_html = ""
        for ref in self.config.references:
            link = f'<a href="{ref.url}" target="_blank">{ref.url}</a>' if ref.url else ''
            items_html += f'<li>{ref.title} {link}</li>\n'
        return f'''<section class="section">
<div class="section-header fade-in">
<div class="section-num">参考资料</div>
<h2 class="section-title">参考文献</h2>
</div>
<div class="references fade-in">
<h3>信源列表</h3>
<ol class="ref-list">
{items_html}
</ol>
</div>
</section>'''

    # ===== Footer =====
    def _build_footer(self) -> str:
        footer = self.config.footer_text or f"{self.config.game_name} · {self.config.subtitle}"
        return f'''<footer class="footer">
<p>{footer}</p>
<p>本报告基于公开信息和社区抽样分析，数据仅供参考，实际数据以官方披露为准</p>
</footer>'''

    # ===== JavaScript =====
    def _build_scripts(self) -> str:
        return '''<script>
// Progress Bar
window.addEventListener('scroll', function() {
  var h = document.documentElement;
  var scrolled = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
  document.getElementById('progress-bar').style.width = scrolled + '%';
});

// Navigation Active State
var sections = document.querySelectorAll('.section[id]');
var navLinks = document.querySelectorAll('.nav-links a');
window.addEventListener('scroll', function() {
  var current = '';
  sections.forEach(function(sec) {
    var top = sec.offsetTop - 80;
    if (window.scrollY >= top) current = sec.id;
  });
  navLinks.forEach(function(link) {
    link.classList.toggle('active', link.getAttribute('href') === '#' + current);
  });
});

// Fade-in Animation
var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-in').forEach(function(el) { observer.observe(el); });

// Accordion
function toggleAccordion(header) {
  header.parentElement.classList.toggle('active');
}

// Chart.js Defaults
Chart.defaults.font.family = "'Microsoft YaHei', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#4a4a4a';
Chart.defaults.borderColor = '#e4e7ec';

// Auto-render all charts from script tags
document.querySelectorAll('script.chart-data').forEach(function(scriptTag) {
  var chartId = scriptTag.getAttribute('data-chart-id');
  var config = JSON.parse(scriptTag.textContent);
  var canvas = document.getElementById('chart-' + chartId);
  if (!canvas || !config) return;

  var chartType = config.chart_type;
  var labels = config.labels;
  var datasets = config.datasets;
  var options = config.options || {};

  // Apply defaults
  if (!options.responsive) options.responsive = true;
  if (options.maintainAspectRatio === undefined) options.maintainAspectRatio = false;

  if (!options.plugins) options.plugins = {};
  if (!options.plugins.legend) options.plugins.legend = { display: true, position: 'top' };

  // Process datasets for color gradients
  datasets.forEach(function(ds) {
    if (!ds.borderColor) ds.borderColor = '#4A90D9';
    if (ds.fill === true && !ds.backgroundColor) {
      ds.backgroundColor = 'rgba(74,144,217,0.15)';
    }
    if (!ds.borderWidth) ds.borderWidth = 2;
    if (ds.tension === undefined) ds.tension = 0.4;
  });

  new Chart(canvas.getContext('2d'), {
    type: chartType,
    data: { labels: labels, datasets: datasets },
    options: options
  });
});
</script>'''
