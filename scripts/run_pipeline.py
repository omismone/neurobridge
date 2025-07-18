import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.io import load_config, load_functional_sessions, load_structural_sessions
from src.graph import build_graph_from_matrix
from graph_tool.draw import graph_draw, prop_to_size
from src.clustering import run_osbm, run_nested_sbm
import matplotlib

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

# Aggregate functional scans
avg_functional = np.mean(functional_data, axis=2)

# Get parameters from config
threshold = config["threshold"]["value"]
directed = config["graph"]["directed"]

# Build graph
G = build_graph_from_matrix(avg_functional, threshold=threshold, directed=directed)

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

# Clustering
model = config["clustering"]["model"]
clustering_result = None

if model == "DC-OSBM":
    clustering_result = run_osbm(G, config)
elif model == "nested":
    clustering_result = run_nested_sbm(G, config)
else:
    raise ValueError(f"Invalid clustering model '{model}'. Supported values: 'DC-OSBM', 'nested'.")

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

