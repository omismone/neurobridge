from graph_tool.all import *
from graph_tool.inference import mcmc_equilibrate
from scipy.io import loadmat
import numpy as np

def run(functional_mat_path, results_path):
    data = loadmat(functional_mat_path)
    mat = data['matrices']
    NS = 30  # number of subjects
    NSS = int(mat.shape[2] / NS)  # sessions per subject
    size = mat.shape[0]

    p1 = Graph(directed=True) # patient 1
    p1.add_vertex(size)
    weights = p1.new_ep("double")
    threshold = 0.66
    for session in range(NSS):
        for i in range(size):
            for j in range(size):
                if abs(mat[i, j, session]) >= threshold:
                    e = p1.add_edge(i, j)
                    weights[e] = mat[i, j, session]
    p1.ep["weight"] = weights

    ew = contract_parallel_edges(p1, weights)
    state = NestedBlockState(p1, base_type=RankedBlockState, state_args=dict(eweight=ew))
    mcmc_equilibrate(state, wait=1000, mcmc_args=dict(beta=np.inf, niter=100))

    # positions
    pos = p1.new_vp("vector<double>")
    angles = np.linspace(0, 2*np.pi, size, endpoint=False)
    for v in p1.vertices():
        pos[v] = (np.cos(angles[int(v)]), np.sin(angles[int(v)]))
    #colors
    ec = p1.new_ep("vector<double>")
    for e in p1.edges():
        v = ew[e]
        ec[e] = [1.0, 1.0, 0.0, 1.0] if v < 0.77 else [1.0, 0.5, 0.0, 1.0] if v < 0.88 else [1.0, 0.0, 0.0, 1.0]

    # names (HOA S1, 48 regions)
    labels = [
        "FP","IC","SFG","MFG","IFGpt","IFGpo","PrG","TP",
        "STGad","STGpd","MTGad","MTGpd","MTGtp","ITGad","ITGpd","ITGtp",
        "PostG","SPL","SGad","SGpd","AG","LOCsd","LOCid","IcC",
        "FMC","JLC","SC","PcG","CGad","CGpd","PC","CC",
        "FOrC","PGad","PGpd","LG","TFCad","TFCpd","TOFC","OFG",
        "FOpC","COC","POC","PP","HG","PT","ScC","OP"
    ]
    vt = p1.new_vp("string")
    for v in p1.vertices(): vt[v] = labels[int(v)]

    state.levels[0].draw(
        pos=pos,
        vertex_fill_color=[1, 1, 1, 1],
        vertex_pen_width=1,
        vertex_size=15,
        vertex_text=vt,
        vertex_font_size=10,
        vertex_text_color=[0, 0, 0, 1],
        edge_color=ec,
        edge_pen_width=prop_to_size(ew, 1, 5),
        output_size=(1000, 1000),
    )



