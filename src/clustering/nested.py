import numpy as np
from graph_tool.all import minimize_nested_blockmodel_dl

def run_nested_sbm(graph, config):
    """
    Runs Nested Stochastic Block Model (Nested SBM) inference on the given graph.
    Optionally performs MCMC sampling to explore alternative partitions.

    Parameters:
        graph (Graph): graph-tool graph (can be directed or undirected).
        config (dict): Configuration dictionary with clustering parameters.

    Returns:
        dict: {
            "labels": numpy array of node → group at selected level,
            "levels": list of np.ndarray for all levels,
            "order": None (not defined for Nested SBM),
            "state": graph-tool BlockState object
        }
    """
    print("[run_nested_sbm] Minimizing description length with nested SBM...")
    state = minimize_nested_blockmodel_dl(graph)

    # # Optional MCMC refinement
    # use_mcmc = config["clustering"].get("use_mcmc", False)
    # if use_mcmc:
    #     n_iter = config["clustering"].get("mcmc_trials", 1000)
    #     print(f"[run_nested_sbm] Running MCMC sweep ({n_iter} iterations)...")
    #     state.mcmc_sweep(niter=n_iter)

    # Extract all levels of the hierarchy
    levels = []
    for level in range(len(state.get_levels())):
        level_state = state.project_level(level)
        labels = level_state.get_blocks().a.copy()
        levels.append(labels)

    print("[run_nested_sbm] Hierarchy levels and group counts:")
    for i, level in enumerate(levels):
        print(f"  Level {i}: {np.unique(level).size} groups")

    # Select the first non-trivial level (more than 1 group), or fallback to level 0
    selected_level = next((i for i, lvl in enumerate(levels) if np.unique(lvl).size > 1), 0)
    selected_labels = levels[selected_level]

    print(f"[run_nested_sbm] Using level {selected_level} with {np.unique(selected_labels).size} groups.")

    return {
        "labels": selected_labels,
        "levels": levels,
        "order": None,
        "state": state
    }
