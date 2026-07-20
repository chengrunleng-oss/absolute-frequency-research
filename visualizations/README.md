# 不确定度可视化产物

本目录整理自原工作目录：

`C:\Users\GS\Desktop\absolute-frequency-research\visualizations`

迁移采用复制方式，原目录未删除。

## 目录结构

```text
visualizations/
├── README.md
├── requirements.txt
├── src/
│   └── generate_uncertainty_charts.py
├── web/
│   ├── uncertainty-comparison.html
│   ├── uncertainty-comparison-interactive.html
│   └── uncertainty-comparison-interactive.fragment.html
└── exports/
    ├── 01_old_uncertainty_pie.png
    ├── 02_new_uncertainty_pie.png
    ├── 03_metric_comparison.png
    ├── 04_variance_share.png
    ├── 05_variance_waterfall.png
    ├── 06_uptime_vs_hm.png
    ├── 07_formula_and_full_budget.png
    ├── uncertainty_comparison_all.png
    └── uncertainty_budget_data.csv
```

## 入口文件

- 静态总览：[`web/uncertainty-comparison.html`](web/uncertainty-comparison.html)
- 交互版本：[`web/uncertainty-comparison-interactive.html`](web/uncertainty-comparison-interactive.html)
- 总览大图：[`exports/uncertainty_comparison_all.png`](exports/uncertainty_comparison_all.png)
- 完整数据：[`exports/uncertainty_budget_data.csv`](exports/uncertainty_budget_data.csv)

## 重新生成图表

在项目根目录执行：

```powershell
python -m pip install -r visualizations/requirements.txt
python visualizations/src/generate_uncertainty_charts.py
```

脚本会将全部 PNG 和 CSV 重新写入 `visualizations/exports/`。

## 产物说明

| 文件 | 内容 |
| --- | --- |
| `01_old_uncertainty_pie.png` | 2025 年论文各项不确定度方差占比 |
| `02_new_uncertainty_pie.png` | 2026 年论文各项不确定度方差占比 |
| `03_metric_comparison.png` | 两篇论文关键不确定度指标对比 |
| `04_variance_share.png` | 功能组总方差占比变化 |
| `05_variance_waterfall.png` | 总方差降低来源 |
| `06_uptime_vs_hm.png` | 光钟 uptime 与 HM 插值/外推不确定度关系 |
| `07_formula_and_full_budget.png` | 合成公式与完整预算分量 |
| `uncertainty_comparison_all.png` | 所有静态图表的总览拼图 |
| `uncertainty_budget_data.csv` | 绘图使用的完整预算数据 |

交互页面依赖外部 Chart.js CDN，离线环境下静态页面和 PNG/CSV 仍可正常使用。
