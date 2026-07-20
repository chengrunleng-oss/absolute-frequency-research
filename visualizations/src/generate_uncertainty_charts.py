# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "exports"
OUTPUT.mkdir(parents=True, exist_ok=True)

FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")
if FONT_PATH.exists():
    fm.fontManager.addfont(FONT_PATH)
    FONT_NAME = fm.FontProperties(fname=FONT_PATH).get_name()
else:
    FONT_NAME = "DejaVu Sans"

plt.rcParams.update(
    {
        "font.family": FONT_NAME,
        "axes.unicode_minus": False,
        "axes.titleweight": "normal",
        "axes.titlesize": 15,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9,
    }
)

BG = "#FFFFFF"
TEXT = "#20262D"
MUTED = "#5F6B76"
GRID = "#D9DEE5"
OLD_COLOR = "#687481"
NEW_COLOR = "#25739A"
REDUCTION = "#3F8C62"
INCREASE = "#B65A64"
GROUP_COLORS = {
    "Lu 本地": "#2D6A8A",
    "HM flywheel": "#C47B28",
    "远程链路": "#4E8B57",
    "SI 参考": "#A84E62",
}
GROUP_ORDER = list(GROUP_COLORS)
HATCHES = ["", "///", "\\\\", "xx", "..", "++", "oo"]


OLD_ITEMS = [
    {"label": "Lu 统计（加权后）", "u": 0.124, "group": "Lu 本地"},
    {"label": "HM interpolation（加权后）", "u": 4.391, "group": "HM flywheel"},
    {"label": "HM / UTC(USNO)", "u": 5.292, "group": "远程链路"},
    {"label": "UTC(USNO) / TAI", "u": 2.328, "group": "远程链路"},
    {"label": "TAI interpolation", "u": 1.50, "group": "远程链路"},
    {"label": "TAI / SI 统计", "u": 0.40, "group": "远程链路"},
    {"label": "HM drift", "u": 2.00, "group": "HM flywheel"},
    {"label": "HM diurnal", "u": 5.00, "group": "HM flywheel"},
    {"label": "Lu 系统", "u": 0.10, "group": "Lu 本地"},
    {"label": "重力红移", "u": 0.40, "group": "Lu 本地"},
    {"label": "PSFS 系统", "u": 0.90, "group": "SI 参考"},
]

NEW_ITEMS = [
    {"label": "Lu 统计", "u": 0.04, "group": "Lu 本地"},
    {"label": "HM extrapolation", "u": 0.74, "group": "HM flywheel"},
    {"label": "HM drift", "u": 0.01, "group": "HM flywheel"},
    {"label": "PPP-AR 链路", "u": 1.00, "group": "远程链路"},
    {"label": "NRC RF 分配", "u": 0.60, "group": "远程链路"},
    {"label": "NRC-FCs2 统计", "u": 1.78, "group": "SI 参考"},
    {"label": "Lu 系统＋重力红移", "u": 0.36, "group": "Lu 本地"},
    {"label": "NRC-FCs2 系统", "u": 1.17, "group": "SI 参考"},
]

OLD_WINDOWS = np.array(
    [
        [11, 15],
        [2, 29],
        [7, 16],
        [37, 6.8],
        [14, 14],
        [9, 18],
        [3, 24],
        [30, 7.6],
        [20, 8.8],
    ],
    dtype=float,
)


def variance_total(items: list[dict]) -> float:
    return sum(item["u"] ** 2 for item in items)


def group_variances(items: list[dict]) -> dict[str, float]:
    result = defaultdict(float)
    for item in items:
        result[item["group"]] += item["u"] ** 2
    return dict(result)


def style_axes(ax, grid_axis: str = "y") -> None:
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def save_figure(fig, filename: str) -> Path:
    path = OUTPUT / filename
    fig.savefig(path, dpi=210, bbox_inches="tight", pad_inches=0.22, facecolor=BG)
    plt.close(fig)
    return path


def draw_donut(items: list[dict], title: str, published_total: float, filename: str) -> Path:
    total = variance_total(items)
    values = [item["u"] ** 2 for item in items]
    colors = [GROUP_COLORS[item["group"]] for item in items]
    group_counts = defaultdict(int)
    hatches = []
    for item in items:
        hatches.append(HATCHES[group_counts[item["group"]] % len(HATCHES)])
        group_counts[item["group"]] += 1

    fig, ax = plt.subplots(figsize=(13.2, 7.6), facecolor=BG)
    wedges, _ = ax.pie(
        values,
        startangle=90,
        counterclock=False,
        colors=colors,
        wedgeprops={"width": 0.42, "edgecolor": BG, "linewidth": 1.5},
    )
    for wedge, hatch in zip(wedges, hatches):
        wedge.set_hatch(hatch)
    ax.text(0, 0.08, f"{published_total:.2f}", ha="center", va="center", fontsize=26, color=TEXT)
    ax.text(0, -0.11, "×10$^{-16}$", ha="center", va="center", fontsize=12, color=MUTED)
    ax.set_title(title, pad=18, color=TEXT)

    labels = [
        f"{item['label']}   u={item['u']:.3g}   u²占比={100 * item['u'] ** 2 / total:.1f}%"
        for item in items
    ]
    ax.legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
        labelcolor=TEXT,
        handlelength=2.4,
    )
    ax.text(
        0,
        -1.22,
        "饼图面积按方差 u² 分配；不确定度不能直接按 u 相加。",
        ha="center",
        va="center",
        fontsize=10,
        color=MUTED,
    )
    ax.set_aspect("equal")
    return save_figure(fig, filename)


def draw_metric_comparison() -> Path:
    labels = [
        "总不确定度",
        "统计不确定度",
        "系统不确定度",
        "HM 插值 / 外推",
        "远程时间链路",
        "HM drift",
        "HM diurnal",
        "Lu 本地系统",
        "SI 参考系统",
    ]
    old = np.array([9.22, 7.40, 5.50, 4.39, 5.99, 2.00, 5.00, 0.43, 0.90])
    new = np.array([2.57, 2.26, 1.22, 0.74, 1.17, 0.01, 0.00, 0.36, 1.17])
    y = np.arange(len(labels))
    height = 0.34

    fig, ax = plt.subplots(figsize=(12.8, 7.8), facecolor=BG)
    ax.barh(y + height / 2, old, height, color=OLD_COLOR, label="前篇：TAI 链路")
    ax.barh(y - height / 2, new, height, color=NEW_COLOR, label="后篇：PPP-AR 直比")
    for index, value in enumerate(old):
        ax.text(value + 0.10, index + height / 2, f"{value:.2f}", va="center", color=TEXT, fontsize=9)
    for index, value in enumerate(new):
        ax.text(value + 0.10, index - height / 2, f"{value:.2f}", va="center", color=TEXT, fontsize=9)

    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 10.2)
    ax.set_xlabel("不确定度 u（×10$^{-16}$）")
    ax.set_title("两篇论文关键不确定度指标同尺度比较")
    ax.legend(loc="lower right", frameon=False, labelcolor=TEXT)
    style_axes(ax, "x")
    ax.text(
        0,
        -0.13,
        "远程时间链路：前篇合并 HM/UTC、UTC/TAI、TAI interpolation 与 TAI/SI 统计；后篇合并 PPP-AR 与 RF 分配。",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=9,
    )
    return save_figure(fig, "03_metric_comparison.png")


def draw_variance_share() -> Path:
    old_groups = group_variances(OLD_ITEMS)
    new_groups = group_variances(NEW_ITEMS)
    totals = [sum(old_groups.values()), sum(new_groups.values())]

    fig, ax = plt.subplots(figsize=(11.5, 5.4), facecolor=BG)
    left = np.zeros(2)
    for group in GROUP_ORDER:
        values = np.array(
            [
                100 * old_groups[group] / totals[0],
                100 * new_groups[group] / totals[1],
            ]
        )
        bars = ax.barh([0, 1], values, left=left, color=GROUP_COLORS[group], height=0.52, label=group)
        for row, (bar, value) in enumerate(zip(bars, values)):
            if value >= 5:
                ax.text(
                    left[row] + value / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    color=BG,
                    fontsize=10,
                )
        left += values

    ax.set_yticks([0, 1], ["前篇", "后篇"])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("总方差占比（%）")
    ax.set_title("总方差主导项从 HM/长链路转移到 NRC-FCs2")
    ax.legend(ncols=4, loc="lower center", bbox_to_anchor=(0.5, -0.32), frameon=False, labelcolor=TEXT)
    style_axes(ax, "x")
    ax.text(
        0.5,
        -0.18,
        "后篇 NRC-FCs2 的统计＋系统方差占总方差约 69.0%",
        transform=ax.transAxes,
        ha="center",
        color=MUTED,
        fontsize=10,
    )
    return save_figure(fig, "04_variance_share.png")


def draw_variance_waterfall() -> Path:
    old_groups = group_variances(OLD_ITEMS)
    new_groups = group_variances(NEW_ITEMS)
    old_total = sum(old_groups.values())
    changes = [
        new_groups["HM flywheel"] - old_groups["HM flywheel"],
        new_groups["远程链路"] - old_groups["远程链路"],
        new_groups["Lu 本地"] - old_groups["Lu 本地"],
        new_groups["SI 参考"] - old_groups["SI 参考"],
    ]
    labels = ["前篇总方差", "HM flywheel", "远程链路", "Lu 本地", "SI 参考变化", "后篇总方差"]
    cumulative = [old_total]
    for change in changes:
        cumulative.append(cumulative[-1] + change)
    final_total = cumulative[-1]

    fig, ax = plt.subplots(figsize=(12.8, 6.4), facecolor=BG)
    ax.bar(0, old_total, color=OLD_COLOR, width=0.68)
    for index, change in enumerate(changes, start=1):
        previous = cumulative[index - 1]
        current = cumulative[index]
        bottom = min(previous, current)
        ax.bar(index, abs(change), bottom=bottom, color=REDUCTION if change < 0 else INCREASE, width=0.68)
        ax.plot([index - 0.66, index - 0.34], [previous, previous], color=MUTED, linewidth=1)
        ax.text(
            index,
            max(previous, current) + 2.2,
            f"{change:+.2f}",
            ha="center",
            va="bottom",
            color=TEXT,
            fontsize=10,
        )
    ax.plot([4.34, 4.66], [final_total, final_total], color=MUTED, linewidth=1)
    ax.bar(5, final_total, color=NEW_COLOR, width=0.68)
    ax.text(0, old_total + 2.2, f"{old_total:.2f}", ha="center", color=TEXT, fontsize=10)
    ax.text(5, final_total + 2.2, f"{final_total:.2f}", ha="center", color=TEXT, fontsize=10)

    ax.set_xticks(range(len(labels)), labels)
    ax.set_ylabel("方差 u²［(10$^{-16}$)²］")
    ax.set_title("方差瀑布图：为什么总不确定度能下降 3.58 倍")
    ax.set_ylim(0, 95)
    style_axes(ax, "y")
    handles = [
        Patch(facecolor=OLD_COLOR, label="起点"),
        Patch(facecolor=REDUCTION, label="方差减少"),
        Patch(facecolor=INCREASE, label="方差增加"),
        Patch(facecolor=NEW_COLOR, label="终点"),
    ]
    ax.legend(handles=handles, ncols=4, loc="upper right", frameon=False, labelcolor=TEXT)
    ax.text(
        0.5,
        -0.15,
        "HM 与远程链路共减少 82.21；参考钟项增加 3.73，因此净方差由 85.11 降至 6.58（−92.3%）。",
        transform=ax.transAxes,
        ha="center",
        color=MUTED,
        fontsize=10,
    )
    return save_figure(fig, "05_variance_waterfall.png")


def draw_uptime_scatter() -> Path:
    fig, ax = plt.subplots(figsize=(10.8, 6.7), facecolor=BG)
    ax.scatter(
        OLD_WINDOWS[:, 0],
        OLD_WINDOWS[:, 1],
        s=62,
        color=OLD_COLOR,
        marker="o",
        label="前篇：9 个五日窗口",
        zorder=3,
    )
    for index, (uptime, uncertainty) in enumerate(OLD_WINDOWS, start=1):
        ax.annotate(f"W{index}", (uptime, uncertainty), xytext=(5, 5), textcoords="offset points", color=MUTED, fontsize=8)
    ax.scatter([94.2], [0.74], s=130, color=NEW_COLOR, marker="D", label="后篇：十日连续测量", zorder=4)
    ax.annotate(
        "94.2%, 0.74",
        (94.2, 0.74),
        xytext=(-92, 28),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": NEW_COLOR, "linewidth": 1.2},
        color=TEXT,
        fontsize=10,
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 32)
    ax.set_xlabel("Lu 光钟运行占空比（%）")
    ax.set_ylabel("HM 插值 / 外推不确定度（×10$^{-16}$）")
    ax.set_title("高占空比直接压低 HM interpolation / extrapolation")
    ax.legend(loc="upper right", frameon=False, labelcolor=TEXT)
    style_axes(ax, "both")
    return save_figure(fig, "06_uptime_vs_hm.png")


def formula_block(ax, title: str, lines: list[tuple[str, str]]) -> None:
    ax.axis("off")
    ax.set_title(title, loc="left", pad=10, color=TEXT)
    y = 0.94
    for label, formula in lines:
        ax.text(0.01, y, label, transform=ax.transAxes, color=MUTED, fontsize=10, va="top")
        ax.text(0.28, y, formula, transform=ax.transAxes, color=TEXT, fontsize=10, va="top")
        y -= 0.14


def data_table(ax, items: list[dict], title: str) -> None:
    total = variance_total(items)
    rows = [
        [item["label"], item["group"], f"{item['u']:.3g}", f"{100 * item['u'] ** 2 / total:.1f}%"]
        for item in items
    ]
    ax.axis("off")
    ax.set_title(title, loc="left", pad=10, color=TEXT)
    table = ax.table(
        cellText=rows,
        colLabels=["分量", "功能组", "u (×10^-16)", "u²占比"],
        colWidths=[0.39, 0.22, 0.19, 0.16],
        cellLoc="left",
        colLoc="left",
        loc="upper left",
        bbox=[0, 0.02, 1, 0.94],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.7)
    for (row, _column), cell in table.get_celld().items():
        cell.set_edgecolor(GRID)
        cell.set_linewidth(0.6)
        cell.set_text_props(color=TEXT, fontfamily=FONT_NAME)
        cell.set_facecolor("#F3F5F7" if row == 0 else BG)


def draw_formula_budget() -> Path:
    old_formula = [
        ("九次权重", "a_j = (1/u_j²) / Σ_i(1/u_i²)"),
        ("分量有效值", "u_k,eff = √[Σ_j(a_j u_k,j)²]"),
        ("Lu / TAI", "√(0.124²+4.391²+5.292²+2.328²) = 7.253"),
        ("统计合成", "u_A = √(7.253²+1.5²+0.4²) = 7.42 ≈ 7.4"),
        ("系统合成", "u_B = √(2.0²+5.0²+0.1²+0.4²+0.9²) = 5.48 ≈ 5.5"),
        ("最终", "u_old = √(7.4²+5.5²) = 9.22 ≈ 9.2"),
    ]
    new_formula = [
        ("统计合成", "u_A = √(0.04²+0.74²+0.01²+1.00²+0.60²+1.78²)"),
        ("舍入分量", "√5.0777 = 2.253；论文用未舍入数据报告 2.26"),
        ("系统合成", "u_B = √(0.36²+1.17²) = 1.224 ≈ 1.22"),
        ("最终", "u_new = √(2.26²+1.22²) = 2.57 ≈ 2.6"),
        ("改善倍数", "u_old/u_new = 9.2/2.57 = 3.58"),
        ("方差降幅", "1−(2.57/9.2)² = 92.3%"),
    ]

    fig = plt.figure(figsize=(17.0, 13.2), facecolor=BG)
    grid = fig.add_gridspec(2, 2, height_ratios=[0.42, 0.58], hspace=0.18, wspace=0.10)
    formula_block(fig.add_subplot(grid[0, 0]), "前篇：合成公式", old_formula)
    formula_block(fig.add_subplot(grid[0, 1]), "后篇：合成公式", new_formula)
    data_table(fig.add_subplot(grid[1, 0]), OLD_ITEMS, "前篇：完整预算数据")
    data_table(fig.add_subplot(grid[1, 1]), NEW_ITEMS, "后篇：完整预算数据")
    fig.suptitle("不确定度计算公式与完整数据（统一单位：10$^{-16}$）", fontsize=18, color=TEXT, y=0.995)
    fig.text(
        0.5,
        0.008,
        "前篇数据：2502.10004v3 Table 2–3；后篇数据：2607.07044v1 Table 4。所有独立分量按方差相加。",
        ha="center",
        color=MUTED,
        fontsize=10,
    )
    return save_figure(fig, "07_formula_and_full_budget.png")


def write_data_csv() -> Path:
    path = OUTPUT / "uncertainty_budget_data.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["paper", "component", "functional_group", "u_x_1e-16", "variance", "variance_share_percent"])
        for paper, items in [("2025_old", OLD_ITEMS), ("2026_new", NEW_ITEMS)]:
            total = variance_total(items)
            for item in items:
                writer.writerow(
                    [
                        paper,
                        item["label"],
                        item["group"],
                        f"{item['u']:.6g}",
                        f"{item['u'] ** 2:.8g}",
                        f"{100 * item['u'] ** 2 / total:.6f}",
                    ]
                )
    return path


def make_contact_sheet(paths: list[Path]) -> Path:
    width = 3000
    gap = 42
    margin = 52
    col_width = (width - 2 * margin - gap) // 2
    row_heights = [930, 930, 930, 1700]
    height = 2 * margin + sum(row_heights) + gap * (len(row_heights) - 1)
    sheet = Image.new("RGB", (width, height), BG)

    placements = [
        (paths[0], margin, margin, col_width, row_heights[0]),
        (paths[1], margin + col_width + gap, margin, col_width, row_heights[0]),
        (paths[2], margin, margin + row_heights[0] + gap, width - 2 * margin, row_heights[1]),
        (paths[3], margin, margin + row_heights[0] + row_heights[1] + 2 * gap, col_width, row_heights[2]),
        (paths[4], margin + col_width + gap, margin + row_heights[0] + row_heights[1] + 2 * gap, col_width, row_heights[2]),
        (paths[5], margin, margin + sum(row_heights[:3]) + 3 * gap, col_width, row_heights[3]),
        (paths[6], margin + col_width + gap, margin + sum(row_heights[:3]) + 3 * gap, col_width, row_heights[3]),
    ]
    for path, x, y, target_width, target_height in placements:
        with Image.open(path).convert("RGB") as image:
            fitted = ImageOps.contain(image, (target_width, target_height), method=Image.Resampling.LANCZOS)
            paste_x = x + (target_width - fitted.width) // 2
            paste_y = y + (target_height - fitted.height) // 2
            sheet.paste(fitted, (paste_x, paste_y))

    output = OUTPUT / "uncertainty_comparison_all.png"
    sheet.save(output, quality=94, optimize=True)
    return output


def main() -> None:
    paths = [
        draw_donut(OLD_ITEMS, "前篇（2025）：各项方差占比", 9.22, "01_old_uncertainty_pie.png"),
        draw_donut(NEW_ITEMS, "后篇（2026）：各项方差占比", 2.57, "02_new_uncertainty_pie.png"),
        draw_metric_comparison(),
        draw_variance_share(),
        draw_variance_waterfall(),
        draw_uptime_scatter(),
        draw_formula_budget(),
    ]
    write_data_csv()
    make_contact_sheet(paths)
    print(f"Generated {len(paths) + 2} files in {OUTPUT}")


if __name__ == "__main__":
    main()
