# 2_Name_Clusters

## Overview

This directory contains the code and intermediate outputs for **Extended Data Fig. 9** of *"A Tripartite Map of the Ventromedial Prefrontal Cortex"*.

The analysis provides a data-driven validation of the three-class functional-term partition (social / valuation / affect) used in Study 1. Two independent representational spaces — pretrained language model semantic embeddings (Qwen3-Embedding-8B) and whole-brain Neurosynth meta-analytic association maps — are used to hierarchically cluster the functional terms. An independent large language model (Gemini 3 Pro) is then asked to assign a broad functional label to each cluster, blinded to the original category names, across 100 repeated runs. Label distributions are summarized as donut plots.

## Pipeline

Run the notebooks under `codes/` in numerical order. Notebooks sharing the same numeric prefix belong to the same analysis stage.

| Notebook | Purpose & Key Result | Paper Figure |
|---|---|---|
| `0_copy_files.ipynb` | Copy `term_mapping.json`, the Neurosynth `dataset.pkl`, and the VMPFC mask from `1_MACM_Clustering/` | / |
| `1_PLM_clustering.ipynb` | Embed the top-15 / top-50 functional terms with Qwen3-Embedding-8B using the template "cognitive neuroscience concept of {term}"; hierarchical clustering with cosine distance | Ext. Data Fig. 9a, left |
| `2_MetaAnalysis_clustering.ipynb` | Hierarchical clustering of whole-brain Neurosynth meta-analytic maps (voxels inside the VMPFC mask excluded) with correlation distance | Ext. Data Fig. 9a, right |
| `3_1_ask_LLM.ipynb` | Submit the three unnamed clusters to Gemini 3 Pro and collect blinded labels over 100 runs | Ext. Data Fig. 9b |
| `3_2_analysis_LLM.ipynb` | Aggregate the 100 blinded labelings and render the label-proportion donut plots | Ext. Data Fig. 9b |
