# 7_Region_Based_Parcellation

## Overview

This directory contains the code and intermediate outputs for **Study 4 (Multimodal Feature-Based Parcellation)** of the paper *"A Tripartite Map of the Ventromedial Prefrontal Cortex"*.

Study 4 uses the HCP Young Adult cohort (n = 667) and the Hansen Receptors Atlas and applies the same K-means clustering pipeline as Study 3 (connectivity-based parcellation; K = 2–6, n_init = 1000, random_state = 42) to independently construct a VMPFC voxelwise similarity matrix from four connectivity-independent brain features: gray-matter volume (GMV), cortical myelination (T1w/T2w, left and right hemispheres treated separately), resting-state brain entropy (BEN), and neurotransmitter receptor/transporter density (PET templates aggregated through the Schaefer-2018 1000-region atlas). Each modality independently yields K = 2–6 parcellations and is internally evaluated with silhouette and Davies–Bouldin indices. Finally, `6_Parcellation_Similarity.ipynb` computes pairwise permutation-maximum Dice across five modalities (Myelination / SC / BEN / GMV / Neurotransmitter; SC comes from the DTI parcellation in Study 3) to verify that the VMPFC partition structure is consistent across features.

> Note: `1_GMV_inhouse.ipynb` and `3_BEN_inhouse.ipynb` replicate the same pipeline on an in-house cohort of 240 subjects (FWHM = 8 mm instead of the HCP-YA 6 mm) as an internal robustness check; they do not correspond to a specific paper figure.
>
> `data/HCP_3T.tsv` lists the HCP-YA subject IDs. The raw volumes under `/home/guoqiu/NAS/Dep/HCP_GMV`, `/home/guoqiu/NAS/Dep/HCP_BEN`, etc., are too large to redistribute and are not bundled with this repository; download them from HCP ConnectomeDB before running. The Hansen Receptors Atlas is obtained from the NetNeurolab public repository (<https://github.com/netneurolab/hansen_receptors>).

## Pipeline

Execute the notebooks under `codes/` in numerical order. HCP-YA and in-house notebooks sharing the same numeric prefix replicate the same modality on different datasets.

| Notebook | Purpose / conclusion | Paper figure |
|---|---|---|
| `1_GMV_HCP_3T.ipynb` | HCP-YA (n = 667) gray-matter VBM, FWHM = 6 mm; voxelwise cross-correlation matrix → K-means parcellation (K = 2–6), outputs `GMV_HCP_3T_K{2..6}.nii.gz` together with silhouette / DBI internal indices | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `1_GMV_inhouse.ipynb` | Same pipeline replicated on the in-house 240-subject cohort (FWHM = 8 mm) as an internal robustness check | / |
| `2_Myelination_HCP_3T.ipynb` | Surface-based HCP-YA cortical myelination (T1w/T2w); left and right hemispheres are K-means parcellated separately (K = 2–6), producing `Myelination_HCP_3T_K{k}.func.gii` and `Myelination_HCP_3T_K{k}_R.func.gii` | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `3_BEN_HCP_3T.ipynb` | K-means parcellation on HCP-YA resting-state brain-entropy maps (FWHM = 6 mm), producing `BEN_HCP_3T_K{2..6}.nii.gz` | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `3_BEN_inhouse.ipynb` | Brain-entropy replication on the in-house 240-subject cohort (FWHM = 8 mm) | / |
| `4_Neurotransmitter.ipynb` | Hansen Receptors Atlas PET templates (FWHM = 4 mm) are aggregated into cortical receptor/transporter profiles via the Schaefer-2018 1000-region atlas using `neuromaps.Parcellater`; the resulting VMPFC voxelwise similarity matrix is K-means clustered, producing `Neurotransmitter_K{2..6}.nii.gz` in both 2 mm and 3 mm resolutions | Ext. Data Fig. 8;  Suppl. Fig. 1 |
| `5_Plot_Split.ipynb` | Splits the multi-label `nii` outputs into single-label volumes under `results/nii_by_label/` and projects them onto the cortical surface (`results/gii/`, `results/gii_by_label/`) via `wb_command -volume-to-surface-mapping`, for downstream plotting | / |
| `6_Parcellation_Similarity.ipynb` | Computes pairwise permutation-maximum Dice across the five modalities (Myelination / SC / BEN / GMV / Neurotransmitter; best assignment over all label permutations per K), producing `Dice_K{2..6}.csv`. K = 3 yields the highest mean Dice, consistent with the paper's conclusion that K = 3 is the only resolution at which every modality pair reaches Dice ≥ 0.50 | Ext. Data Fig. 8 |
