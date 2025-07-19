import numpy as np
from graph_tool.all import minimize_nested_blockmodel_dl

def run_nested_sbm(graph, config):
    """
    Runs Nested SBM on the given graph.
    Selects the first level with more than 1 group.

    Returns:
        dict: {
            "labels": node→group array,
            "levels": list of np.ndarray for all levels,
            "order": None,
            "state": graph-tool BlockState
        }
    """
    # print("[run_nested_sbm] Running nested SBM inference...")
    state = minimize_nested_blockmodel_dl(graph)

    levels = []
    for level in range(len(state.get_levels())):
        lbl = state.project_level(level).get_blocks().a.copy()
        levels.append(lbl)
        if np.unique(lbl).size == 1:  # stop if collapsed
            break

    level_summary = [f"L{idx}:{np.unique(lbl).size}" for idx, lbl in enumerate(levels)]
    print(f"    Hierarchy levels: {' | '.join(level_summary)}")


    selected_level = next((i for i, lbl in enumerate(levels) if np.unique(lbl).size > 1), 0)
    selected_labels = levels[selected_level]
    print(f"    → Selected level {selected_level} with {np.unique(selected_labels).size} groups")


    return {
        "labels": levels[selected_level],
        "levels": levels,
        "order": None,
        "state": state
    }
