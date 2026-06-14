# 5_Connectivity_Predict_Activation

## Project overview

This directory contains all code and intermediate outputs for **Study 3** of *"A Tripartite Map of the Ventromedial Prefrontal Cortex"* (corresponding to Fig. 3[待确认]).

Study 3 tests **whether structural connectivity (SC, derived from dMRI probabilistic tractography) and functional connectivity (FC, derived from resting-state BOLD correlations) can predict, across subjects, the task-activation maps of the three VMPFC motifs (social / valuation / affect)**. For each subject, for every voxel inside the VMPFC mask, we extract a connectivity feature vector from that voxel to whole-brain BNA + MDTB seeds; then a `LinearRegression` model with `LeaveOneGroupOut` cross-validation across subjects is used to predict the voxel's intensity in each motif's activation map, with 2000 subject-label permutations estimating the null distribution. Each motif uses only the inhouse subjects with the corresponding activation map (n = 35–42).

The main analysis is performed on the inhouse dataset (with both BNA and HOA ROI atlases) and is validated on external HCP 3T / 7T datasets: weights fitted on inhouse subjects are used to predict the corresponding motif activations in HCP subjects, then correlated against the real HCP activation maps. In each bar plot, the x-axis shows the three motifs and each motif has two adjacent bars: FC (light) and SC (dark); the light-gray dashed line is the noise ceiling for that dataset (estimated from test–retest reliability), and the solid line at y = 0 corresponds to the permutation null level. Significance asterisks shown in the published figure are added in PPT.

### Upstream code and methods

The `.py` / `.sh` scripts under `codes/connectome/`, `codes/prediction/`, and `codes/preprocessing/` build SC and FC connectivity matrices and motif activation maps from raw fMRI / dMRI data, and run the transfer prediction on HCP data. They are **adapted from existing lab pipelines**, with VMPFC seed selection and downstream motif adaptation added for this study.

## Pipeline

Run the notebooks under `codes/` in numbered order.

| Notebook | Main purpose / conclusion | Paper figure |
|---|---|---|
| `1_predict_inhouse_BNA.ipynb` | On the inhouse dataset, build SC / FC connectivity features of VMPFC voxel × BNA seed; run `LeaveOneGroupOut` linear regression with 2000 permutations; save prediction accuracies `*_prediction.df.pkl` and model weights `*.LinearRegression.pkl` | / |
| `2_stat_test.ipynb` | Load `1_*` outputs; for each (X, y) combination, compute the p value against the permutation null |  |
| `3_plot.ipynb` | Plot the prediction-accuracy bar charts for all 5 datasets (inhouse_BNA / inhouse_HOA / HCP_3T_BNA / inhouse_predict_HCP_3T_BNA / inhouse_predict_HCP_7T_BNA), with noise ceilings and the permutation baseline | Fig. 3 |
| `4_model_weight.ipynb` | Load the linear-regression weight vectors of each motif's FC / SC model; use `pearsonr` + `regplot` to compare whether FC and SC learn consistent seed importance | Ext. Data Fig. 5 |
