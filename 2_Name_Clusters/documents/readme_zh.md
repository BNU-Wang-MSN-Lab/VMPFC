# 2_Name_Clusters

## 项目简介

本目录包含论文 *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* 中 **Extended Data Fig. 9** 的全部代码与中间产物。

该分析对 Study 1 中"功能词三类划分（社会 / 价值 / 情感）"做数据驱动的独立验证：在两套相互独立的表征空间——预训练语言模型语义嵌入（Qwen3-Embedding-8B）与全脑 Neurosynth 元分析共激活图谱——对功能词分别做层次聚类，然后让一个独立的大语言模型（Gemini 3 Pro）在不知道原始类别名的前提下重复 100 次盲标，统计标签分布。

## 运行流程

按编号顺序执行 `codes/` 下的 notebook。同一前缀编号的 notebook 属于同一分析阶段。

| Notebook | 主要作用或结论 | 对应论文图 |
|---|---|---|
| `0_copy_files.ipynb` | 从 `1_MACM_Clustering/` 拷贝 `term_mapping.json`、Neurosynth `dataset.pkl` 与 VMPFC mask | / |
| `1_PLM_clustering.ipynb` | 用 Qwen3-Embedding-8B 对 top-15 / top-50 功能词进行层次聚类 | ExDataFig 9a, left |
| `2_MetaAnalysis_clustering.ipynb` | 用 Neurosynth 全脑元分析图谱做层次聚类 | ExDataFig 9a, right |
| `3_1_ask_LLM.ipynb` | 把聚出的三类无名簇交给 Gemini 3.1 Pro，重复 100 次盲标 | ExDataFig 9b |
| `3_2_analysis_LLM.ipynb` | 汇总 100 次盲标结果，绘制标签占比 donut 图 | ExDataFig 9b |
