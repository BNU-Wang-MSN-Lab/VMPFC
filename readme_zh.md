# 腹内侧前额叶皮层的三分图谱

本仓库提供论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 的全部代码与中间结果。该研究在 VMPFC 上识别出后—中—前的三分功能组织（情感 / 价值 / 社会认知），并通过元分析、任务态 fMRI、ANN 编码、连接预测以及多模态特征等多条独立证据线对其加以验证。

## 论文章节与文件夹的对应关系

| 论文章节 | 文件夹 | 作用 |
|---|---|---|
| Study 1 — VMPFC 功能多样性刻画 | `1_MACM_Clustering/` | 基于 Neurosynth + BrainMap 的 Meta-Analytic Co-activation Modeling（MACM），将 VMPFC 划分为三个功能子区，并在独立数据库上验证三分组织 |
| Study 1 — 子区命名（Ext. Data Fig. 9） | `2_Name_Clusters/` | 使用预训练语言模型的文本嵌入结合 Gemini 2.5 Pro，对三个 MACM 子区进行命名（情感 / 价值 / 社会） |
| Study 2 — 个体水平验证（Fig. 2; Ext. Data Fig. 3） | `3_HCP_3Tasks/` | HCP-YA 三类任务 fMRI（emotion / social / gambling）；组水平对比 + KNN / SVC / Logistic 三类分类器在被试个体上还原三分结构 |
| Study 2 — ANN 编码验证（Fig. 2; Ext. Data Fig. 3） | `4_NeuroGen_Predict_Activation/` | NeuroGen 特征加权感受野 DNN，逐体素地预测 VMPFC 激活模式，从编码角度交叉验证三分组织 |
| Study 3 — 连接驱动的个体差异机制 | `5_Connectivity_Predict_Activation/` | 用静息态功能连接预测任务激活模式，解释 VMPFC 三分结构在被试间的差异来源 |
| Study 4 — 跨数据集的泛化性（Ext. Data Fig. 7） | `6_Connectivity_Based_Parcellation/` | DTI 结构连接 K-means parcellation 在多套数据集（HCP-YA / HCP-Aging / 非人灵长类）上的复现，验证跨队列稳定性 |
| Study 4 — 跨模态的泛化性（Ext. Data Fig. 8; Suppl. Fig. 1） | `7_Region_Based_Parcellation/` | 基于四类与连接无关的脑特征（灰质体积、皮层髓鞘化、脑熵、神经递质受体/转运体密度）进行 K-means parcellation；五模态两两 permutation-max Dice 显示 K = 3 是最稳定的划分 |

## 子文件夹结构

所有子目录均按以下统一约定组织：

```
<study>/
├── codes/        # Notebook（按数字顺序执行）以及小型工具模块
├── data/         # 被试列表、模板、图谱等轻量级输入
├── documents/    # 各 Study 独立的 readme.md / readme_zh.md，含完整 pipeline 表
├── plots/        # 出版级 PNG / SVG 输出
└── results/      # 分区 NIfTI / GIfTI 文件、相似度矩阵以及中间缓存
```

原始影像数据（HCP 体积数据、in-house 队列、PET 模板等）因体量与授权限制不随仓库分发，notebook 中 `/home/guoqiu/NAS/...` 形式的路径指向原作者的存储。若要重跑，请先从 HCP ConnectomeDB、Hansen Receptors Atlas、NeuroGen 等公共仓库获取原始数据。`results/` 中已附带下游 notebook（`5_*`、`6_*` 等）以及生成论文图所需的预计算中间结果。

## 使用方式

1. 查看每个 study 自带的 `documents/readme_en.md` 或 `readme_zh.md`，了解该 study 的 notebook 级 pipeline。
2. 每个 `codes/` 下的 notebook 按数字顺序执行；前缀数字相同代表同一分析在不同队列上的复制（例如 `1_GMV_HCP_3T.ipynb` 与 `1_GMV_inhouse.ipynb`）。
3. 跨 study 之间存在显式依赖。典型例子：`7_Region_Based_Parcellation/codes/6_Parcellation_Similarity.ipynb` 会读取 `../../6_Connectivity_Based_Parcellation/results/nii/HCP_YA_age_22_35_DTI_K{k}.nii.gz` 作为结构连接参考，因此跨模态比较之前需先完成 Study 4 的 DTI parcellation。

## 运行环境

整套项目维护两份 pip-tools 环境：

- `vmpfc_general_requirements.{in,txt}`：通用分析栈（`nilearn`、`nibabel`、`scikit-learn`、`neuromaps`、`nimare`、绘图依赖等）。涵盖 Study 1–4 的绝大部分 notebook。
- `vmpfc_nsplus_requirements.{in,txt}`：Neurosynth-plus / NiMARE 元分析专用环境（`1_MACM_Clustering/`）。因其 `nimare`、`pyale` 等版本与通用栈互不兼容，单独维护。

按需安装：`pip install -r vmpfc_general_requirements.txt`。

## 辅助内容

- `plot_donghui_connectivity_predict_activation/`：为 Study 3（`5_Connectivity_Predict_Activation`）独立贡献的绘图脚本集合，因来源独立而保留在主 study 树之外。
- `external_projects/Project_VMPFC_Final/readme.md` 是历史遗留的中文索引文件，与本表一致，仅保留以备追溯。
