from graph_tool.all import *
from scipy.io import loadmat


def run(functional_mat_path, results_path):
    data = loadmat(functional_mat_path)
    mat = data['matrices']
    mat = mat[:, :, 0]                                          # load only the first session and first subject
    size = mat.shape[0]  # should be 116

    g = Graph(directed=True)
    g.add_vertex(size)
    weights = g.new_ep("double")
    threshold = 0.33
    for i in range(size):
        for j in range(size):
            if abs(mat[i, j]) > threshold:
                edge = g.add_edge(g.vertex(i), g.vertex(j))
                weights[edge] = mat[i, j]
    g.ep["weight"] = weights

    # ------------------------------
    # Run the nested SBM to obtain hierarchical partitions
    # ------------------------------
    state = NestedBlockState(g)  # initialize nested SBM

    collected_partitions = []
    # callback function that adds the current partition to the list
    def collect_partitions(s):
        collected_partitions.append(s.get_bs())

    # run additional sweeps and collect partitions via the callback
    mcmc_equilibrate(state, force_niter=10000, mcmc_args=dict(niter=10), callback=collect_partitions)

    # disambiguate partitions and obtain marginals over all hierarchical levels
    pmode = PartitionModeState(collected_partitions, nested=True, converge=True)
    pv = pmode.get_marginal(g)  # vertex marginals at all levels

    # obtain consensus (maximum a posteriori) nested partition
    state = state.copy(bs=pmode.get_max_nested())

    # ------------------------------
    # Visualize the hierarchical partition
    # ------------------------------
    state.draw(vertex_shape="pie",
               vertex_pie_fractions=pv,
               output_size=(1600, 1600),
               output= results_path + "functional_connectivity.svg")