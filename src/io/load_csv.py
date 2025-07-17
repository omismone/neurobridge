import os
import numpy as np

def load_functional_sessions(folder: str) -> np.ndarray:
    sessions = []
    for session in range(1, 11):
        filename = f"sub-0025452_ses-{session}_func_HarvardOxfordcort-maxprob-thr25_space-MNI152NLin6_res-2x2x2.nii.gz_edgelist.csv"
        path = os.path.join(folder, filename)
        sessions.append(_load_matrix_from_edgelist(path))
    return np.stack(sessions, axis=2)

def load_structural_sessions(folder: str) -> np.ndarray:
    sessions = []
    for session in range(1, 11):
        filename = f"sub-0025452_ses-{session}_dwi_HarvardOxfordcort-maxprob-thr25_space-MNI152NLin6_res-2x2x2_connectome.csv"
        path = os.path.join(folder, filename)
        sessions.append(_load_matrix_from_edgelist(path, val_type=int))
    return np.stack(sessions, axis=2)

def _load_matrix_from_edgelist(path: str, val_type=float) -> np.ndarray:
    entries = []
    max_index = 0
    with open(path, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            parts = line.strip().split()
            i, j, v = int(parts[0]) - 1, int(parts[1]) - 1, val_type(float(parts[2]))
            entries.append((i, j, v))
            max_index = max(max_index, i, j)
    mat = np.zeros((max_index + 1, max_index + 1), dtype=val_type)
    for i, j, v in entries:
        mat[i, j] = v
        mat[j, i] = v
    return mat
