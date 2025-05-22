import graph_tool.all as gt
import numpy as np
from scipy.sparse import lil_matrix
import matplotlib.pyplot as plt

class Analyzer:
    @staticmethod
    def structuralAnalysis(subject, folder):
        """
        Performs structural connectivity analysis and visualization on the subject's data.

        Steps:
        1. Compute the mean structural connectivity matrix across the third dimension.
        2. Normalize the matrix by its maximum value.
        3. Plot and save the connectivity matrix heatmap.
        4. Threshold the matrix to retain only the top 30% strongest connections.
        5. Convert the thresholded matrix into a sparse graph-tool graph.
        6. Assign region labels (hoa_labels) to vertices.
        7. Arrange vertices on a circle for visualization.
        8. Color edges based on weight percentiles (low=yellow, medium=orange, high=red).
        9. Draw and save the connectogram graph.

        Parameters:
        - subject: Object containing structural connectivity data in subject.structurals
        - folder: Output folder path for saving plots
        """
        mat = subject.structurals[:, :, :].mean(axis=2)
        mat = mat / mat.max() if mat.max() != 0 else mat

        ## connectivity matrix
        fig, ax = plt.subplots(figsize=(8,8))
        cax = ax.imshow(mat, cmap='inferno', interpolation='nearest')
        ax.set_title("Connectivity matrix")
        plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
        plt.savefig(f"{folder}/connectivity_matrix.png", dpi=300, bbox_inches='tight')
        plt.close(fig)

        ## connectogram
        weights = mat.flatten()
        mat = np.where(mat >= np.percentile(weights[weights > 0], 70), mat, 0) # plot only the 30% more significative

        sparse_mat = lil_matrix(mat)
        g = gt.Graph(sparse_mat, directed=False)
        ew = g.ep["weight"]

        # vertex names
        hoa_labels = ["FP","IC","SFG","MFG","IFGpt","IFGpo","PrG","TP","STGad","STGpd","MTGad","MTGpd","MTGtp","ITGad","ITGpd","ITGtp","PostG","SPL","SGad","SGpd","AG","LOCsd","LOCid","IcC","FMC","JLC","SC","PcG","CGad","CGpd","PC","CC","FOrC","PGad","PGpd","LG","TFCad","TFCpd","TOFC","OFG","FOpC","COC","POC","PP","HG","PT","ScC","OP"]
        v_label = g.new_vertex_property("string")
        for v in g.vertices():
            v_label[v] = hoa_labels[int(v)]
        g.vp["label"] = v_label

        # vertex positions
        n = g.num_vertices()
        pos = g.new_vertex_property("vector<double>")
        for i, v in enumerate(g.vertices()):
            angle = 2 * np.pi * i / n
            pos[v] = (np.cos(angle), np.sin(angle))

        # edges color
        weights_nonzero = np.array([ew[e] for e in g.edges() if ew[e] > 0])
        e_color = g.new_edge_property("vector<float>")
        for e in g.edges():
            w = ew[e]
            e_color[e] = (1, 1, 0, 1) if w <= np.percentile(weights_nonzero, 33) else (1, 0.5, 0, 1) if w <= np.percentile(weights_nonzero, 66) else (1, 0, 0, 1)
   
        gt.graph_draw(g, pos=pos, vertex_text=g.vp.label, edge_color=e_color, vertex_fill_color="white", vertex_font_size=10, edge_pen_width=gt.prop_to_size(ew, mi=1, ma=4, power=1, log=True), output=f"{folder}/graph.png")


    @staticmethod
    def functional_partitionate(subject, session):
        pass


