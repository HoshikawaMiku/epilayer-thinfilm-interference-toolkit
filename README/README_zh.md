# Epilayer & Thin-Film Interference Toolkit（外延层与薄膜干涉工具包）

一个全面的Python工具集，用于通过双光束干涉计算外延层厚度，以及模拟薄膜多光束干涉，具备数值分析和可视化功能。

[English](README.md) | [简体中文](README_zh.md)

## 概述

本项目整合了两个核心工具，用于研究薄膜和外延层中的光学干涉现象，适用于光学和材料科学领域的学生、研究人员及工程师：

1. **外延层厚度计算器**：基于双光束干涉原理计算外延层厚度，分析关键参数（折射率、波数）的敏感性，并可视化参数变化对结果的影响。

2. **薄膜多光束干涉模拟器**：采用数值方法模拟薄膜中的多光束干涉，包括透射光束的强度分布和振幅特性，并通过可视化呈现其物理行为。


## 核心功能

### 1. 外延层厚度计算
- 基于双光束干涉公式精确计算厚度：`d = k / (2 * n1 * cosθ₁ * ṽ)`
- 关键参数敏感性分析：
  - 外延层折射率（`n1`）
  - 红外波数（`ṽ`，波长的倒数）
- 厚度随参数变化的交互式可视化
- 支持自定义参数，适配不同材料体系（如SiC、GaN）


### 2. 薄膜多光束干涉模拟
- 光强分布计算，支持两种方法对比：
  - 区分s波/p波的分析（考虑偏振特性）
  - 简化计算（不区分偏振）
- 振幅特性分析：固定入射角下，追踪多阶透射光束的振幅方向
- 3D表面图展示透射光强在不同干涉角度范围内的分布
- 集成菲涅尔系数（s波/p波的反射/透射系数），精确建模波行为


## 环境要求

- Python 3.6+
- NumPy（用于数值计算）
- Matplotlib（用于可视化）

通过以下命令安装依赖：
```bash
pip install numpy matplotlib
```


## 使用示例

### 1. 外延层厚度计算
```python
from doublebeam_epi_thickness import EpilayerThicknessCalculator

# 初始化计算器（默认参数为SiC：n1=2.65，n2=2.68等）
calculator = EpilayerThicknessCalculator()

# 执行计算
calculator.calculate_thickness()
calculator.calculate_sensitivity()

# 打印数值结果和模型细节
calculator.print_results()

# 生成敏感性分析图（展示厚度与n1、波数的关系）
calculator.plot_sensitivity()

# 示例：自定义GaN材料参数
gan_calculator = EpilayerThicknessCalculator(
    n1=2.5,    # GaN外延层折射率
    n2=2.55,   # GaN衬底折射率
    nu_tilde=750,  # 波数（cm⁻¹）
    m=2        # 干涉级次
)
gan_calculator.print_results()
```


### 2. 薄膜多光束干涉模拟
直接运行脚本生成综合可视化结果：
```bash
python thin_film_multibeam_interference_sim.py
```

输出为PNG文件（例如`Thin_film_multiple_beam_interference_simulation_(Fixed_incident_angle=15°).png`），包含：
- 区分/不区分s波/p波的光强分布对比
- 不同阶次透射光束的振幅方向
- 透射光强随干涉角度变化的3D表面图


## 代码结构

| 文件 | 描述 |
|------|------|
| `doublebeam_epi_thickness.py` | 核心类`EpilayerThicknessCalculator`，实现基于双光束干涉的厚度计算、敏感性分析及结果可视化。 |
| `thin_film_multibeam_interference_sim.py` | 多光束干涉模拟工具，包括菲涅尔系数计算、光强分析及2D/3D可视化功能。 |


## 参数说明

### 外延层计算参数

| 参数 | 描述 | 单位 |
|------|------|------|
| `n1` | 外延层折射率 | 无量纲 |
| `n2` | 衬底折射率 | 无量纲 |
| `theta0_deg` | 空气中的入射角 | 度 |
| `nu_tilde` | 红外波数（1/λ） | cm⁻¹ |
| `m` | 初始干涉级次 | - |


### 薄膜模拟参数

| 参数 | 描述 | 单位 |
|------|------|------|
| `lambda_` | 入射光波长 | nm |
| `n` | 薄膜折射率 | 无量纲 |
| `h` | 薄膜厚度 | nm |
| `Ai` | 入射光振幅 | - |
| `theta_max` | 像方视场角范围 | 弧度 |
| `N` | 模拟中考虑的透射光束数量 | - |


## 许可证

本项目基于MIT许可证开源，详情参见`LICENSE`文件。