# 4_NeuroGen_Predict_Activation

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Study 2** 的 ANN encoding 验证部分（与 `3_HCP_3Tasks/` 共同支撑 Fig. 2 与 Extended Data Fig. 3）。

我们使用深度网络驱动的 fwRF（feature-weighted Receptive Field）编码模型，在 NSD 数据集上为每个 VMPFC voxel 拟合视觉特征到神经反应的映射，并将训练好的编码器迁移到独立的刺激库上预测响应。通过对每个 VMPFC 子区在不同情绪/价值/社会刺激集上的预测反应进行比较，验证 **后部—情感、中部—价值、前部—社会认知** 的三分组织。主分析使用编码精度 r > 0.05 的 3 名 NSD 被试（s2 / s4 / s7）；r > 0.01 的 6 被试 sensitivity 分析作为补充。

### 上游代码与方法

`codes/src/`、`codes/torchmodel/`、`codes/getmaskedROImean.py`、`codes/fwrf_ROIvoxel_mean.py` 以及 `datasets/dataset_predict_resize.py`、`datasets/h5py_transform_resize.py` 用于训练 fwRF 编码器与生成预测，**改编自以下公开工作**，本研究在其基础上做了 VMPFC ROI 与下游分析适配：

- **fwRF 模型与 NSD 数据加载**：<https://github.com/styvesg/nsd>
- **NeuroGen 框架**：<https://github.com/zijin-gu/NeuroGen>

## 运行流程

按编号顺序执行 `codes/` 下的 notebook。`utils/plot.py` 提供共享的数据加载常量与函数。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `1_plot_motif_single.ipynb` | 在 3 组单 motif 刺激（PISC+Parade 社会、Food_5k+Food_11 价值、ECED+GAPED 情感）上验证 anterior / middle / posterior 子区的优势激活；LMM + Tukey HSD | Fig. 2c |
| `2_plot_motif_intersection.ipynb` | 在 4 组 motif 交叉刺激（CFD = social∩value、Antique = value∩affect、SMID = social∩affect、NAPS_ERO = 三向交叉）上检验每个子区是否显著高于 0；one-sample t-test + FDR-BH | Ext. Data Fig. 3b |
