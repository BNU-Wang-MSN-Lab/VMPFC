# 6_Connectivity_Based_Parcellation

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Study 4 — Generality across cohorts**（Ext. Data Fig. 7）的后处理代码与组水平分区结果。

Study 4 沿用 K-means VMPFC 分区流程（K = 2–6，n_init = 1000，random_state = 42），在多个队列、多种模态上进行复现，验证 VMPFC 三分结构的跨队列稳健性。每个体素的连接指纹（静息态功能连接或 DTI 纤维束追踪）经 CBPtools 聚类后得到组水平分区图，再通过置换最大 Dice 进行跨数据集一致性比较，并按数据集计算 silhouette / Davies–Bouldin 内部指标。

`data/cbptools/` 下随分区图一同发布的数据集（每个子目录为一种队列 × 模态）：

| 数据集目录 | 队列 × 模态 |
|---|---|
| `BCP_age_0_3_resting` / `BCP_age_0_3_resting_remap` | Baby Connectome Project（0–3 岁）静息态；`_remap` 版本由 `1_BCP.ipynb` 生成，将婴儿期分区标签重排到成人三分顺序 |
| `HCP_D_age_05_11_resting` / `HCP_D_age_12_21_resting` | HCP-Development 静息态，按年龄分为两层 |
| `HCP_YA_age_22_35_resting_3T` / `HCP_YA_age_22_35_resting_7T` / `HCP_YA_age_22_35_movie` / `HCP_YA_age_22_35_DTI` | HCP-Young Adult，四种模态（3 T 静息、7 T 静息、7 T movie、DTI 结构连接） |
| `HCP_A_age_36_60_resting` / `HCP_A_age_61_100_resting` | HCP-Aging 静息态，按年龄分为两层 |
| `Inhouse_age_18_30_resting` / `Inhouse_age_18_30_DTI` | 自有 18–30 岁队列，静息态与 DTI |
| `Primate` | 非人灵长类静息态 |

> dHCP（preterm 新生儿队列）在上游进行了评估，但不属于 Study 4，本目录不包含 dHCP 相关数据与结果。

### 本目录不包含的内容

- **CBPtools 驱动代码与原始工作区。** 各数据集的 CBPtools YAML / shell 脚本（`codes/cbptools/`）以及完整 CBPtools 工作区（`results/cbptools/<dataset>/{group,individual,log}`）在实验室集群上对 NAS 时间序列数据外部运行，不随仓库发布；本目录只随附最终组分区图（`data/cbptools/<dataset>/K{2..6}.nii.gz`）与内部指标表（`data/cbptools/<dataset>/internal_validity.tsv`）。如需从原始影像重建分区，请自行安装 CBPtools（<https://github.com/inm7/cbptools>）并配置受试者列表与掩膜路径。
- **Neurosynth 数据。** `4_Decode_Parcel.ipynb` 调用 `neurosynth.Dataset`，term–activation 元分析数据库本身不随仓库发布。请从 <https://neurosynth.org> 下载（或通过 `neurosynth.Dataset.load(...)`）至 `data/neurosynth_data/` 后再运行。
- **受试者列表。** 各队列的 participant TSV 不随仓库发布；仅在自行复现上游 CBPtools 流程时需要。

### 跨 Study 依赖

`7_Region_Based_Parcellation/codes/6_Parcellation_Similarity.ipynb` 把本目录的 HCP-YA DTI 分区作为结构连接参考，在当前精简布局下，该参考位于 `data/cbptools/HCP_YA_age_22_35_DTI/K{2..6}.nii.gz`。

## 运行流程

按编号顺序执行 `codes/` 下的 notebook。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `0_copy_files.ipynb` | 把外部 CBPtools 工作区里的 `group/K{2..6}.nii.gz` 与 `individual/internal_validity.tsv` 归集到 `data/cbptools/<dataset>/`；已预先运行，仅在自行复现上游 CBPtools 流程时重跑 | / |
| `1_BCP.ipynb` | 对 BCP（Baby Connectome Project）K = 2–6 分区进行标签重排，使婴儿期簇 ID 对齐成人三分顺序，输出后续比较所使用的 `BCP_age_0_3_resting_remap` 分区 | / |
| `1_Parcellation_Similarity.ipynb` | 跨数据集一致性：对每个 K ∈ {2..6}，从 `data/cbptools/<dataset>/K{k}.nii.gz` 计算每对数据集的置换最大 Dice，输出 `results/scores/Dice_K{k}.csv` 与 `plots/heatmap/Dice_{k}.svg` | Ext. Data Fig. 7 |
| `2_Plot_Internal_Validity.ipynb` | 基于 `data/cbptools/<dataset>/internal_validity.tsv` 绘制各数据集在 K = 2–6 上的 silhouette / Davies–Bouldin 曲线，输出 `plots/internal_validity/<dataset>.{png,svg}` | Ext. Data Fig. 7 |
| `3_Decode_FC_Parcel.ipynb` | 构造各分区的静息态功能连接均值指纹，作为雷达图解码的输入 | / |
| `4_Decode_Parcel.ipynb` | 使用 Neurosynth 对各 VMPFC 分区进行 term–activation 解码；运行前需下载 `data/neurosynth_data/`（见上） | / |
| `4_Plot_FC_Parcel_Decode.ipynb` | 基于 `data/Parcel_FC/` 中的均值 FC 表绘制 FC 解码雷达图（`plots/radar_plot*.{png,svg}`） | / |
