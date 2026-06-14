from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

RAW_COL_TO_REGION = {"0": "anterior", "1": "middle", "2": "posterior"}
REGION_ORDER: tuple[str, ...] = ("posterior", "middle", "anterior")
SUBJECTS: tuple[str, ...] = ("s2", "s4", "s7")
DATA_ROOT = Path("../datasets/predicted_activations")


def load_combined_per_subject(
    motif_folder: str,
    datasets: Sequence[str],
    subjects: Iterable[str] = SUBJECTS,
    data_root: Path | str = DATA_ROOT,
) -> pd.DataFrame:
    """Wide DataFrame mimicking `combined_<motif>_data.csv` in the original code.

    Columns: anterior, middle, posterior, Subject, ImageID.
    Rows are ordered subject-by-subject, then image-by-image within subject.
    """
    root = Path(data_root) / motif_folder
    pieces = []
    for subj in subjects:
        per_subj = []
        for ds in datasets:
            df = pd.read_csv(root / subj / f"{ds}.csv", index_col=0)
            df.columns = [RAW_COL_TO_REGION[c] for c in df.columns]
            per_subj.append(df[["anterior", "middle", "posterior"]])
        merged = pd.concat(per_subj, ignore_index=True)
        merged["Subject"] = subj
        merged["ImageID"] = merged.index.astype(str)
        pieces.append(merged)
    return pd.concat(pieces, ignore_index=True)


def load_mean_predicted(
    motif_folder: str,
    dataset: str,
    data_root: Path | str = DATA_ROOT,
) -> pd.DataFrame:
    """Across-subject mean predicted activations for one dataset (one row per image)."""
    root = Path(data_root) / motif_folder
    stacks = []
    for subj in SUBJECTS:
        df = pd.read_csv(root / subj / f"{dataset}.csv", index_col=0)
        df.columns = [RAW_COL_TO_REGION[c] for c in df.columns]
        stacks.append(df[["anterior", "middle", "posterior"]].values)
    mean = np.mean(np.stack(stacks, axis=0), axis=0)
    return pd.DataFrame(mean, columns=["anterior", "middle", "posterior"])
