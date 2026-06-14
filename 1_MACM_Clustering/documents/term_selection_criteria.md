# Term Selection Criteria

This document outlines the selection criteria and classification logic for cognitive terms used in the meta-analytic coactivation modeling (MACM) parcellation study of the ventromedial prefrontal cortex (vmPFC).

The data files corresponding to this description are:
- **Term Selection Sheet**: `../neurosynth_data/term_selection.xls`
- **Core Cognitive Mapping**: `../term_mapping.json`

---

## 1. Objectives of Term Selection

This study aims to parcellate the vmPFC based on meta-analytic coactivation maps using Neurosynth data. To ensure the robustness, validity, and interpretability of the clustering algorithms (e.g., K-Means or spectral clustering), raw high-frequency terms extracted from the literature underwent rigorous filtering to achieve the following goals:

1. **Highlight Cognitive Function**: Remove brain anatomical and spatial landmark terms.
2. **Ensure Semantic Specificity**: Filter out general vocabulary and experimental methodology terms to minimize background noise.
3. **Eliminate Feature Multicollinearity**: Consolidate morphological variations and synonyms to prevent redundant feature representation.

---

## 2. Selection Criteria

The dataset contains a total of **892** high-frequency terms, categorized using the binary indicator `selected` (where `1` indicates inclusion/selection, and `0` indicates exclusion/omission).

### 2.1 Inclusion Criteria
To be selected (`selected = 1`), a term must meet all of the following three conditions:

1. **Explicit Cognitive/Psychological Definition**: The term must represent a concrete, dissociable mental process or psychological state (e.g., learning, decision making, social, emotion).
2. **Defined Domain Classification**: The term must map cleanly to one of the three primary cognitive domains: **Social**, **Valuation**, or **Affect**. The `others` category is reserved for hard-to-classify cognitive terms that do not fit into these three primary domains (e.g., `alzheimer`, `approach`, `evaluation`).
3. **Canonical Wordform Representation**: If a concept is represented by multiple wordforms or derivatives, only the most representative and standard singular noun form is retained (e.g., keeping `reward` over `rewards` or `rewarding`).

### 2.2 Exclusion Criteria
Terms that do not satisfy the inclusion criteria are excluded (`selected = 0`) and categorized into three groups:

* **Anatomical Terms (`type = anatomy`)**
  - *Rationale*: These terms (e.g., `vmpfc`, `amygdala`, `prefrontal cortex`) designate specific anatomical brain structures or activation locations. Since the objective of this study is functional parcellation of the brain based on psychological processes, including spatial location terms would bias the parcellation towards spatial priors, rendering the functional parcellation scientifically redundant.
* **General/Unspecific Terms (`type = unspecific`)**
  - *Rationale*: This category comprises general experimental methodology terms (e.g., `resting state`, `connectivity`, `functional connectivity`), statistical metrics, or generic terms without specific psychological specificity (e.g., `traits`, `positive`, `mode`). Including these terms introduces substantial background noise, degrading clustering specificity.
* **Derivative/Redundant Terms (`type = *_duplicated`)**
  - *Rationale*: To prevent morphological variations (such as the plural `choices`, the adjective `emotional`, or the abbreviation `tom`) from introducing highly collinear features into the term-frequency matrix, all derivative forms are excluded, retaining only their corresponding canonical terms (e.g., `choice`, `emotion`, `theory mind`).
