# `176Lu+ (3D1)` 绝对频率测量复现手册

本手册补充 `lu3d1_absolute_frequency_explained.md`。前者偏概念导读，本文件偏复现视角：哪些能复现、需要哪些数据、按什么顺序算、哪些地方会卡住。

复现对象是论文：

- `Absolute frequency measurement of a Lu+ (3D1) optical frequency standard via link to international atomic time`
- arXiv:2502.10004v3
- 本地 PDF：`2502.10004v3.pdf`

## 0. 一页路线图

如果你只想读懂论文主线：读 `lu3d1_absolute_frequency_explained.md` 第 1-16 节即可。

如果你想动手复算：先做本手册第 3 节的 L1 表格复算任务。它不需要作者原始数据，能马上验证你是否理解单位、平方和合成和表格检查点。

如果你想处理公开数据：进入 L2，下载 Circular T、USN7 RINEX 和 GNSS 精密产品；但由于缺少作者本地 RINEX 和 Lu/HM 数据，公开数据不能闭合全链路。

如果你想完整复现中心值：必须向作者请求本地 Lu/HM 时间序列、本地 RINEX、uptime mask、系统误差记录和分析配置。

如果你想实验复现：需要完整单离子光钟实验平台，包括离子阱、激光系统、光频梳、氢钟和 GNSS/PPP 时间传递链路。

## 1. 复现目标和边界

“复现这篇论文”不是一个单一任务。至少要分成下面几层：

| 层级 | 目标 | 需要什么 | 能得到什么 | 不能得到什么 |
| --- | --- | --- | --- | --- |
| L0 概念复现 | 读懂实验链路和误差来源 | 论文 PDF、解读文档 | 理解 `Lu+ -> HM -> UTC(USNO) -> TAI -> SI` | 不能独立算出最终频率 |
| L1 表格复算 | 复算论文公开表格中的合成项 | 论文表 1、表 2、表 3 数值 | 复算系统频移合计、统计/系统不确定度平方和 | 不能验证原始数据处理 |
| L2 公开链路复现 | 处理公开的 Circular T、USN7 RINEX 等 | BIPM、CDDIS 数据和 GNSS 工具 | 可复现部分 UTC(USNO)-TAI、TAI-SI 链路 | 缺本地 RINEX 和 Lu/HM 数据，不能闭合全链路 |
| L3 数据分析复现 | 用作者原始数据重做论文数值分析 | 作者 Lu/HM 日志、本地 RINEX、uptime 时间戳、系统误差记录 | 有机会复算图 4、表 2、表 3 和最终频率 | 数据未随论文公开，需要向作者请求 |
| L4 实验复现 | 从硬件开始复现实验 | 单离子光钟、激光、Paul 阱、光频梳、氢钟、GNSS/PPP | 独立测量 `Lu+ (3D1)` 绝对频率 | 成本和门槛极高，不是文档即可完成 |

论文的数据可用性说明是：USN7 的 RINEX 文件来自 CDDIS 公开档案；支撑研究发现的数据可向通讯作者合理请求。因此，没有作者的本地实验数据时，不能独立复算完整最终值 `353 638 794 073 800.35(33) Hz`，只能复现方法、公开链路处理和表格合成。

## 2. 数据清单

| 数据 | 用途 | 来源 | 是否公开 | 时间范围 | 格式 | 对应计算 |
| --- | --- | --- | --- | --- | --- | --- |
| Lu/HM 测量数据 | 得到 `f_Lu/f_HM` | 作者实验日志 | 未公开，需请求 | MJD 59270-59338 附近 | 论文未说明；图 4 提到 20 s 记录 | 频率链第 1 项、图 4 蓝点 |
| Lu+ uptime 时间戳 | 判断每个 5 天窗口内光钟何时开机 | 作者实验日志 | 未公开，需请求 | 论文表 2 的 9 个窗口 | 时间戳或 mask | HM 死时间插值 |
| SDR 相位数据 | 从 20 MHz 下变频信号得到频率差 | 作者实验系统 | 未公开，需请求 | 光钟 uptime 内 | 论文未说明 | `f_Lu/f_HM` |
| 光频梳锁定参数 | 确定 comb tooth、beat、DDS offset 正负号 | 作者实验配置 | 未公开，需请求 | 光钟 uptime 内 | 配置表/日志 | 光频到 HM 的转换 |
| 本地 RINEX | 本地 HM 到 GNSS 时间传递 | 作者 PolaRx5TR 接收机 | 未公开，需请求 | 约 80 天，覆盖测量期 | RINEX | PPP 得到 HM-UTC(USNO) |
| USN7 RINEX | 远端 UTC(USNO) 参考 | CDDIS | 公开，通常需要 NASA Earthdata 账号 | 同上 | RINEX | PPP 得到 HM-UTC(USNO) |
| GNSS 精密产品 | PPP 必需的星历、钟差等 | IGS/CDDIS 等 | 公开 | 同上 | SP3、CLK 等 | PPP |
| Circular T 399-401 | UTC(USNO)-TAI、TAI-SI | BIPM | 公开 | 2021-03 到 2021-05 | 文本/PDF | TAI/SI 链接、表 3 |
| EAL/TAI 稳定度模型 | TAI 插值模拟 | BIPM 相关产品；论文给出模型参数 | 部分公开 | Circular T 399-401 | 报告/文本 | TAI dead time |
| 磁场测量 | 二阶塞曼修正 | 作者实验记录 | 未公开，论文给均值 | 全 campaign | 日志 | 表 1 |
| 高度测量和地球模型 | 引力红移 | 作者测量、WGS84、EGM2008 | 部分公开 | 固定位置 | 高程数据 | 表 1 |
| 微运动、微波极化、ac-Stark、BBR 记录 | 其他系统频移 | 作者实验记录和参考文献 [8] | 多数未公开 | campaign 内 | 实验日志 | 表 1 |

最小可行复现建议：先做 L1，也就是用论文表格数值复算不确定度合成；再根据可获取数据尝试 L2。

## 3. 最小复算任务

这一节是最推荐的小白起点。它只复算论文表格已经给出的合成结果，不需要作者未公开的原始数据。

### 任务 1：复算表 1 系统频移合计

输入：表 1 中 Lu+ 本体系统项的 shift 和 uncertainty。

目标输出：

```text
Lu+ systematics subtotal = -150.4(7.3)e-18
total with redshift     = +1568(37)e-18
```

计算方式：

- shift 直接相加。
- uncertainty 先假设相互独立，按平方和开根号。
- 引力红移 `1718(36)e-18` 加到 Lu+ 本体 subtotal 上。

### 任务 2：复算表 2 每个 5 天窗口总统计不确定度

输入：表 2 四行 uncertainty：

- `Lu clock`
- `HM interpolation`
- `HM/UTC(USNO)`
- `UTC(USNO)/TAI`

目标输出：

```text
22, 33, 23, 18, 21, 24, 29, 18, 19 e-16
```

计算方式：每个 5 天窗口内，四个 uncertainty 按平方和开根号。

### 任务 3：复算表 3 最后一列

输入：

```text
statistical: 7.3, 1.5, 0.4
systematic:  2.0, 5.0, 0.1, 0.4, 0.9
```

目标输出：

```text
total statistical = 7.4e-16
total systematic  = 5.5e-16
total uncertainty = 9.2e-16
```

可直接运行的 Python 示例：

```python
from math import sqrt

def rss(values):
    return sqrt(sum(v * v for v in values))

# Task 1: Table 1
lu_shifts = [-140.7, -0.2, -0.1, 0.2, -8.0, 0.0, 0.0, -1.6]
lu_unc = [0.6, 0.2, 0.1, 0.1, 6.2, 3.7, 1.2, 0.3]
subtotal_shift = sum(lu_shifts)
subtotal_unc = rss(lu_unc)
total_shift = subtotal_shift + 1718
total_unc = rss([subtotal_unc, 36])
print(round(subtotal_shift, 1), round(subtotal_unc, 1))
print(round(total_shift), round(total_unc))

# Task 2: Table 2
lu_clock = [0.4, 0.8, 0.5, 0.2, 0.4, 0.4, 0.7, 0.2, 0.3]
hm_interp = [15, 29, 16, 6.8, 14, 18, 24, 7.6, 8.8]
hm_utc = [15] * 9
utc_tai = [6.6] * 9
totals = [
    rss([a, b, c, d])
    for a, b, c, d in zip(lu_clock, hm_interp, hm_utc, utc_tai)
]
print([round(x) for x in totals])

# Task 3: Table 3 final column
stat = rss([7.3, 1.5, 0.4])
sys = rss([2.0, 5.0, 0.1, 0.4, 0.9])
total = rss([stat, sys])
print(round(stat, 1), round(sys, 1), round(total, 1))
```

用上面这些已经四舍五入的表格输入运行，输出应接近：

```text
-150.4 7.4
1568 37
[22, 33, 23, 18, 22, 24, 29, 18, 19]
7.5 5.5 9.3
```

这些结果与论文目标值 `-150.4(7.3)e-18`、`22,33,23,18,21,24,29,18,19 e-16` 和 `7.4,5.5,9.2 e-16` 有轻微差异，因为这里使用的是表格已四舍五入后的输入值，并且表 1 有 `<0.1` 这样的非精确输入。严格复算需要论文内部未四舍五入的数值。

## 4. 软件和环境

论文实际使用或涉及：

| 模块 | 论文使用 | 复现说明 |
| --- | --- | --- |
| GNSS/PPP | Bernese GNSS Software | 这是有门槛的软件。没有 Bernese 时，可用 NRCan 在线 PPP、GipsyX、RTKLIB 等做探索性替代，但结果不等价于论文复现。 |
| RINEX 下载 | CDDIS | 常需要 NASA Earthdata 账号和正确目录结构。PPP 还需要精密星历、钟差、天线模型等产品。 |
| 相位测量 | USRP N210 SDR | 硬件用于实验采集。数据分析需要知道作者保存的相位格式和 sign convention。 |
| 噪声模拟 | FFT power-law noise | 可用 Python 实现，但论文没有给完整低通平台噪声参数和真实 uptime mask。 |
| 表格复算 | 任意脚本或电子表格 | Python `numpy/pandas/scipy` 足够做 L1 合成和检查点。 |

推荐的分析环境：

```text
Python >= 3.10
numpy
pandas
scipy
matplotlib
astropy    # 可选，用于 MJD/UTC 转换
```

当前仓库还没有脚本化分析管线。如果后续要真正支持复现，建议建立：

```text
data/
  raw/
  external/
  processed/
scripts/
  download_circular_t.py
  parse_circular_t.py
  fit_maser_drift.py
  simulate_dead_time.py
  combine_uncertainties.py
notebooks/
  01_frequency_chain.ipynb
  02_uncertainty_budget.ipynb
```

## 5. 硬件复现清单

如果目标是 L4 实验复现，论文中至少涉及这些硬件或功能模块：

| 模块 | 论文信息 | 用途 |
| --- | --- | --- |
| 线性 Paul 阱 `Lu-2` | 单个 `176Lu+` 离子 | 囚禁离子 |
| 646 nm 光 | Doppler cooling | 冷却 |
| 350 nm repump 光 | 由 701 nm 倍频产生；论文提到 mode hopping 是中断来源 | repump |
| 848 nm 钟激光 | 外腔二极管激光 | `1S0 -> 3D1` 询问 |
| 804 nm 光 | `1S0, F=7 -> 3D2, F=9` | 微运动测量 |
| 10 cm ULE 腔 | finesse 约 400000，真空 `1e-7 mbar`，温控 `33.2 deg C` | 稳定 848 nm 激光 |
| EOM/DDS | DDS 补偿 ULE 腔 `40 mHz/s` creep | 光频 offset 和伺服修正 |
| 微波源 | 两个微波频率 `f_1`、`f_2` | 超精细平均序列 |
| 氢钟 | Microchip MHM-2010，`10 MHz` | 本地飞轮 |
| 光频梳 | Menlo 掺铒飞秒光纤梳，`~250 MHz` repetition rate | 光频到微波的桥 |
| GNSS 接收机 | PolaRx5TR 双频接收机 | 本地 HM 到 UTC(USNO) 的 PPP 链路 |
| SDR | USRP N210 | 零死时间相位测量 |

这些信息只够建立硬件需求图，不够直接搭建实验。实际复现还需要真空、离子装载、激光稳频、光路、磁场、射频阱驱动、控制时序和安全规范等完整实验细节。

## 6. 时间轴和窗口定义

论文说 Lu+ 测量发生在 MJD 59270 到 59338，覆盖 2021 年 3 月到 5 月。表 2 的 5 天窗口为了对齐 Circular T，从 MJD 59269 到 59339 中选出 9 个有光钟数据的窗口。

MJD 从 UTC 午夜开始计日。下面日期是 UTC，`stop` 通常按右开区间理解，即 `[start, stop)`。

| 窗口 | MJD start | UTC start | MJD stop | UTC stop | Lu uptime | 表 2 Lu/TAI 总不确定度 |
| --- | ---: | --- | ---: | --- | ---: | ---: |
| 1 | 59269 | 2021-02-24 | 59274 | 2021-03-01 | 11% | `22e-16` |
| 2 | 59274 | 2021-03-01 | 59279 | 2021-03-06 | 2% | `33e-16` |
| 3 | 59284 | 2021-03-11 | 59289 | 2021-03-16 | 7% | `23e-16` |
| 4 | 59289 | 2021-03-16 | 59294 | 2021-03-21 | 37% | `18e-16` |
| 5 | 59294 | 2021-03-21 | 59299 | 2021-03-26 | 14% | `21e-16` |
| 6 | 59314 | 2021-04-10 | 59319 | 2021-04-15 | 9% | `24e-16` |
| 7 | 59324 | 2021-04-20 | 59329 | 2021-04-25 | 3% | `29e-16` |
| 8 | 59329 | 2021-04-25 | 59334 | 2021-04-30 | 30% | `18e-16` |
| 9 | 59334 | 2021-04-30 | 59339 | 2021-05-05 | 20% | `19e-16` |

注意事项：

- 光钟实际运行时间范围和 Circular T 对齐窗口范围不完全相同。
- 没有光钟数据的 5 天窗口没有进入表 2，但在月度 TAI 插值时会影响 dead time。
- 不要使用本地时区切窗口；时间传递和 Circular T 都按 UTC/MJD 处理。
- Circular T 399、400、401 的精确覆盖和字段应以 BIPM 原始报告为准。

## 7. 符号和正负号约定

高危提醒：本论文复算最容易错的不是数量级，而是正负号。任何中心频率复算在没有作者原始脚本时都必须逐项核对 sign convention。若正负号错，结果可能仍在 `1e-15` 量级，看起来合理但实际错误。

论文中频率链写成比值形式：

```text
f_Lu / f_SI
= (f_Lu,T1 / f_HM,T1)
* (f_HM,T1 / f_HM,T2)
* (f_HM,T2 / f_UTC(USNO),T2)
* (f_UTC(USNO),T2 / f_TAI,T2)
* (f_TAI,T2 / f_TAI,T3)
* (f_TAI,T3 / f_SI,T3)
```

复现时通常不直接乘一堆接近 1 的数，而是使用分数频率偏差：

```text
y(A/B) = f_A / f_B - 1
```

当所有 `y` 都很小时：

```text
f_A / f_C = (1 + y(A/B)) (1 + y(B/C))
          approx 1 + y(A/B) + y(B/C)
```

所以一阶近似下，链路中的分数频率偏差可以相加。

相位差到频率差的基本关系是：

```text
y(A/B) = d[x(A) - x(B)] / dt
```

如果 `x` 的单位是秒，`t` 的单位也是秒，则 `y` 是无量纲 `Hz/Hz`。例如某段时间 `Delta t` 内相位差变化 `Delta x`：

```text
average y(A/B) = Delta x / Delta t
```

数值例子：

```text
5 天 = 432000 s
若 x(A)-x(B) 在 5 天内增加 0.20 ns = 0.20e-9 s
则 y(A/B) = 0.20e-9 / 432000 = 4.63e-16
```

正负号最容易出错。复现时要固定一个约定：

- 本手册采用 `y(A/B) > 0` 表示 A 相对 B 走得更快。
- PPP 输出若是 `x(HM)-x(USNO)`，斜率就是 `y(HM/UTC(USNO))`，前提是软件输出的 `x` 符号与该定义一致。
- Circular T 字段可能使用自己的符号约定，必须按报告说明读取。论文写到 TAI 相对 TT/SI 的偏差使用 `y_TAI = -d`。
- 最终系统频移修正的加减号要跟表 1 保持一致。引力红移在表 1 中为正 `+1718e-18`。

## 8. 从原始数据到最终结果的流水线

| 步骤 | 输入 | 处理 | 输出 | 论文位置/检查点 |
| --- | --- | --- | --- | --- |
| 1. 光钟询问 | 离子响应、848 nm 激光、微波 `f_1/f_2` | Ramsey/hyper-Ramsey 伺服到 `f_Lu = nu_L + (2 f_1 + f_2)/3` | Lu+ 稳定的钟激光 | 图 1、式 (1) |
| 2. 光频梳比较 | 钟激光、comb `f_r/f_o/beat`、HM | 用光频梳把光频转换到 HM 可比较频率 | `f_Lu/f_HM` | 图 2 |
| 3. SDR 相位处理 | 20 MHz 下变频相位 | 对相位斜率求频率偏差；按 20 s 或实验采样平均 | Lu/HM 时间序列 | 图 4(a) 蓝点 |
| 4. PPP 链路 | 本地 RINEX、USN7 RINEX、精密 GNSS 产品 | PPP 估计 `x(HM)-x(USNO)`，30 s 间隔 | HM-UTC(USNO) 时间序列 | 图 4(a) 橙点 |
| 5. HM 漂移拟合 | HM-UTC(USNO) 约 80 天数据 | 二次模型拟合 HM offset/drift/aging | HM 漂移模型 | 图 4(a)，线性漂移约 `-3.7e-15/day` |
| 6. 漂移扣除 | Lu/HM 数据、HM 漂移模型 | 从本地观测扣除 HM 相对 UTC(USNO) 漂移 | `y(Lu/UTC(USNO))` | 图 4(b) |
| 7. 5 天分箱 | 漂移扣除后的数据、uptime mask | 按 Circular T 5 天窗口加权/平均 | 9 个 5 天结果 | 表 2 |
| 8. HM dead time | uptime mask、HM 噪声模型 | 模拟 `T1` 平均与完整 `T2` 平均差 | HM 插值不确定度 | 表 2，图 5 |
| 9. UTC(USNO)-TAI | Circular T 5 天相位数据 | 读取 `UTC(USNO)/TAI`，加入卫星链路不确定度 | `y(Lu/TAI)` | 表 2 |
| 10. 月度平均 | 5 天结果、Circular T 月度窗口 | 对每个 Circular T 报告求加权平均 | 399、400、401 三个月结果 | 图 6、表 3 |
| 11. TAI dead time | 月内有/无数据窗口、EAL/TAI 噪声模型 | 模拟 5 天到月度的 dead time | TAI 插值不确定度 | 表 3 |
| 12. TAI-SI | Circular T 的 `d` 和 `u` | 使用 `y_TAI = -d` 链接 SI 秒 | `f_Lu/f_SI` | 表 3 |
| 13. 系统频移 | 表 1 各系统项 | 加上 Lu+ 系统修正和引力红移，合成不确定度 | 修正后的绝对频率 | 表 1 |
| 14. 合并三个月 | 月度结果和不确定度 | 处理相关/非相关项，求加权平均 | `353 638 794 073 800.35(33) Hz` | 图 6 |

系统频移是对 Lu+ 物理参考频率的修正，表中放在第 13 步只是为了按数据分析流程组织；不要理解成时间链路末端才产生这些频移。

## 9. 光频梳和 SDR 方程

频率梳的基本关系是：

```text
nu_L = n f_r + f_o +/- f_beat +/- f_offsets
```

其中：

- `nu_L` 是 848 nm 钟激光频率。
- `n` 是 comb tooth index，通常是约百万量级的整数。
- `f_r` 是重复频率，论文中约 `250 MHz`。
- `f_o` 是 carrier-envelope offset。
- `f_beat` 是钟激光和最近 comb tooth 的拍频。
- `f_offsets` 包括 DDS、EOM、AOM 或电子混频引入的频率偏置。

论文描述的实现中，`f_r` 通过激光-comb beat 锁到 Lu+ 稳定钟激光，`f_o` 锁到 HM。HM 的 `10 MHz` 被倍频到 `980 MHz`，再与 `4 f_r` 附近的 `1 GHz` 信号混频，得到 `20 MHz` 信号，由 USRP N210 记录相位。

复现时必须向作者或实验日志确认：

- `n` 的值。
- 所有 beat 和 offset 的正负号。
- SDR 记录的相位单位、采样间隔和 unwrap 方法。
- cycle slip 检查方法和剔除规则。

若相位记录为 `phi(t)`，对应某个名义频率 `f0` 的分数频率偏差通常可写成：

```text
y = (1 / (2 pi f0)) d phi / dt
```

但这里的 `f0` 和符号取决于混频链路。没有实验配置表时，不能从论文文字唯一恢复最终小数部分。

## 10. PPP 和 UTC(USNO) 链接

论文使用本地 PolaRx5TR 接收机和 USN7 接收机的 RINEX 文件，通过 Bernese GNSS Software 做 PPP，得到 30 s 间隔的：

```text
Delta x = x(HM) - x(USNO)
```

处理所需材料通常包括：

- 本地接收机 RINEX observation/navigation 文件。
- USN7 RINEX 文件。
- 精密星历和钟差产品。
- 接收机/天线相位中心模型。
- 地球自转参数和潮汐/相对论等模型设置。
- Bernese PPP 配置。

公开数据只覆盖远端 USN7 和部分 GNSS 产品；本地 RINEX 未随论文公开。因此外部读者无法完整复现 HM-UTC(USNO) 链路，只能复现公开侧的数据获取和 PPP 工具流程。

论文给出的 PPP 链路稳定度结果：

```text
4.6e-15 * (tau/day)^-0.75
```

约 5 天后达到：

```text
1.3e-15
```

这一噪声底主要归因于 HM。

卫星频率传递不确定度使用论文式 (4)：

```text
u = sqrt(2) * u_A / tau_0 * (tau / tau_0)^-0.9
```

其中 `u_A = 0.2 ns`，`tau_0 = 5 d`。当 `tau = 5 d`：

```text
u = sqrt(2) * 0.2e-9 s / 432000 s
  = 6.5e-16
```

这对应表 2 中 `UTC(USNO)/TAI = 6.6e-16`。

## 11. 氢钟漂移和 dead time

论文用覆盖光钟测量的约 80 天 HM-UTC(USNO) 数据评估氢钟漂移。漂移不是纯线性，所以使用二次模型：

```text
y_HM(t) = a0 + a1 (t - t0) + a2 (t - t0)^2
```

也可以等价地拟合相位：

```text
x_HM(t) = b0 + b1 (t - t0) + b2 (t - t0)^2 + b3 (t - t0)^3
```

具体取决于输入是相位还是频率。论文报告：

- HM 线性漂移约 `-3.7e-15/day`。
- aging 约 `4.6e-15/day/year`。
- 5 天 PPP 残差统计不确定度约 `1.5e-15`。
- 漂移模型对最终结果贡献 `2e-16`，作为相关系统项处理。

HM dead time 模拟用于估计“光钟只在 `T1` 时间运行，完整 5 天窗口是 `T2`”造成的不确定度。论文噪声模型包含：

| 噪声项 | 参数 |
| --- | --- |
| 白相位噪声 | `5.1e-13 * (tau/s)^-1` |
| 白频率噪声 | `4.6e-14 * (tau/s)^-1/2` |
| 闪烁频率噪声 | `1.3e-15` |
| 额外平台噪声 | 低通白频率噪声，拟合约 5 到 60 分钟平台 |

伪代码：

```python
for window in five_day_windows:
    diffs = []
    for k in range(2000):
        y = generate_hm_noise(
            duration_days=5,
            dt=dt,
            white_phase=5.1e-13,
            white_freq=4.6e-14,
            flicker_freq=1.3e-15,
            plateau_model=plateau_params,
        )
        avg_full = mean(y over full T2)
        avg_uptime = mean(y over actual Lu uptime mask T1)
        diffs.append(avg_uptime - avg_full)
    sigma_dead_time = std(diffs)
```

无法从论文唯一恢复的参数：

- 真实 uptime mask。
- 仿真采样间隔 `dt`。
- 低通平台噪声的截止频率和幅度。
- 随机种子。

因此没有作者数据时，只能复现思想和数量级，不能严格复现图 5 黑点和表 2 的 HM interpolation 列。

## 12. Circular T 到 TAI/SI

表 3 涉及三类 TAI/SI 相关量：

1. `UTC(USNO)/TAI`：Circular T 每 5 天给出的时间尺度链接。
2. `TAI interpolation`：5 天窗口到月度 TAI 平均之间的 dead time。
3. `TAI/SI` 和 `PSFS`：TAI 标度间隔相对 SI 秒的校准，以及参与校准的主/次级频率标准不确定度。

论文说明 `TAI` 是 terrestrial time `TT` 的实现，Circular T 给出 TAI 标度间隔相对 SI 秒的偏差。使用关系：

```text
y_TAI = -d
```

TAI 插值模拟使用 EAL/TAI 稳定度模型。论文给出的模型是：

| 噪声项 | 参数 |
| --- | --- |
| 白频率噪声 | `1.4e-15 * (tau/s)^-1/2` |
| 闪烁频率噪声 | `2e-16` |
| 随机游走频率噪声 | `2e-17 * (tau/s)^1/2` |

PSFS 系统不确定度的处理需要 Circular T 中各主/次级标准的 `mu_B` 信息。论文认为三个月中大多数参与校准的钟相同，因此 PSFS 系统项按跨月相关处理。

## 13. 系统频移复算表

| 项 | 公式/方法 | 输入 | 输出 | 是否可由论文独立复算 |
| --- | --- | --- | --- | --- |
| 二阶塞曼 | `Delta nu = k B^2` | `k=-4.89264(88) Hz/mT^2`，`B=0.10084(20) mT` | `-140.7(0.6)e-18` | 可复算论文给出的数值合成；不可独立验证原始磁场测量 |
| 引力红移 | `Delta f/f = g h / c^2`，`h=H-N` | `g=9.7803(3) m/s^2`，`H=23.68(10) m`，`N=7.89(10) m` | `1718(36)e-18` | 可复算论文给出的数值合成；不可独立验证原始高程和 geoid 测量 |
| 过剩微运动 | 804 nm sideband spectroscopy | 三正交方向测量记录 | `-0.2(0.2)e-18` | 不可；缺原始谱 |
| 二阶多普勒 | 引用 [8] | 温度/运动参数 | `-0.1(0.1)e-18` | 不可；需 [8] 和实验参数 |
| rf ac-Zeeman | 引用 [8] | 阱驱动射频场参数 | `0.2(<0.1)e-18` | 不可；需 [8] |
| microwave ac-Zeeman | 微波 `sigma+/-` 极化不平衡 | 三次极化测量 | `-8.0(6.2)e-18` | 不可；缺测量记录 |
| microwave coupling | 假设 1% coupling error | 微波 `pi` time 和 coupling | `0.0(3.7)e-18` | 只能复算说明，不可验证 |
| 848 nm ac-Stark | hyper-Ramsey 剩余频移，约 `2/(pi T_R)*(Delta/Omega)^3` | ac-Stark step 误差、`T_R`、`Omega` | `0.0(1.2)e-18` | 部分；缺激光强度变化 |
| BBR | 黑体辐射模型 | 粗略温度 `35(10) deg C` | `-1.6(0.3)e-18` | 需模型系数 |

表 1 检查点：

```text
Lu+ systematics subtotal = -150.4(7.3)e-18
gravitational redshift  = +1718(36)e-18
total with redshift     = +1568(37)e-18
```

## 14. 不确定度合成

独立不确定度按平方和开根号：

```text
u_total = sqrt(u_1^2 + u_2^2 + ... + u_n^2)
```

表 3 最后一列可以这样复算：

统计项：

```text
sqrt(7.3^2 + 1.5^2 + 0.4^2) = 7.46 -> 7.4
```

系统项：

```text
sqrt(2.0^2 + 5.0^2 + 0.1^2 + 0.4^2 + 0.9^2) = 5.47 -> 5.5
```

总不确定度：

```text
sqrt(7.4^2 + 5.5^2) = 9.22 -> 9.2
```

表 1 的 Lu+ 系统不确定度 `7.3e-18` 在表 3 中写成 `0.1e-16`，因为：

```text
7.3e-18 = 0.073e-16 -> 0.1e-16
```

月度加权平均通常用非相关统计方差做权重：

```text
w_i = 1 / u_i^2
mean = sum(w_i * y_i) / sum(w_i)
u_mean = 1 / sqrt(sum(w_i))
```

相关系统项不能简单随三个月平均降低。例如 HM drift 和 HM diurnal 是跨月相关或作为潜在偏差处理，所以最终仍保留 `2.0e-16` 和 `5.0e-16`。

如果要严格复现论文的三个月加权平均，需要知道每个月的中心频率偏差，而论文图 6 只显示相对加权均值的图形，原始数值未全部列表。

## 15. 图表导航

| 图/表 | 读图目的 | 复现中对应步骤 |
| --- | --- | --- |
| 图 1 | 看 Lu+ 能级、微波/光学跃迁和询问序列 | 光钟定义、式 (1)、脉冲时序 |
| 图 2 | 看完整频率链 | `Lu+ -> HM -> UTC(USNO) -> TAI -> SI` |
| 图 3 | 看 HM 相对 Lu+ 和 UTC(USNO) 的稳定度 | HM 噪声模型、dead time 模拟 |
| 图 4 | 看 HM 漂移拟合、漂移扣除、5 天结果 | 频率链主分析 |
| 图 5 | 看 uptime fraction 对 HM 插值不确定度的影响 | dead time 模拟检查 |
| 图 6 | 看三个月结果和最终加权平均 | 最终频率 |
| 表 1 | Lu+ 系统频移预算 | 系统修正 |
| 表 2 | 5 天窗口统计不确定度 | `Lu/TAI` 5 天结果检查 |
| 表 3 | 月度和总不确定度预算 | 最终合成检查 |

## 16. 常用换算

| 换算 | 公式/结果 |
| --- | --- |
| 5 天到秒 | `5 d = 432000 s` |
| ns 相位到 5 天频率 | `0.2 ns / 432000 s = 4.63e-16`；乘 `sqrt(2)` 得 `6.55e-16` |
| mHz 到分数频率 | `49.75 mHz / 353638794073800 Hz = 1.407e-16` |
| 高度到引力红移 | 近似 `1 m -> 1.09e-16` |
| 表 1 到表 3 单位 | `1e-18 = 0.01e-16` |
| 绝对 Hz 到分数不确定度 | `0.33 Hz / 353638794073800 Hz = 9.3e-16` |
| MJD 日期 | MJD 0 是 1858-11-17 00:00:00 UTC |

## 17. 检查点

复现时建议逐步对照：

| 检查点 | 目标值 | 若不同，优先检查 |
| --- | ---: | --- |
| 表 1 Lu+ subtotal | `-150.4e-18` | 系统项单位是否是 `e-18` |
| 表 1 total with redshift | `+1568e-18` | 引力红移正负号 |
| 表 2 UTC(USNO)/TAI | `6.6e-16` | ns 到 5 天频率换算、`sqrt(2)` |
| 表 2 Lu/TAI total | `22,33,23,18,21,24,29,18,19 e-16` | HM interpolation 列、平方和 |
| 表 3 total statistical | `7.4e-16` | 是否只合成统计项 |
| 表 3 total systematic | `5.5e-16` | 相关系统项是否未平均降低 |
| 表 3 total | `9.2e-16` | 统计/系统平方和 |
| 最终频率 | `353 638 794 073 800.35 Hz` | 中心值需要作者原始数据，不能只靠表格复出 |

## 18. 无法完整复现项

没有作者数据时，以下项目不能严格复现：

- `0.35 Hz` 这个最终小数中心值。
- 图 4 的蓝点和橙点。
- HM 二次漂移拟合的完整参数。
- 图 5 黑点对应的真实 dead time 模拟。
- 每个月中心频率偏差和加权平均的原始输入。
- 微波极化、微运动、ac-Stark、BBR 等系统误差的原始评估。

这些不是文档缺少推导，而是论文没有公开完整原始数据。正确做法是向通讯作者请求数据，并要求至少包括 Lu/HM 时间序列、本地 RINEX、uptime mask、系统误差记录和分析配置。

## 19. 复现术语补充

| 术语 | 复现中在哪里用 |
| --- | --- |
| MJD | 切 5 天窗口和 Circular T 月度窗口 |
| `x` phase/time difference | GNSS/PPP 输出的时间差，单位通常是秒或 ns |
| `y` fractional frequency deviation | 频率偏差，单位 `Hz/Hz` |
| Allan deviation | 频率稳定度常用指标 |
| Hadamard deviation | 对频率漂移更稳健的稳定度指标；图 3 使用 |
| uptime fraction | 光钟在 5 天窗口中实际运行比例 |
| dead time | 光钟未运行但窗口仍需平均的时间 |
| EAL | free atomic timescale，用于 TAI 稳定度模型 |
| PSFS | 参与 TAI 校准的主/次级频率标准 |
| PFS/SFS/SRS | 主频标/次级频标/秒的次级表示 |
| geoid | 大地水准面，引力红移参考面 |
| ellipsoid/WGS84 | GNSS 使用的地球椭球参考 |
| EGM2008 | 用于估计 geoid undulation 的地球重力模型 |
| `f_o` | 光频梳 carrier-envelope offset |
| `f_r` | 光频梳 repetition rate |
| comb tooth index `n` | 光频梳齿编号，决定光频绝对值 |
| cycle slip | 光频梳或相位测量跳周，会破坏频率计数 |
