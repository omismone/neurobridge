import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.io import load_config, load_functional_sessions, load_structural_sessions, save_matrix, save_labels
from src.graph import build_graph_from_matrix
from graph_tool.draw import graph_draw, prop_to_size
from src.clustering import run_nested_sbm
import matplotlib
from sklearn.metrics import fowlkes_mallows_score
from src.structural import is_equitable, compute_equitable_structure

# Load config file
config = load_config("config/settings.json")

# Get folder paths from config
functional_path = config["input_paths"]["functional_matrices_folder"]
structural_path = config["input_paths"]["structural_matrices_folder"]
output_dir = config["output_path"]

# Create output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load functional and structural matrices
functional_data = load_functional_sessions(functional_path)
structural_data = load_structural_sessions(structural_path)

# Get parameters from config
threshold = config["threshold"]["value"]
directed = config["graph"]["directed"]

# Run clustering on each functional matrix and select representative session
model = config["clustering"]["model"]
n_sessions = functional_data.shape[2]

partitions = []
graphs = []
states = []

for i in range(n_sessions):
    print(f"[run_pipeline] Processing session {i + 1} of {n_sessions}")
    mat = functional_data[:, :, i]
    G = build_graph_from_matrix(mat, threshold=threshold, directed=directed)
    graphs.append(G)

    result = run_nested_sbm(G, config)

    partitions.append(result["labels"])
    states.append(result["state"])

# Compute pairwise similarity (Fowlkes–Mallows)
n = len(partitions)
sim = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            sim[i, j] = fowlkes_mallows_score(partitions[i], partitions[j])

avg_sim = sim.mean(axis=1)
best_idx = np.argmax(avg_sim)

print(f"[run_pipeline] Selected representative session: {best_idx + 1} (mean similarity = {avg_sim[best_idx]:.3f})")

# Extract best graph and clustering result
G = graphs[best_idx]
clustering_result = {
    "labels": partitions[best_idx],
    "state": states[best_idx]
}

# Build output filename
threshold_pct = int(threshold * 100)
graph_type = "directed" if directed else "undirected"
filename = f"graph_thresh-{threshold_pct}_{graph_type}.pdf"
full_output_path = os.path.join(output_dir, filename)

# Draw and save the graph
graph_draw(G,
           pos=None,
           output_size=(600, 600),
           vertex_text=G.vertex_index,
           edge_pen_width=0.6,
           vertex_fill_color="#ffd000",
           output=full_output_path)

# Draw the clustered graph using SBM layout with scaled vertex labels
if clustering_result and clustering_result["state"] is not None:
    print("[run_pipeline] Drawing clustered graph with SBM layout and labels...")
    sbm_output_path = os.path.join(output_dir, f"graph_{model.lower()}_clustered.pdf")

    state = clustering_result["state"]
    g = state.g

    labels = g.new_vertex_property("int", vals=[i + 1 for i in range(g.num_vertices())])

    state.draw(
        edge_color=prop_to_size(g.ep.weight, power=1, log=True),
        ecmap=(matplotlib.cm.inferno, 0.6),
        eorder=g.ep.weight,
        edge_pen_width=prop_to_size(g.ep.weight, 1, 4, power=1, log=True),
        edge_gradient=[],
        vertex_text=labels,
        vertex_text_color="black",
        output=sbm_output_path
    )

# Compute average structural matrix
avg_structural = np.mean(structural_data, axis=2)
print("[run_pipeline] Computed average structural matrix A0")

# Check if partition is equitable
partition = clustering_result["labels"]
is_eq = is_equitable(avg_structural, partition)

if is_eq:
    print("[run_pipeline] Partition is already equitable on A0.")
    Ak = avg_structural
else:
    print("[run_pipeline] Partition is NOT equitable on A0. Solving for Ak...")
    Ak = compute_equitable_structure(avg_structural, partition)
    print("[run_pipeline] Optimization completed. Ak is now equitable.")

# Save results
save_matrix(avg_structural, output_dir, "A0_structural_mean")
save_matrix(Ak, output_dir, "Ak_structural_equitable")
save_labels(partition, output_dir, "functional_partition")
