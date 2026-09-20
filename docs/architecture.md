# 架构说明

## 整体架构

```
┌─────────────────────────────────────────────────────┐
│                   GameOpsAgent                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Config    │→│ Generator │→│  HTML Output       │   │
│  │ (Data)    │  │ (Engine)  │  │  (Self-contained) │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
│       ↑                                              │
│  ┌──────────┐                                       │
│  │ User API  │  (链式调用 / JSON配置)                │
│  └──────────┘                                       │
└─────────────────────────────────────────────────────┘
```

## 模块职责

### 1. config.py - 配置层
- 定义所有数据结构（dataclass）
- `ReportConfig`：报告总配置
- `ChapterConfig`：章节配置
- `ChartConfig`：图表配置
- 组件级配置：`StatCard`, `PricingCard`, `DataCard`, `TimelineItem`, `AccordionItem`, `CalloutItem`
- 提供 `from_dict()` 方法支持从JSON/YAML加载

### 2. agent.py - 编排层
- `GameOpsAgent`：主Agent类
- 提供链式API和配置加载两种使用方式
- 图片自动转base64
- 配置导出功能

### 3. generator.py - 渲染层
- `ReportGenerator`：HTML报告生成器
- CSS生成（基于主题配置变量）
- HTML结构构建（导航→Hero→章节→参考→页脚）
- JavaScript生成（进度条、导航高亮、fade-in动画、手风琴、Chart.js自动渲染）
- Chart.js图表通过 `<script type="application/json">` 标签传递数据，JS自动解析渲染

## 数据流

```
用户输入
  │
  ├── JSON/YAML配置文件 ──→ load_config() ──→ ReportConfig
  │                                              │
  └── 链式API调用 ──────────→ GameOpsAgent ──────┤
                                                  │
                                          ReportGenerator
                                                  │
                                          HTML字符串
                                                  │
                                          写入文件
                                                  │
                                          report.html (自包含)
```

## 设计原则

1. **配置驱动**：报告内容完全由配置决定，代码不包含硬编码内容
2. **自包含输出**：生成的HTML文件无需任何外部依赖（Chart.js通过CDN加载）
3. **组件化**：每个UI组件（数据卡片、定价卡片、时间线等）独立渲染
4. **主题可定制**：通过CSS变量实现配色，一处修改全局生效
5. **渐进式使用**：支持从简单到复杂的各种使用方式
