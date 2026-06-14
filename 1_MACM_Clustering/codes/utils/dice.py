from scipy.optimize import linear_sum_assignment
import numpy as np


def max_dice_score(y_true, y_pred, n):
    """Maximum mean Dice score under optimal label permutation.

    Cluster labels from unsupervised algorithms are arbitrary, so we use the
    Hungarian algorithm to find the one-to-one mapping between predicted and
    true labels that maximizes the mean per-cluster Dice coefficient.

    Parameters
    ----------
    y_true, y_pred : array-like of int
        Label arrays (labels in {1, ..., n}).
    n : int
        Number of clusters.

    Returns
    -------
    float
        Mean per-cluster Dice coefficient under the optimal label assignment.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    # Cost matrix: negative Dice between true cluster i and predicted cluster j
    # (Hungarian solves a minimization problem, so we negate.)
    cost_matrix = np.zeros((n, n))
    for i in range(1, n + 1):
        mask_true = (y_true == i)
        for j in range(1, n + 1):
            mask_pred = (y_pred == j)
            intersection = np.sum(mask_true & mask_pred)
            denom = np.sum(mask_true) + np.sum(mask_pred)
            dice = 0.0 if denom == 0 else 2.0 * intersection / denom
            cost_matrix[i - 1, j - 1] = -dice

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return -cost_matrix[row_ind, col_ind].sum() / n