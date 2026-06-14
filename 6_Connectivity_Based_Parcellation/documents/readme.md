# 6_Connectivity_Based_Parcellation

## Overview

This directory contains the post-processing code and group-level parcellation maps for **Study 4 — Generality across cohorts** of the paper *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* (Ext. Data Fig. 7).

Study 4 replicates the K-means VMPFC parcellation pipeline (K = 2–6, n_init = 1000, random_state = 42) across multiple cohorts and modalities to demonstrate cross-cohort reproducibility. Per-voxel connectivity fingerprints (resting-state functional or diffusion-MRI tractography) are clustered with CBPtools, then group-level parcellations are compared across datasets via permutation-maximum Dice and evaluated per dataset with silhouette / Davies–Bouldin indices.

Datasets bundled under `data/cbptools/` (one folder per cohort × modality):

| Dataset folder | Cohort × modality |
|---|---|
| `BCP_age_0_3_resting` / `BCP_age_0_3_resting_remap` | Baby Connectome Project (0–3 y), resting fMRI; the `_remap` variant is produced by `1_BCP.ipynb` to align infant cluster labels with the adult parcellation |
| `HCP_D_age_05_11_resting` / `HCP_D_age_12_21_resting` | HCP-Development, resting fMRI, two age strata |
| `HCP_YA_age_22_35_resting_3T` / `HCP_YA_age_22_35_resting_7T` / `HCP_YA_age_22_35_movie` / `HCP_YA_age_22_35_DTI` | HCP-Young Adult, four modalities (3 T resting, 7 T resting, 7 T movie, DTI tractography) |
| `HCP_A_age_36_60_resting` / `HCP_A_age_61_100_resting` | HCP-Aging, resting fMRI, two age strata |
| `Inhouse_age_18_30_resting` / `Inhouse_age_18_30_DTI` | In-house young-adult cohort, resting fMRI and DTI |
| `Primate` | Non-human primate, resting fMRI |

> The dHCP preterm-neonatal cohort was evaluated upstream but is not part of Study 4 and is not included in this directory.

### Not bundled in this directory

- **CBPtools driver code and raw workspace.** The per-dataset CBPtools YAML / shell scripts (`codes/cbptools/`) and the full CBPtools workspace (`results/cbptools/<dataset>/{group,individual,log}`) are run externally on the lab cluster against NAS-hosted time-series data; they are not part of this public release. Only the final group parcellation maps (`data/cbptools/<dataset>/K{2..6}.nii.gz`) and per-dataset internal-validity tables (`data/cbptools/<dataset>/internal_validity.tsv`) are shipped here. To rebuild the parcellation maps from raw imaging data, install CBPtools (<https://github.com/inm7/cbptools>) and supply your own subject list / mask paths.
- **Neurosynth data.** `4_Decode_Parcel.ipynb` instantiates a `neurosynth.Dataset`; the underlying term-association database is not bundled. Download it from <https://neurosynth.org> (or via `neurosynth.Dataset.load(...)`) into `data/neurosynth_data/` before running.
- **Subject lists.** Per-cohort participant TSVs are excluded from the public repository; they are only required for re-running the upstream CBPtools pipeline.

### Cross-study dependency

`7_Region_Based_Parcellation/codes/6_Parcellation_Similarity.ipynb` consumes the HCP-YA DTI parcellation produced here as the structural-connectivity reference. In this slim layout that reference lives at `data/cbptools/HCP_YA_age_22_35_DTI/K{2..6}.nii.gz`.

## Pipeline

Execute the notebooks under `codes/` in numerical order.

| Notebook | Purpose / conclusion | Paper figure |
|---|---|---|
| `0_copy_files.ipynb` | Stages per-dataset CBPtools outputs (`group/K{2..6}.nii.gz`, `individual/internal_validity.tsv`) from the external CBPtools workspace into `data/cbptools/<dataset>/`. Pre-run; rerun only if you reproduce the upstream CBPtools pipeline yourself | / |
| `1_BCP.ipynb` | Relabels the Baby Connectome Project (BCP) K = 2–6 parcellations so that infant cluster IDs match the adult tripartite order; outputs the `BCP_age_0_3_resting_remap` parcellation set used in all downstream comparisons | / |
| `1_Parcellation_Similarity.ipynb` | Cross-dataset agreement: for each K ∈ {2..6}, computes the per-dataset-pair permutation-maximum Dice from `data/cbptools/<dataset>/K{k}.nii.gz`, writes `results/scores/Dice_K{k}.csv`, and renders `plots/heatmap/Dice_{k}.svg` | Ext. Data Fig. 7 |
| `2_Plot_Internal_Validity.ipynb` | Per-dataset silhouette / Davies–Bouldin curves over K = 2–6 from `data/cbptools/<dataset>/internal_validity.tsv`; outputs `plots/internal_validity/<dataset>.{png,svg}` | Ext. Data Fig. 7 |
| `3_Decode_FC_Parcel.ipynb` | Builds per-parcel mean resting-state functional connectivity fingerprints used by the radar-plot decoding | / |
| `4_Decode_Parcel.ipynb` | Neurosynth term-association decoding per VMPFC parcel; requires `data/neurosynth_data/` (see above) | / |
| `4_Plot_FC_Parcel_Decode.ipynb` | Renders the FC-decoding radar plots (`plots/radar_plot*.{png,svg}`) from the `data/Parcel_FC/` mean-FC tables | / |

