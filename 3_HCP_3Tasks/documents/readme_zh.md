# 3_HCP_3Tasks

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Study 2** 的部分代码与中间产物。

Study 2 使用 Human Connectome Project的个体水平任务态 fMRI 数据，对应三个任务范式（Emotion / Reward / Social）——分别代表 affect、valuation、social 三个功能域——在群体水平复现 Study 1 的三分区结构，并通过个体水平的空间分类（SVC / KNN / Logistic Regression，5-fold 交叉验证 + permutation test）验证 VMPFC 的 anterior–middle–posterior 三分区组织在个体水平同样成立。

> 注：HCP 任务原始名称为 *Reward*，论文中将其归入 *valuation* 功能域；下文沿用代码里的 `reward` 命名以匹配 HCP 官方数据。
>
> `data/group/` 下的 HCP S1200 group activation map 体积过大且需要用户同意 HCP Data Use Terms 后下载，未随仓库分发；运行前请从 [HCP ConnectomeDB](https://db.humanconnectome.org) 自行获取并放回原位。

## 运行流程

按编号顺序执行 `codes/` 下的 notebook。同一前缀编号的 notebook 属于同一分析阶段。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `1_group.ipynb` | 加载 HCP S1200 三任务 group-level Cohen's d 图，分别得到 affect / reward / social 的激活与 winner-takes-all 分区，并计算三任务的 overlap | Fig. 2a |
| `2_1_individual_PrepareData.ipynb` | 准备个体水平输入：读取每被试三任务的 peak 坐标、定义 VMPFC mask 内的体素位置、生成 5-fold 训练/测试索引 | Fig. 2b |
| `2_2_individual_KNN.ipynb` | 在 left / right VMPFC 上用 KNN 由空间坐标预测任务类别，5-fold CV + permutation test | Fig. 2b;  SupFig 3b, left |
| `2_3_individual_SVC.ipynb` | 同上，使用线性 SVC | SupFig 3b, middle |
| `2_4_individual_Logistic.ipynb` | 同上，使用 Logistic Regression | SupFig 3b, right |
| `2_5_individual_Plot.ipynb` | 汇总三种分类器在两个半球的准确率，与 permutation null 分布对比绘图 | SupFig 3b |
