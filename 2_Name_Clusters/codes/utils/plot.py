import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.cluster.hierarchy import dendrogram


def circular_dendrogram(Z, term_color_mapping, figsize=(14, 14),
                        gap_fraction=0.02, r_inner=0, r_outer=1.0,
                        line_width=0.8, font_size=9, label_pad=0.06,
                        colored_branches=True, n_clusters=3,
                        rotation_degrees=0, flip=False):
    """
    Plots a circular dendrogram where branches are colored based on a majority vote
    of their subtree leaf nodes.

    Args:
        Z (ndarray): SciPy linkage matrix.
        term_color_mapping (dict): Mapping of {term_label: color}, matching sample order.
        figsize (tuple, optional): Figure size. Defaults to (14, 14).
        gap_fraction (float, optional): Fraction of the circle left blank at the top (0~1). Defaults to 0.02.
        r_inner (float, optional): Radius of the root node (innermost). Defaults to 0.
        r_outer (float, optional): Radius of the leaf nodes (outermost). Defaults to 1.0.
        line_width (float, optional): Width of the dendrogram lines. Defaults to 0.8.
        font_size (int, optional): Font size for leaf labels. Defaults to 9.
        label_pad (float, optional): Spacing between labels and the outer circle. Defaults to 0.06.
        colored_branches (bool, optional): If True, branches are colored by majority vote. Defaults to True.
        n_clusters (int, optional): Number of clusters for top-level branch coloring. Defaults to 3.
        rotation_degrees (float, optional): Overall rotation angle in degrees. Defaults to 0.
        flip (bool, optional): If True, mirrors the dendrogram layout radially. Defaults to False.

    Returns:
        tuple: (fig, ax) Matplotlib figure and axes objects.
    """
    labels = list(term_color_mapping.keys())
    n = len(labels)

    dn = dendrogram(Z, labels=labels, no_plot=True)
    icoord = np.array(dn['icoord'])
    dcoord = np.array(dn['dcoord'])
    ivl = dn['ivl']
    leaf_order = dn['leaves']

    x_min, x_max = 5, 5 + (n - 1) * 10
    total_angle = 2 * np.pi * (1 - gap_fraction)

    start_angle = np.pi / 2 + np.radians(rotation_degrees)
    direction = 1 if flip else -1

    def x2theta(x):
        return start_angle + direction * ((x - x_min) / (x_max - x_min) * total_angle)

    d_max = dcoord.max() * 1.05

    def d2r(d):
        return r_outer - d / d_max * (r_outer - r_inner)

    node_color = {}

    if colored_branches:
        def get_leaves(node_id):
            if node_id < n:
                return [int(node_id)]
            row = int(node_id - n)
            return get_leaves(int(Z[row, 0])) + get_leaves(int(Z[row, 1]))

        top_rows = set(range(len(Z) - (n_clusters - 1), len(Z)))
        top_node_ids = {n + r for r in top_rows}

        cluster_roots = set()
        for r in top_rows:
            for child in [int(Z[r, 0]), int(Z[r, 1])]:
                if child not in top_node_ids:
                    cluster_roots.add(child)

        cluster_color_map = {}
        for root in cluster_roots:
            lvs = get_leaves(root)
            colors = [term_color_mapping.get(labels[l], 'black') for l in lvs]
            cluster_color_map[root] = Counter(colors).most_common(1)[0][0]

        def assign_color(node_id, color):
            node_color[node_id] = color
            if node_id >= n:
                row = int(node_id - n)
                assign_color(int(Z[row, 0]), color)
                assign_color(int(Z[row, 1]), color)

        for root in cluster_roots:
            assign_color(root, cluster_color_map[root])

        for node_id in top_node_ids:
            node_color[node_id] = 'black'

        for i in range(n):
            node_color.setdefault(i, term_color_mapping.get(labels[i], 'black'))

        node_x = {}
        for disp_idx, orig_idx in enumerate(leaf_order):
            node_x[orig_idx] = 5 + disp_idx * 10
        for i in range(len(Z)):
            node_x[n + i] = (node_x[int(Z[i, 0])] + node_x[int(Z[i, 1])]) / 2

        ushape_info = []
        used = set()
        tol = 1e-8
        for u_idx, (ic, dc) in enumerate(zip(icoord, dcoord)):
            info = (None, None, None)
            for z_row in range(len(Z)):
                if z_row in used:
                    continue
                if abs(Z[z_row, 2] - dc[1]) < tol:
                    lid, rid = int(Z[z_row, 0]), int(Z[z_row, 1])
                    if (abs(node_x[lid] - ic[0]) < tol and abs(node_x[rid] - ic[3]) < tol):
                        info = (z_row, lid, rid)
                        used.add(z_row)
                        break
                    elif (abs(node_x[rid] - ic[0]) < tol and abs(node_x[lid] - ic[3]) < tol):
                        info = (z_row, rid, lid)
                        used.add(z_row)
                        break
            ushape_info.append(info)

    fig, ax = plt.subplots(figsize=figsize, subplot_kw={'projection': 'polar'})

    for u_idx, (ic, dc) in enumerate(zip(icoord, dcoord)):
        t = [x2theta(x) for x in ic]
        r = [d2r(y) for y in dc]

        if colored_branches:
            z_row, node_x1, node_x4 = ushape_info[u_idx]
            if z_row is not None and z_row < len(Z) - (n_clusters - 1):
                lc = node_color[node_x1]
                rc = node_color[node_x4]
                ac = node_color[n + z_row]
            else:
                lc = rc = ac = 'black'
        else:
            lc = rc = ac = 'black'

        zo = 1 if (lc == 'black' and rc == 'black' and ac == 'black') else 2

        ax.plot([t[0], t[1]], [r[0], r[1]], color=lc, lw=line_width, zorder=zo)
        ax.plot([t[2], t[3]], [r[2], r[3]], color=rc, lw=line_width, zorder=zo)

        t_start, t_end = min(t[1], t[2]), max(t[1], t[2])
        arc_t = np.linspace(t_start, t_end, 60)
        ax.plot(arc_t, np.full_like(arc_t, r[1]), color=ac, lw=line_width, zorder=zo)

    for i, lab in enumerate(ivl):
        theta = x2theta(5 + i * 10)
        deg = np.degrees(theta) % 360

        if 90 < deg < 270:
            rotation, ha = deg + 180, 'right'
        else:
            rotation, ha = deg, 'left'

        ax.text(theta, r_outer + label_pad, lab,
                rotation=rotation, ha=ha, va='center',
                fontsize=font_size,
                color=term_color_mapping.get(lab, 'black'),
                rotation_mode='anchor')

    ax.set_rticks([])
    ax.set_thetagrids([])
    ax.spines['polar'].set_visible(False)
    ax.grid(False)
    ax.set_ylim(0, r_outer + 0.45)
    plt.tight_layout()

    return fig, ax


def circular_dendrogram_make_adjacent(Z, labels, label_a, label_b):
    """
    Swaps the left and right subtrees of internal nodes to make `label_a` and `label_b`
    adjacent in the leaf arrangement, without altering the clustering structure (distances).

    Args:
        Z (ndarray): SciPy linkage matrix (will be copied).
        labels (list[str]): List of leaf labels.
        label_a (str): The label to be moved.
        label_b (str): The target neighbor label.

    Returns:
        ndarray: The adjusted linkage matrix.
    """
    Z = Z.copy()
    n = len(labels)
    lab2idx = {l: i for i, l in enumerate(labels)}
    idx_a, idx_b = lab2idx[label_a], lab2idx[label_b]

    def get_leaves(node):
        if node < n:
            return {int(node)}
        r = int(node - n)
        return get_leaves(int(Z[r, 0])) | get_leaves(int(Z[r, 1]))

    def find_lca(node, a, b):
        if node < n:
            return None
        r = int(node - n)
        left, right = int(Z[r, 0]), int(Z[r, 1])
        ll, rl = get_leaves(left), get_leaves(right)
        if a in ll and b in ll:
            return find_lca(left, a, b)
        if a in rl and b in rl:
            return find_lca(right, a, b)
        return node

    root = n + len(Z) - 1
    lca = find_lca(root, idx_a, idx_b)
    lca_row = int(lca - n)

    if idx_a not in get_leaves(int(Z[lca_row, 0])):
        Z[lca_row, 0], Z[lca_row, 1] = Z[lca_row, 1], Z[lca_row, 0]

    subtree_a = int(Z[lca_row, 0])
    subtree_b = int(Z[lca_row, 1])

    def push_right(node, target):
        if node < n:
            return
        r = int(node - n)
        if target in get_leaves(int(Z[r, 0])):
            Z[r, 0], Z[r, 1] = Z[r, 1], Z[r, 0]
        push_right(int(Z[r, 1]), target)

    def push_left(node, target):
        if node < n:
            return
        r = int(node - n)
        if target in get_leaves(int(Z[r, 1])):
            Z[r, 0], Z[r, 1] = Z[r, 1], Z[r, 0]
        push_left(int(Z[r, 0]), target)

    push_right(subtree_a, idx_a)
    push_left(subtree_b, idx_b)

    return Z