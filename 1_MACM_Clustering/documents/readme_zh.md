# 1_MACM_Clustering

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Study 1** 的全部代码与中间产物。

Study 1 基于元分析共激活建模（Meta-Analytic Co-activation Modeling, MACM），将 VMPFC 划分为三个功能子区——后部（情感）、中部（价值）、前部（社会认知），并在独立元分析数据库（BrainMap）上验证其稳健性。

## 运行流程

按编号顺序执行 `codes/` 下的 notebook。同一前缀编号的 notebook 属于同一分析阶段。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `0_1_prepare_neurosynth.ipynb` | 构建 Neurosynth 数据集 | / |
| `0_2_prepare_BrainMap.ipynb` | 构建 BrainMap数据集 | / |
| `1_ReverseInference_VMPFC.ipynb` | 对 VMPFC mask 做反向推断，得到 top-15 功能词 | Fig. 1a |
| `2_1_MACM.ipynb` | 对每个 VMPFC voxel 计算共激活，PCA 降维后 K-means 聚类（K = 2…6），选定 K = 3 | Fig. 1b              |
| `2_2_MACM_Parcel_Decode.ipynb` | 对每个子区做功能解码 | Fig. 1d |
| `2_3_Plot_MACM.ipynb` | 渲染 K = 3 三分区的脑图 | Fig. 1b–d |
| `2_4_Plot_Wordcloud.ipynb` | 绘制K=2~6的每个子区的功能词云 | Fig. 1c; ExDataFig 2 |
| `3_1_Robust_Neurosynth.ipynb` | 检查阈值稳健性，最小研究阈值（≥100 / ≥150 / ≥200），重跑聚类 | SupFig. 3a, left |
| `3_2_Robust_Plot_Neurosynth.ipynb` | 绘制阈值稳健性结果 | SupFig. 3a, left |
| `3_3_Robust_BrainMap.ipynb` | 在 BrainMap 数据库上完整复现 MACM 流程 | SupFig. 4b |
| `4_Bias_Neurosynth.ipynb`          | 确认Neurosynth 无领域偏倚                                    | SupFig. 4a |
| `4_Bias_BrainMap.ipynb`            | BrainMap无领域偏倚，确认BrainMap和Neurosynth 无任务范式偏倚  | SupFig. 4c |


