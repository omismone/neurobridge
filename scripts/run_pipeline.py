import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.io.load_config import load_config
from src.io.load_csv import load_functional_sessions, load_structural_sessions

# Load config file
config = load_config("config/settings.json")

# Get folder paths from config
functional_path = config["input_paths"]["functional_matrices_folder"]
structural_path = config["input_paths"]["structural_matrices_folder"]

# Load functional and structural matrices
functional_data = load_functional_sessions(functional_path)
structural_data = load_structural_sessions(structural_path)

