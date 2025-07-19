import numpy as np
import os

def save_matrix(matrix: np.ndarray, path: str, name: str):
    """
    Saves a matrix to CSV at the specified location.

    Parameters:
        matrix (np.ndarray): 2D array to save
        path (str): directory where to save
        name (str): filename (without extension)
    """
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, f"{name}.csv")
    np.savetxt(full_path, matrix, delimiter=",")
    print(f"[save] Saved matrix to {full_path}")


def save_labels(labels: np.ndarray, path: str, name: str = "labels"):
    """
    Saves clustering labels to CSV.

    Parameters:
        labels (np.ndarray): 1D array of labels
        path (str): directory where to save
        name (str): filename (default = "labels")
    """
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, f"{name}.csv")
    np.savetxt(full_path, labels, delimiter=",", fmt="%d")
    print(f"[save] Saved labels to {full_path}")
