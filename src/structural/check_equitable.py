import numpy as np

def is_equitable(matrix: np.ndarray, labels: np.ndarray, tol: float = 1e-5) -> bool:
    """
    Checks if the given partition is equitable on the provided adjacency matrix.

    Parameters:
        matrix (np.ndarray): Adjacency matrix (NxN), assumed symmetric.
        labels (np.ndarray): Array of group assignments (length N).
        tol (float): Tolerance for numerical equality.

    Returns:
        bool: True if partition is equitable, False otherwise.
    """
    # N = matrix.shape[0]
    groups = np.unique(labels)
    group_map = {g: np.where(labels == g)[0] for g in groups}

    for s in groups:
        nodes_s = group_map[s]
        for r in groups:
            nodes_r = group_map[r]

            # Compute the input from group r to each node in group s
            inputs = matrix[nodes_s][:, nodes_r].sum(axis=1)

            # Check if all nodes in group s receive the same input from group r
            if not np.allclose(inputs, inputs[0], atol=tol):
                return False

    return True
