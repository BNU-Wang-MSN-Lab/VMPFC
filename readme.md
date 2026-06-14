# A Tripartite Map of the Ventromedial Prefrontal Cortex

Code and intermediate outputs accompanying the manuscript *"A Tripartite Map of the Ventromedial Prefrontal Cortex"*. The paper identifies a posterior–middle–anterior tripartite organisation of the VMPFC (affect / valuation / social cognition) and validates it across meta-analytic, task-fMRI, ANN-encoding, connectivity, and multimodal-feature evidence.

## Paper-to-directory mapping

| Paper section | Directory | Role |
|---|---|---|
| Study 1 — Characterising VMPFC functional diversity | `1_MACM_Clustering/` | Meta-Analytic Co-activation Modeling (MACM) on Neurosynth + BrainMap; partitions VMPFC into three functional subregions and validates the tripartite organisation on an independent database |
| Study 1 — Naming the clusters (Ext. Data Fig. 9) | `2_Name_Clusters/` | Combines pre-trained language model embeddings with Gemini 2.5 Pro to label the three MACM clusters (affect / valuation / social) |
| Study 2 — Individual-level validation (Fig. 2; Ext. Data Fig. 3) | `3_HCP_3Tasks/` | HCP-YA three-task fMRI (emotion / social / gambling); group-level contrasts + KNN / SVC / logistic-regression decoders that recover the tripartite organisation in individual subjects |
| Study 2 — ANN-encoding validation (Fig. 2; Ext. Data Fig. 3) | `4_NeuroGen_Predict_Activation/` | NeuroGen feature-weighted receptive-field DNN trained to predict per-voxel VMPFC activation; cross-validates the tripartite organisation in an encoding framework |
| Study 3 — Connectivity-based mechanisms of individual differences | `5_Connectivity_Predict_Activation/` | Resting-state functional connectivity predicts task activation patterns and explains individual differences in the VMPFC tripartite layout |
| Study 4 — Generality across cohorts (Ext. Data Fig. 7) | `6_Connectivity_Based_Parcellation/` | DTI structural-connectivity K-means parcellation replicated across multiple datasets (HCP-YA / HCP-Aging / non-human primates), demonstrating cross-cohort reproducibility |
| Study 4 — Generality across modalities (Ext. Data Fig. 8; Suppl. Fig. 1) | `7_Region_Based_Parcellation/` | K-means parcellation from four connectivity-independent features (GMV, cortical myelination, brain entropy, neurotransmitter receptor/transporter density); pairwise permutation-maximum Dice across five modalities confirms K = 3 as the most consistent resolution |

## Per-study layout

Every sub-directory follows the same convention:

```
<study>/
├── codes/        # Notebooks (run in numeric order) + small helper modules
├── data/         # Subject lists, masks, atlases, and other lightweight inputs
├── documents/    # Per-study readme.md / readme_zh.md with the full pipeline table
├── plots/        # Figure-quality PNG / SVG outputs
└── results/      # Parcellation NIfTI / GIfTI files, similarity matrices, intermediate caches
```

Raw imaging data (HCP volumes, in-house cohorts, PET templates) are not redistributed because of size and licensing. Paths under `/home/guoqiu/NAS/...` in the notebooks refer to the original author's storage; obtain the raw data from the matching public repositories (HCP ConnectomeDB, Hansen Receptors Atlas, NeuroGen) before re-running. The `results/` directory ships the pre-computed intermediates needed for the downstream notebooks (`5_*`, `6_*`, etc.) and for the paper figures.

## How to read this repository

1. Open the per-study `documents/readme_en.md` (or `readme_zh.md`) for the notebook-by-notebook pipeline of that study.
2. Notebooks under each `codes/` are numbered in execution order; same numeric prefix means the same analysis replicated on a different cohort (e.g. `1_GMV_HCP_3T.ipynb` vs `1_GMV_inhouse.ipynb`).
3. Cross-study dependencies are explicit. The clearest case: `7_Region_Based_Parcellation/codes/6_Parcellation_Similarity.ipynb` reads `../../6_Connectivity_Based_Parcellation/results/nii/HCP_YA_age_22_35_DTI_K{k}.nii.gz` as the structural-connectivity reference, so run Study 4-DTI before the cross-modality comparison.

## Environments

Two pip-tools environments cover the whole project:

- `vmpfc_general_requirements.{in,txt}` — general analysis stack (`nilearn`, `nibabel`, `scikit-learn`, `neuromaps`, `nimare`, plotting). Used by Studies 1, 2, 3, 4 and most plotting notebooks.
- `vmpfc_nsplus_requirements.{in,txt}` — pinned environment for Neurosynth-plus / NiMARE meta-analysis (`1_MACM_Clustering/`). Kept separate because it pins older versions of `nimare`, `pyale`, and friends that conflict with the general stack.

Install whichever environment matches the study you are running, e.g. `pip install -r vmpfc_general_requirements.txt`.

## Auxiliary content

- `plot_donghui_connectivity_predict_activation/` — standalone plotting scripts contributed for Study 3 (`5_Connectivity_Predict_Activation`), kept outside the main study tree because they were authored independently.
- The legacy `readme.md` at the top of `external_projects/Project_VMPFC_Final/` lists the same study-to-directory mapping in Chinese and is kept for backward reference.
