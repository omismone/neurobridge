import graph_tool.all as gt
import numpy as np
from scipy.sparse import lil_matrix
import matplotlib.pyplot as plt

class Analyzer:
    @staticmethod
    def functional_partitionate(subject, session):
        session_idx = session - 1
        mat = subject.structurals[:, :, session_idx]

        # Normalize matrix to [0,1]
        norm_mat = mat.copy()
        norm_mat = norm_mat / norm_mat.max() if norm_mat.max() != 0 else norm_mat

        # Plot full normalized connectivity matrix
        fig, ax = plt.subplots(figsize=(8,8))
        cax = ax.imshow(norm_mat, cmap='inferno', interpolation='nearest')
        ax.set_title("Connectivity matrix")
        plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
        plt.savefig("./results/connectivity_matrix.png", dpi=300, bbox_inches='tight')
        plt.close(fig)


        weights = mat[np.triu_indices_from(mat, k=1)]
        threshold = np.percentile(weights[weights > 0], 70)

        # Filtro: mantieni solo pesi >= soglia
        mat = np.where(mat >= threshold, mat, 0)

        sparse_mat = lil_matrix(mat)
        g = gt.Graph(sparse_mat, directed=False)
        ew = g.ep["weight"]

        hoa_labels = [
            "FP","IC","SFG","MFG","IFGpt","IFGpo","PrG","TP",
            "STGad","STGpd","MTGad","MTGpd","MTGtp","ITGad","ITGpd","ITGtp",
            "PostG","SPL","SGad","SGpd","AG","LOCsd","LOCid","IcC",
            "FMC","JLC","SC","PcG","CGad","CGpd","PC","CC",
            "FOrC","PGad","PGpd","LG","TFCad","TFCpd","TOFC","OFG",
            "FOpC","COC","POC","PP","HG","PT","ScC","OP"
        ]

        v_label = g.new_vertex_property("string")
        for v in g.vertices():
            v_label[v] = hoa_labels[int(v)]
        g.vp["label"] = v_label

        n = g.num_vertices()
        pos = g.new_vertex_property("vector<double>")
        for i, v in enumerate(g.vertices()):
            angle = 2 * np.pi * i / n
            pos[v] = (np.cos(angle), np.sin(angle))

        weights_nonzero = np.array([ew[e] for e in g.edges()])
        p33 = np.percentile(weights_nonzero, 33)
        p66 = np.percentile(weights_nonzero, 66)

        e_color = g.new_edge_property("vector<float>")  # RGB color

        for e in g.edges():
            w = ew[e]
            if w <= p33:
                e_color[e] = (1, 1, 0, 1)      # giallo (RGBA)
            elif w <= p66:
                e_color[e] = (1, 0.5, 0, 1)    # arancione
            else:
                e_color[e] = (1, 0, 0, 1)      # rosso

        gt.graph_draw(
            g,
            pos=pos,
            vertex_text=g.vp.label,
            edge_color=e_color,
            vertex_fill_color="white",
            vertex_font_size=10,
            edge_pen_width=gt.prop_to_size(ew, mi=1, ma=4, power=1, log=True),
            output="./results/graph.png"
        )


