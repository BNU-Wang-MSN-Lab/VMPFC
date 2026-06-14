# 1_MACM_Clustering

## Overview

This directory contains the full code and intermediate outputs underlying **Study 1** of the paper *"A Tripartite Map of the Ventromedial Prefrontal Cortex"*.

Study 1 uses Meta-Analytic Co-activation Modeling (MACM) to partition the VMPFC into three functional subregions — posterior (affect), middle (valuation), and anterior (social cognition) — and validates this tripartite organization on an independent meta-analytic database (BrainMap).

## Pipeline

Execute the notebooks under `codes/` in numerical order. Notebooks sharing the same leading number belong to the same analytical stage.

| Notebook | Purpose / Result | Figure |
|---|---|---|
| `0_1_prepare_neurosynth.ipynb` | Build the Neurosynth dataset | — |
| `0_2_prepare_BrainMap.ipynb` | Build the BrainMap dataset | — |
| `1_ReverseInference_VMPFC.ipynb` | Reverse inference over the VMPFC mask; obtain top-15 functional terms | Fig. 1a |
| `2_1_MACM.ipynb` | Voxel-wise co-activation, PCA, and K-means clustering (K = 2…6); select K = 3 | Fig. 1b |
| `2_2_MACM_Parcel_Decode.ipynb` | Functional decoding of each subregion | Fig. 1d |
| `2_3_Plot_MACM.ipynb` | Render the K = 3 parcellation on the cortical surface | Fig. 1b–d |
| `2_4_Plot_Wordcloud.ipynb` | Per-subregion wordclouds for K = 2…6 | Fig. 1c; Ext. Data Fig. 2 |
| `3_1_Robust_Neurosynth.ipynb` | Threshold robustness: re-run clustering with minimum-studies ≥100 / ≥150 / ≥200 | Suppl. Fig. 3a, left |
| `3_2_Robust_Plot_Neurosynth.ipynb` | Plot the threshold-robustness results | Suppl. Fig. 3a, left |
| `3_3_Robust_BrainMap.ipynb` | Full MACM replication on the BrainMap database | Suppl. Fig. 4b |
| `4_Bias_Neurosynth.ipynb` | Confirm no paradigm bias in Neurosynth | Suppl. Fig. 4a |
| `4_Bias_BrainMap.ipynb` | Confirm no paradigm bias in BrainMap (joint consistency with Neurosynth) | Suppl. Fig. 4c |
