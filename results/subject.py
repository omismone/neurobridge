import numpy as np


class Subject:
    def __init__(self, folder, subject_id):
        self.id = subject_id
        self.functionals = self._load_all_functional_sessions(folder, subject_id)
        self.structurals = self._load_all_structural_sessions(folder, subject_id)

    def _load_all_functional_sessions(self, folder, subject_id):
        sessions = []
        for session in range(1, 11):
            path = f'{folder}/functional/sub-00{subject_id}_ses-{session}_func_HarvardOxfordcort-maxprob-thr25_space-MNI152NLin6_res-2x2x2.nii.gz_edgelist.csv'
            sessions.append(self._load_mat(path))
        return np.stack(sessions, axis=2)
    
    def _load_all_structural_sessions(self, folder, subject_id):
        sessions = []
        for session in range(1, 11):
            path = f'{folder}/structural/sub-00{subject_id}_ses-{session}_dwi_HarvardOxfordcort-maxprob-thr25_space-MNI152NLin6_res-2x2x2_connectome.csv'
            sessions.append(self._load_mat(path, int))
        return np.stack(sessions, axis=2)
    
    def _load_mat(self, path, val_type = float):
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
