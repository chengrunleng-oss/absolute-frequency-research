# `lu3d1_absolute_frequency_explained.md` 本轮修订后复审

审核对象：

- 主解说：`lu3d1_absolute_frequency_explained.md`
- 配套复现手册：`reproduction_guide.md`
- 原始论文：`2502.10004v3.pdf`

本轮最新修改意见是：**相位时间差部分的数学推导不够逻辑连贯清晰。** 本反馈已基于修改后的当前文件重新审核，不保留已经失效的旧待办。

## 1. 复审结论

本轮意见已落实。解说现在不再把 SDR、PPP 和 Circular T 的输入笼统称为同一种“相位”，而是建立了以下连续数学链：

```text
时钟读数 T(t)
-> 秒制时间偏差 x(t)
-> 两时标时间差 Delta x
-> 严格频率比
-> 小偏差近似 y ~= d(Delta x)/dt
-> 有限窗口端点差或多点斜率拟合
```

同时单独建立了电子测量链：

```text
弧度相位 phi_20
-> 20 MHz 拍频变化 delta f_20
-> comb repetition rate 变化 delta f_r
-> 光学频率变化 delta nu_L
-> Lu/HM 频率比
```

当前版本已能让初学者区分秒、弧度、Hz 和无量纲分数频率，并能判断关键公式何时是严格关系、何时只是一阶近似。

## 2. 已完成的 P0 修改

### 2.1 已定义所有基础量及单位

第 3.2 节新增定义表，明确区分：

- $T_A(t)$：时钟读数，单位 s。
- $x_A(t)=T_A(t)-t$：相对参考时间的时间偏差，单位 s。
- $\phi_A(t)$：电信号相位偏差，单位 rad。
- $\Delta x_{AB}=x_A-x_B$：A 相对 B 的时间差，单位 s。
- $y_A$ 和 $y(A/B)$：无量纲分数频率偏差。

文档还明确规定：单位为秒的 time deviation 即使在文献中被称作 phase，也不与弧度相位 $\phi$ 混写。

### 2.2 已从时钟读数推导严格频率比

当前文档先写

$$
T_A=t+x_A,qquad T_B=t+x_B,
$$

再得到

$$
\frac{f_A}{f_B}
=\frac{1+\dot x_A}{1+\dot x_B},
$$

以及严格式

$$
y(A/B)
=\frac{\dot x_A-dot x_B}{1+\dot x_B}.
$$

随后才在 $|\dot x_A|,|\dot x_B|\ll1$ 条件下写出

$$
y(A/B)\approx\frac{d\Delta x_{AB}}{dt}.
$$

原先把近似关系直接写成无条件等式的问题已经解决。

### 2.3 已区分瞬时导数和有限窗口平均

文档补入

$$
\bar y(A/B)
\approx
\frac{\Delta x_{AB}(t_2)-\Delta x_{AB}(t_1)}{t_2-t_1},
$$

并使用 `0.20 ns / 5 d = 4.63e-16` 的数值例子解释纳秒时间变化如何对应 $10^{-16}$ 频率偏差。

对于多点数据，文档给出

$$
\Delta x_k=a+b(t_k-t_0)+\epsilon_k,
$$

并说明只有窗口内平均频率近似恒定时才有 $b\approx\bar y$；HM drift 和 aging 需要更高阶模型。

### 2.4 已完成弧度相位到频率偏差的推导

文档从

$$
V(t)=V_0\cos[2\pi f_0t+\phi(t)]
$$

推到

$$
y(t)=\frac{1}{2\pi f_0}\frac{d\phi}{dt},
\qquad
x(t)=\frac{\phi(t)}{2\pi f_0}.
$$

并明确该结果依赖相位正号约定；若接收机保存 $-\phi$，结果整体反号。

### 2.5 SDR 不再从 20 MHz 相位直接跳到 Lu/HM

第 8 节以一个明确标注为人为选择的符号约定写出

$$
f_{20}=4f_r-98f_{\mathrm{HM}},
$$

因此

$$
\frac{1}{2\pi}\frac{d\phi_{20}}{dt}
=4\,\delta f_r-98\,\delta f_{\mathrm{HM}}.
$$

随后再通过

$$
\delta\nu_L
=n\,\delta f_r+delta f_o
\pm\delta f_{\mathrm{beat}}
\pm\delta f_{\mathrm{offsets}}
$$

说明 $\phi_{20}$、$f_r$ 和光学频率之间的层级关系。

文档没有虚构完整 transfer equation，而是明确指出论文未公开 comb tooth index、DDS/beat 全部符号、SDR 相位定义和完整 offset 配置，因此不能从论文文字唯一恢复每个样本到 Lu/HM 的最终系数。这符合来源边界。

### 2.6 PPP 已单独应用秒制时间差公式

第 10.4 节使用论文定义

$$
\Delta x_{\mathrm{PPP}}
=x(\mathrm{HM})-x(\mathrm{USNO}),
$$

推导

$$
y(\mathrm{HM/UTC(USNO)})
\approx\frac{d\Delta x_{\mathrm{PPP}}}{dt}.
$$

同时解释 `30 s` 输出、Figure 4 的 `6 h` 显示平均、固定延迟和随时间变化延迟的不同作用，以及 PPP 相关噪声不能按独立白噪声简单开平方。

### 2.7 Circular T 的两个负号已分开

第 10.5 节定义

$$
C_k=UTC-UTC(k),
$$

并推到

$$
y(UTC(k)/TAI)
\approx-\frac{dC_k}{dt}.
$$

文档把该**字段方向负号**与

$$
y_{\mathrm{TAI/SI}}\approx-d
$$

的**周期倒数负号**明确区分，不再把两者混为同一符号规则。

### 2.8 论文式 (4) 已由一般不确定度传播引入

第 10.6 节先写

$$
u^2(\bar y)=
\frac{u_x^2(t_1)+u_x^2(t_2)
-2\operatorname{Cov}[x(t_1),x(t_2)]}{\Delta T^2},
$$

再说明只有端点独立且等不确定度时才得到 $\sqrt2u_A/\Delta T$。最后引入论文引用的

$$
u(\tau)=\frac{\sqrt2u_A}{\tau_0}
\left(\frac{\tau}{\tau_0}\right)^{-0.9}.
$$

文档已明确：$\sqrt2$ 可由端点差分理解，`-0.9` 则来自文献 [34] 的链路缩放模型，二者不是同一步推导。

## 3. 已完成的 P1 修改

### 3.1 Figure 4(b) 负号已写成代数链

当前文档给出

$$
y(\mathrm{Lu/UTC})
\approx-y(\mathrm{HM/Lu})+y(\mathrm{HM/UTC}),
$$

并进一步说明论文绘制 $-y(\mathrm{Lu/UTC})$ 时组合方向如何变化。文档同时标注：由于原始数据列和处理脚本未公开，这只是符号结构解释，不是假装逐行还原作者代码。

### 3.2 已增加“原始输出到目标量”表

第 10.1 节现在分别列出 SDR、PPP、Circular T part 1 和 part 3 的原始量、单位、目标量和转换重点，能够防止读者把四种输入都理解成同一种 phase。

### 3.3 逻辑链和术语表已同步

第 17 节已展开为

```text
phi_20 -> delta f_20 -> delta f_r -> delta nu_L -> Lu/HM
x(HM)-x(USNO) -> slope -> HM/UTC(USNO)
```

第 18 节明确注明：

- $\phi$ 的单位是 rad。
- $\Delta x_{AB}$ 的单位是 s。
- $d\Delta x/dt$ 只有在共同标称秒和小偏差条件下才近似等于 $y(A/B)$。

## 4. 来源边界与非缺陷项

以下内容仍不能由论文 PDF 唯一恢复，但主解说已经诚实标注，不再构成文档逻辑缺陷：

1. SDR/光频梳完整 transfer equation 的所有带符号系数。
2. comb tooth index、全部 DDS/EOM/beat offset 和相位累加器定义。
3. 作者 Lu/HM 原始时间序列及每个数据列的 sign convention。
4. 本地 RINEX、完整 PPP 配置和硬件延迟温度记录。
5. Figure 5 的真实 uptime mask 与 plateau 噪声完整参数。

若要数值复现这些环节，仍需向作者请求实验配置和原始数据；不能通过补写基础公式消除数据缺失。

## 5. 本轮验收清单

- [x] 定义 $T_A$、$x_A$、$\phi_A$、$\Delta x_{AB}$、$y_A$ 和 $y(A/B)$。
- [x] 区分秒、弧度、Hz 和无量纲四种单位。
- [x] 先给严格频率比，再给小偏差近似。
- [x] 区分瞬时导数、有限窗口差分和多点斜率拟合。
- [x] 给出 `0.20 ns / 5 d` 数值例子。
- [x] 给出 $\phi -> x -> y$ 转换及符号约定。
- [x] SDR 部分写出拍频和梳传递层级。
- [x] 明确 SDR 完整转换不可唯一复现的来源边界。
- [x] PPP 使用 $x(HM)-x(USNO)$ 推导频率方向。
- [x] Circular T 从字段定义推导方向负号。
- [x] 分开解释字段方向负号和 $y_{TAI/SI}\approx-d$ 的倒数负号。
- [x] 式 (4) 先从协方差传播式引入，再说明 `-0.9` 的文献来源。
- [x] Figure 4(b) 的符号转换写成代数链。
- [x] 术语表注明 $\phi$、$\Delta x$ 的单位和适用条件。
- [x] Figure 1-6、论文式 (1)-(4)、Table 2/3 等上一轮成果仍然保留。

## 6. 当前可用性判断

当前主解说已经达到本轮要求：读者可以从时钟读数模型出发，不跳步地理解电子相位、秒制时间差、分数频率偏差、PPP、Circular T 和论文式 (4) 的关系，也能识别不同负号的来源。

剩余限制来自论文未公开的实验配置和原始数据，而不是当前文档仍缺少相位—时间基础推导。
