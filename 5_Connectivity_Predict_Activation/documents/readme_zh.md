# 5_Connectivity_Predict_Activation

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Study 3** 的全部代码与中间产物（对应 Fig. 3[待确认]）。

Study 3 检验 **结构连接（SC，dMRI 探针追踪）与功能连接（FC，静息态 BOLD 相关）能否在跨被试上预测 VMPFC 三个 motif（social / valuation / affect）对应的任务激活图**。对每位被试：从 VMPFC mask 中每个 voxel 出发，提取其到全脑 BNA + MDTB seed 的连接特征向量；用 `LinearRegression` + `LeaveOneGroupOut` 跨被试交叉验证，预测该 voxel 在 social / valuation / affect 任务激活图中的强度，并以 2000 次 subject-label permutation 估计零分布。每个 motif 仅纳入有相应激活图的 inhouse 被试（n = 35–42）。

主分析在 inhouse 数据集（BNA 与 HOA 两套 ROI atlas）完成，并在外部 HCP 3T / 7T 数据集上验证泛化：用 inhouse 拟合的权重在 HCP 被试上预测对应 motif 激活，再与真实 HCP 激活图求相关。每幅条形图横轴是 3 种 motif，每个 motif 下两根条柱依次为 FC（浅色）/ SC（深色）；浅灰色虚线为该数据集的噪声上限（基于 test-retest 估计），y=0 的实线对应 permutation 零分布水平；显著性星号在论文图里由 PPT 补充。

### 上游代码与方法

`codes/connectome/`、`codes/prediction/`、`codes/preprocessing/` 中的 `.py` / `.sh` 脚本负责从原始 fMRI / dMRI 数据生成 SC、FC 连接矩阵与 motif 激活图，以及在 HCP 数据上做迁移预测，**改编自实验室既有 pipeline**，本研究在其基础上做了 VMPFC seed 选择与下游 motif 适配。

## 运行流程

按编号顺序执行 `codes/` 下的 notebook。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `1_predict_inhouse_BNA.ipynb` | 在 inhouse 数据集上构建 VMPFC voxel × BNA seed 的 SC/FC 连接特征，做 LeaveOneGroupOut 线性回归 + 2000 次 permutation，保存预测精度 `*_prediction.df.pkl` 与模型权重 `*.LinearRegression.pkl` | / |
| `2_stat_test.ipynb` | 读取 `1_*` 输出，计算每个 (X, y) 组合相对 permutation 零分布的 p 值 |             |
| `3_plot.ipynb` | 绘制 5 个数据集（inhouse_BNA / inhouse_HOA / HCP_3T_BNA / inhouse_predict_HCP_3T_BNA / inhouse_predict_HCP_7T_BNA）的预测精度条形图，附噪声上限与 permutation 基线 | Fig. 3 |
| `4_model_weight.ipynb` | 读取每个 motif 的 FC / SC 线性回归权重向量，做 pearsonr + regplot 比较 FC 与 SC 学到的 seed 重要性是否一致 | ExDataFig 5 |
