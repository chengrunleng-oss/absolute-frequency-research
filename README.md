# Absolute Frequency Research

本仓库整理 `176Lu+` 光频标绝对频率测量论文、中文解读、复现资料、内容汇报和不确定度可视化产物。

## 文档目录

| 文件 | 用途 |
| --- | --- |
| [`Lu光频标绝对频率测量_内容汇报.md`](Lu光频标绝对频率测量_内容汇报.md) | 简要中文内容汇报，按逻辑介绍论文 Figure 1-6 |
| [`Lu光频标绝对频率测量_内容汇报.docx`](Lu光频标绝对频率测量_内容汇报.docx) | 可直接阅读和汇报的 Word 版本 |
| [`lu3d1_absolute_frequency_explained.md`](lu3d1_absolute_frequency_explained.md) | 面向初学者的完整论文解读 |
| [`reproduction_guide.md`](reproduction_guide.md) | 数据需求、计算流程和复现边界 |
| [`lu3d1_absolute_frequency_feedback.md`](lu3d1_absolute_frequency_feedback.md) | 解读文档的审核反馈记录 |

## 原始论文

| 文件 | 内容 |
| --- | --- |
| [`2502.10004v3.pdf`](2502.10004v3.pdf) | Lu+ (3D1) 光频标经 TAI 链路的绝对频率测量 |
| [`2607.07044v1.pdf`](2607.07044v1.pdf) | 后续分析论文 |

## 图片与可视化

- `assets/paper_figures/`：从原论文提取的 Figure 1-6。
- [`visualizations/README.md`](visualizations/README.md)：不确定度对比图、交互页面、CSV 数据和生成方法。
- [`visualizations/web/uncertainty-comparison.html`](visualizations/web/uncertainty-comparison.html)：静态可视化入口。
- [`visualizations/web/uncertainty-comparison-interactive.html`](visualizations/web/uncertainty-comparison-interactive.html)：交互可视化入口。

## 生成脚本

- `build_paper_report.py`：重新生成 Word 内容汇报。
- `visualizations/src/generate_uncertainty_charts.py`：重新生成不确定度图表和 CSV。

临时渲染文件和重复输出位于 `tmp/`、`output/`，不会纳入版本控制。
