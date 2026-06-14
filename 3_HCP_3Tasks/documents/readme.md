# 3_HCP_3Tasks

## Overview

This directory contains part of the code and intermediate outputs for **Study 2** of the paper *"A Tripartite Map of the Ventromedial Prefrontal Cortex"*.

Study 2 uses individual-level task fMRI data from the Human Connectome Project, covering three task paradigms (Emotion / Reward / Social) that correspond to the affect, valuation, and social functional domains. It first reproduces the Study 1 tripartite structure at the group level, and then validates the anterior–middle–posterior tripartite organization of VMPFC at the individual level through spatial classification (SVC / KNN / Logistic Regression, 5-fold cross-validation + permutation test).

> Note: the HCP task is officially named *Reward*; the paper categorizes it under the *valuation* functional domain, while the code retains the `reward` naming to match the official HCP data.
>
> The HCP S1200 group activation map under `data/group/` is too large to redistribute and requires users to agree to the HCP Data Use Terms before downloading. It is not bundled with this repository; before running, please download it from [HCP ConnectomeDB](https://db.humanconnectome.org) and place it back in the original location.

## Pipeline

Execute the notebooks under `codes/` in numerical order. Notebooks sharing the same numeric prefix belong to the same analysis stage.

| Notebook | Purpose / conclusion | Paper figure |
|---|---|---|
| `1_group.ipynb` | Load HCP S1200 group-level Cohen's d maps for the three tasks, derive activation and winner-takes-all parcellation for affect / reward / social, and compute the overlap across the three tasks | Fig. 2a |
| `2_1_individual_PrepareData.ipynb` | Prepare individual-level inputs: read per-subject peak coordinates for the three tasks, define voxel positions inside the VMPFC mask, and generate 5-fold train/test indices | Fig. 2b |
| `2_2_individual_KNN.ipynb` | KNN classification on left / right VMPFC, predicting task category from spatial coordinates, with 5-fold CV + permutation test | Fig. 2b; Suppl. Fig. 3b, left |
| `2_3_individual_SVC.ipynb` | Same as above, using linear SVC | Suppl. Fig. 3b, middle |
| `2_4_individual_Logistic.ipynb` | Same as above, using Logistic Regression | Suppl. Fig. 3b, right |
| `2_5_individual_Plot.ipynb` | Aggregate the three classifiers' accuracies on both hemispheres and plot them against the permutation null distribution | Suppl. Fig. 3b |
