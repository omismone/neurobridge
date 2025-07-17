import numpy as np
from graph_tool import Graph

def build_graph_from_matrix(matrix: np.ndarray, threshold: float = 0.8, directed: bool = True) -> Graph:
    # Copy input to avoid side effects
    mat = matrix.copy()

    # Threshold: retain only values above percentile
    cutoff = np.percentile(mat, threshold * 100)
    mat[mat < cutoff] = 0.0

    # Create graph-tool graph
    N = mat.shape[0]
    g = Graph(directed=directed)
    g.add_vertex(N)

    weights = g.new_edge_property("double")

    for i in range(N):
        for j in range(N):
            if mat[i, j] > 0:
                e = g.add_edge(i, j)
                weights[e] = mat[i, j]

    g.edge_properties["weight"] = weights
    return g
