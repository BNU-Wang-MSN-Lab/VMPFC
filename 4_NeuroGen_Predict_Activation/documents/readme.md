# 4_NeuroGen_Predict_Activation

## Overview

This directory contains the ANN-encoding validation component of **Study 2** in the paper *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* (jointly supporting Fig. 2 and Extended Data Fig. 3 together with `3_HCP_3Tasks/`).

We use a deep-network–driven fwRF (feature-weighted Receptive Field) encoding model to fit a mapping from visual features to neural responses for each VMPFC voxel on the NSD dataset, and transfer the trained encoder to independent stimulus sets to predict responses. By comparing the predicted responses of each VMPFC subregion across affect / valuation / social stimulus sets, we validate the tripartite organization of **posterior—affect, middle—valuation, anterior—social cognition**. The primary analysis uses the 3 NSD subjects with encoding accuracy r > 0.05 (s2 / s4 / s7); the 6-subject sensitivity analysis at r > 0.01 serves as a supplementary check.

### Upstream code and methods

`codes/src/`, `codes/torchmodel/`, `codes/getmaskedROImean.py`, `codes/fwrf_ROIvoxel_mean.py`, and `datasets/dataset_predict_resize.py`, `datasets/h5py_transform_resize.py` are used to train the fwRF encoder and generate predictions. They are **adapted from the following public work**, with VMPFC ROI handling and downstream analysis added in this study:

- **fwRF model and NSD data loading**: <https://github.com/styvesg/nsd>
- **NeuroGen framework**: <https://github.com/zijin-gu/NeuroGen>

## Pipeline

Run the notebooks in `codes/` in numerical order. `utils/plot.py` provides shared data-loading constants and helper functions.

| Notebook | Purpose / conclusion | Paper figure |
|---|---|---|
| `1_plot_motif_single.ipynb` | On 3 single-motif stimulus sets (PISC+Parade for social, Food_5k+Food_11 for valuation, ECED+GAPED for affect), validate the dominant activation of the anterior / middle / posterior subregions; LMM + Tukey HSD | Fig. 2c |
| `2_plot_motif_intersection.ipynb` | On 4 motif-intersection stimulus sets (CFD = social∩value, Antique = value∩affect, SMID = social∩affect, NAPS_ERO = three-way intersection), test whether each subregion is significantly above zero; one-sample t-test + FDR-BH | Ext. Data Fig. 3b |
