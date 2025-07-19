import numpy as np
import cvxpy as cp

def compute_equitable_structure(A0: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """
    Solves a convex optimization problem to compute a structurally
    equitable matrix A_k, close to A0, respecting group symmetry.

    Parameters:
        A0 (np.ndarray): Original structural matrix (NxN), symmetric.
        labels (np.ndarray): Partition vector of nodes (length N).

    Returns:
        np.ndarray: Modified matrix A_k (NxN), equitable and symmetric.
    """
    N = A0.shape[0]
    A = cp.Variable((N, N), symmetric=True)

    # Objective: minimize L1 distance from A0
    objective = cp.Minimize(cp.norm1(A - A0))

    constraints = []

    # Diagonal must be zero
    constraints.append(cp.diag(A) == 0)

    # Non-negative weights
    constraints.append(A >= 0)

    # Equitable partition constraints
    groups = np.unique(labels)
    group_map = {g: np.where(labels == g)[0] for g in groups}

    for s in groups:
        nodes_s = group_map[s]
        for r in groups:
            nodes_r = group_map[r]
            if len(nodes_s) <= 1:
                continue
            # Enforce equal input from r to all nodes in s
            input_sums = [cp.sum(A[i, nodes_r]) for i in nodes_s]
            base = input_sums[0]
            for t in input_sums[1:]:
                constraints.append(t == base)

    # Solve the problem
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.ECOS, verbose=False)

    if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        raise RuntimeError(f"Optimization failed: {problem.status}")

    Ak = A.value

    # Post-processing checks and fixes
    Ak = np.nan_to_num(Ak)
    Ak = (Ak + Ak.T) / 2                    # enforce symmetry
    Ak[np.diag_indices_from(Ak)] = 0        # force diagonal to zero
    Ak[Ak < 0] = 0                          # clip negatives

    return Ak
