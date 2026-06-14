# 7_Region_Based_Parcellation

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Study 4（Multimodal Feature-Based Parcellation）** 的代码与中间产物。

Study 4 在 HCP Young Adult 与 Hansen Receptors Atlas 上，沿用 Study 3 的 K-means 聚类流程（K = 2–6），从四种与连接无关的脑特征独立构造 VMPFC 体素相似性矩阵并聚类：灰质体积（GMV）、皮层髓鞘化（T1w/T2w，左右半球分开）、静息态脑熵（BEN）、神经递质受体/转运体密度（PET 模板）。最终 `6_Parcellation_Similarity.ipynb` 在五种模态（Myelination / SC / BEN / GMV / Neurotransmitter，其中 SC 来自 Study 3 的 DTI 分区）之间逐对计算最大置换 Dice，验证不同模态下 VMPFC 分区结构的一致性。

## 运行流程

按编号顺序执行 `codes/` 下的 notebook，HCP-YA 与 in-house 两套同前缀编号属于同一模态、不同数据集的复现。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `1_GMV_HCP_3T.ipynb` | HCP-YA 灰质体积 VBM（FWHM = 6 mm）的 K-means 分区，输出 `GMV_HCP_3T_K{2..6}.nii.gz` 与 silhouette / DBI 内部指标 | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `1_GMV_inhouse.ipynb` | 自有 240 人队列 GMV 同流程复现（FWHM = 8 mm） | / |
| `2_Myelination_HCP_3T.ipynb` | HCP-YA 皮层 Myelin（T1w/T2w）表面数据，左右半球分别 K-means 分区，输出 `Myelination_HCP_3T_K{k}.func.gii`、`..._K{k}_R.func.gii` | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `3_BEN_HCP_3T.ipynb` | HCP-YA 静息态脑熵图（FWHM = 6 mm）的 K-means 分区，输出 `BEN_HCP_3T_K{2..6}.nii.gz` | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `3_BEN_inhouse.ipynb` | 自有 240 人队列脑熵图同流程复现（FWHM = 8 mm） | / |
| `4_Neurotransmitter.ipynb` | Hansen Receptors Atlas PET 模板（FWHM = 4 mm），用 Schaefer-2018 1000 区图谱通过 `neuromaps.Parcellater` 聚合为皮层受体/转运体特征，对 VMPFC 体素相似性矩阵进行 K-means 分区，输出 `Neurotransmitter_K{2..6}.nii.gz`（2 mm / 3 mm 双版本） | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `5_Plot_Split.ipynb` | 将多标签 `nii` 拆为单标签卷并经 `wb_command -volume-to-surface-mapping` 投影到 `results/gii/` 与 `results/gii_by_label/`，供绘图使用 | / |
| `6_Parcellation_Similarity.ipynb` | 在 Myelination / SC / BEN / GMV / Neurotransmitter 之间逐对计算最大置换 Dice，输出 `Dice_K{2..6}.csv`；K = 3 取得最高均值 Dice，与论文 K = 3 是唯一使所有模态对 Dice ≥ 0.50 的结论一致 | Ext. Data Fig. 8 |
