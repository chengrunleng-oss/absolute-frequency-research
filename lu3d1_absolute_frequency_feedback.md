# `lu3d1_absolute_frequency_explained.md` 最新公式审核复审

审核对象：

- 主解说：`lu3d1_absolute_frequency_explained.md`
- 配套复现手册：`reproduction_guide.md`
- 原始论文：`2502.10004v3.pdf`

本轮在公式审核基础上新增校正：**必须区分 `20 MHz` 完整累积相位 $\Phi_{20}$ 与去掉标称载波后的剩余相位 $\phi_{20}$；前者的导数给 $f_{20}$，后者的导数才给 $\delta f_{20}$。** 本反馈已基于修改后的当前文件重新审核，旧待办不再保留。

## 1. 复审结论

本轮意见已落实。当前解说已经形成两级公式导航：

1. Figure、Table 或结论首次使用公式时，附近直接显示最小公式卡片。
2. 第 5 节集中显示公式本体，并链接到后文详细推导、变量定义、成立条件和数值代入。

论文 Eq. (1)-(4)、PPP 稳定度经验式、HM 二次漂移、TAI/EAL 三分量噪声模型等均已使用可复制、可搜索的 Markdown/LaTeX 排版，不再依赖公式截图或只给出处。

### 1.1 最新相位符号校正已落实

第 8 节现在定义

$$
\Phi_{20}(t)=2\pi f_{20,0}t+\phi_{20}(t),
$$

并分别写出

$$
\frac{1}{2\pi}\frac{d\Phi_{20}}{dt}=f_{20}(t),
$$

$$
\frac{1}{2\pi}\frac{d\phi_{20}}{dt}
=f_{20}(t)-f_{20,0}
=\delta f_{20}(t).
$$

因此正文不再让 $\delta$ 看起来无来源：$\Phi_{20}$ 是包含标称线性增长的总相位，$\phi_{20}$ 是扣除 $2\pi f_{20,0}t$ 后的相位残差。原始量表、逻辑链和术语表也已同步。

## 2. 第 5 节公式速查已完成

第 5 节已从“只列编号的公式总览”改成“先看公式，再看推导”的公式速查，并明确区分：

- `【论文原式】`
- `【论文定量模型】`
- `【解读展开】`
- `【基础公式】`
- `【数值代入】`

### 2.1 Eq. (1) 已直接展示

$$
f_{\mathrm{Lu}}
=\frac{\nu_8+\nu_7+\nu_6}{3}
=\nu_L+\frac{2f_1+f_2}{3}.
$$

附近重复定义 $\nu_{6,7,8}$、$\nu_L$、$f_1$、$f_2$，并导航到第 6.4 节。

### 2.2 Eq. (2) 已直接展示

$$
\sigma_y(\tau)=
\frac{1}{f_{\mathrm{Lu}}}
\frac{1}{2\pi C T_R\sqrt{2N}}
\sqrt{\frac{t_u}{\tau}}
\approx
\frac{3.9\times10^{-15}}{\sqrt{\tau/\mathrm{s}}}.
$$

附近定义 $C,T_R,N,t_u,\tau$，说明它生成 Table 2 的 `Lu clock` 项，并导航到第 7.1 节。

### 2.3 Eq. (3) 已完整展示六段频率比

$$
\frac{f_{\mathrm{Lu}}}{f_{\mathrm{SI}}}
=
\frac{f_{\mathrm{Lu},T_1}}{f_{\mathrm{HM},T_1}}
\frac{f_{\mathrm{HM},T_1}}{f_{\mathrm{HM},T_2}}
\frac{f_{\mathrm{HM},T_2}}{f_{\mathrm{UTC(USNO)},T_2}}
\frac{f_{\mathrm{UTC(USNO)},T_2}}{f_{\mathrm{TAI},T_2}}
\frac{f_{\mathrm{TAI},T_2}}{f_{\mathrm{TAI},T_3}}
\frac{f_{\mathrm{TAI},T_3}}{f_{\mathrm{SI},T_3}}.
$$

$T_1,T_2,T_3$ 和 $f_{A,T}$ 在公式附近重复定义。该公式也已放到 Figure 2 的最小公式卡片中，因此读者查看链路图时无需跳转。

### 2.4 Eq. (4) 已展示公式与数值代入

$$
u(\tau)=
\frac{\sqrt2\,u_A}{\tau_0}
\left(\frac{\tau}{\tau_0}\right)^{-0.9}.
$$

文档在公式附近重复给出 $u_A=0.2\ \mathrm{ns}$、$\tau_0=5\ \mathrm{d}$、$\tau=5\ \mathrm{d}$，并直接计算

$$
u=6.55\times10^{-16},
$$

对应 Table 2 的 `6.6e-16`。Figure 2 附近也已放置 Eq. (4) 卡片。

## 3. PPP 稳定度经验式已补入

第 5.5 和 9.1 节现在直接显示

$$
\sigma_{y,\mathrm{PPP}}(\tau)
\approx4.6\times10^{-15}
\left(\frac{\tau}{\mathrm{day}}\right)^{-0.75},
$$

以及约 5 天后的噪声底

$$
\sigma_{y,\mathrm{floor}}\approx1.3\times10^{-15}.
$$

文档已说明：

- `-0.75` 是本文 HM/PPP 观测的经验缩放。
- 到达 HM 闪烁频率噪声底后不再按原幂律改善。
- 该关系与 Eq. (4) 的 `-0.9` 推荐卫星链路不确定度模型不是同一公式。

## 4. TAI/EAL 三分量噪声模型已补入

第 5.5 和 14.2 节直接显示：

$$
\sigma_{y,\mathrm{TAI}}^{\mathrm{WFM}}(\tau)
=1.4\times10^{-15}
\left(\frac{\tau}{\mathrm{s}}\right)^{-1/2},
$$

$$
\sigma_{y,\mathrm{TAI}}^{\mathrm{FFM}}(\tau)
=2\times10^{-16},
$$

$$
\sigma_{y,\mathrm{TAI}}^{\mathrm{RWFM}}(\tau)
=2\times10^{-17}
\left(\frac{\tau}{\mathrm{s}}\right)^{1/2}.
$$

三式分别标注为 white、flicker、random-walk frequency modulation。文档没有把三个稳定度表达式直接线性相加，而是说明它们用于生成或描述模拟轨迹，再比较有效 5 天集合和完整月度窗口的平均差。

Table 3 的 `TAI interpolation = 1.7, 2.9, 6.3` 已能直接回指到第 14.2 节模型；严格复现仍需要月内有效窗口分布和模拟设置。

## 5. HM quadratic drift 已显式化

第 5.5 和 12.1 节使用 `【解读展开】` 写出

$$
y_{\mathrm{HM}}(t)
=a_0+a_1(t-t_0)+a_2(t-t_0)^2.
$$

文档定义：

- $a_0$：frequency offset。
- $a_1$：linear drift，论文约 $-3.7\times10^{-15}/\mathrm{d}$。
- $a_2$：aging 引起的曲率。

文档没有把 $a_2$ 直接等同于带 `/year` 单位的 aging 数值，而是给出单位一致的条件映射：若 aging $A$ 表示 drift rate 每年变化 $A$，且时间单位为天，则

$$
a_2=\frac{A}{2\times365.25}.
$$

该映射明确标成合理推断，不冒充论文公布的拟合参数表。

## 6. Figure 与 Table 的公式导航已补强

- **Figure 2**：附近直接显示光频梳关系、Eq. (3) 和 Eq. (4)。
- **Figure 3**：附近直接显示 PPP `-0.75` 经验式、长期噪声底和 HM 噪声分量。
- **Figure 5**：新增

  $$
  \delta_k=\langle y_k\rangle_{T_1}-\langle y_k\rangle_{T_2},
  \qquad
  u_{\mathrm{HM,int}}=\operatorname{std}_k(\delta_k),
  $$

  把 HM 噪声模型与 Table 2 的插值不确定度直接连接。
- **Table 2**：明确回指 Eq. (2)、HM 模型、Eq. (4) 和平方和。
- **Table 3**：在表前直接展示 TAI/EAL 模型并解释数值来源。

## 7. 来源标签不再代替公式

当前新增部分均遵循：

```text
公式本体
-> 来源性质和论文位置
-> 变量与单位
-> 成立条件或复现边界
-> 对应 Figure/Table
-> 详细推导位置
```

没有发现“只写 `【论文给出】见 Eq. X`、但附近看不到公式本体”的新增段落。上一轮的相位—时间基础推导、Figure 1-6、Table 2/3 和系统频移公式也仍然保留。

## 8. 来源边界

以下内容仍无法由论文 PDF 唯一恢复，但主解说已明确标注，不属于公式遗漏：

1. comb tooth index、全部 beat/DDS/EOM offset 的带符号配置。
2. 作者 SDR 原始文件保存的是完整相位还是已扣除标称斜率的剩余相位，以及完整 Lu/HM transfer equation。
3. 本地 Lu/HM 时间序列、RINEX 和 uptime mask。
4. TAI/EAL 与 HM dead-time 模拟的全部实现参数和随机轨迹设置。
5. HM quadratic fit 的 $t_0,a_0,a_1,a_2$ 完整数值表。

## 9. 本轮验收清单

- [x] 第 5 节直接展示 Eq. (1)-(4)。
- [x] Eq. (3) 完整展示六个频率比。
- [x] Figure 2 首次使用频率链时显示公式本体。
- [x] 来源标签不再替代公式内容。
- [x] PPP `-0.75` 稳定度经验式已写入。
- [x] PPP 约 5 天达到 $1.3\times10^{-15}$ 噪声底已连贯解释。
- [x] PPP `-0.75` 与 Eq. (4) `-0.9` 已区分。
- [x] TAI/EAL WFM、FFM、RWFM 三条模型已写入。
- [x] Table 3 的 TAI interpolation 已回指模型。
- [x] HM quadratic drift 已显式化并标明来源性质。
- [x] 核心公式均可复制、可搜索。
- [x] 核心公式附近包含必要变量和单位。
- [x] 核心公式说明其 Figure/Table 用途和详细推导位置。
- [x] Figure 5 的 $T_1/T_2$ 平均差已写成公式。
- [x] 已区分 $\Phi_{20}\to f_{20}$ 与 $\phi_{20}\to\delta f_{20}$。
- [x] SDR 原始量表、逻辑链和术语表已同步总相位/剩余相位记号。
- [x] 6 张论文原图和前轮数学推导仍然有效。

## 10. 当前可用性判断

当前主解说已达到本轮目标：原论文 PDF 只用于核对上下文、原图和原始措辞，不再是查看核心公式本体的必需步骤。读者可以从 Figure、Table 或第 5 节公式速查直接进入数学关系，再按导航阅读详细推导。

剩余限制来自论文未公开的实验数据和配置，而不是当前文档仍缺少核心公式或定量模型。
