# Neurobridge: Bridging Functional and Anatomical Neural Connectivity through Dynamical Modeling

## Overview
**Neurobridge** aims to investigate how to reconcile structural and functional brain connectivity using network clustering and structural refinement techniques, as a preparatory step for dynamical modeling.

The focus is on:
- identifying ordered or hierarchical clusters of functionally coherent brain regions;
- using those partitions to refine structural connectivity matrices into equitable versions;
- laying the foundation for later integration into neural dynamical models.

## Objectives
- Load and preprocess functional and structural connectivity data.
- Apply functional clustering via Peixoto’s SBM framework (ordered and nested variants).
- Select a representative session using clustering consistency (Fowlkes–Mallows index).
- Derive an equitable structural matrix \( A_k \) compatible with the functional partition.
- Prepare the system for downstream dynamical simulation (not implemented here).

## Approach

### Tools
- **Peixoto's stochastic block model** via `graph-tool` (both ordered and nested SBM variants).
- **Baruzzi et al.’s structural refinement method**, enforcing equitable input across functionally clustered groups.

### Pipeline Steps
1. **Data Loading**: Import fMRI-based functional matrices and diffusion MRI structural matrices across 10 sessions.
2. **Functional Clustering**:
   - Compute one clustering per session.
   - Select the most representative session via average Fowlkes–Mallows similarity.
   - Store clustering assignments and visualize inferred community structure.
3. **Structural Matrix Averaging**:
   - Compute the average of the 10 structural matrices → \( A_0 \).
4. **Structural Refinement**:
   - Solve a convex optimization problem to find matrix \( A_k \) as close as possible to \( A_0 \), while ensuring equitable connectivity w.r.t. the functional clusters.
5. **Output**:
   - Save \( A_0 \), \( A_k \), and the functional partition.
   - Save visualizations of the input and clustered graphs.

## Dataset Format
- **Functional matrices**: session-level edgelists, 48x48 correlation matrices (after preprocessing).
- **Structural matrices**: session-level connectomes derived from diffusion tractography, also 48x48.

## References
- **Baruzzi, V.**, Lodi, M., Sorrentino, F., & Storace, M. (2023). *Bridging functional and anatomical neural connectivity through cluster synchronization*. Scientific Reports, 13, 22430.  
  [DOI: 10.1038/s41598-023-49746-2](https://doi.org/10.1038/s41598-023-49746-2)

- **Peixoto, T.P.** (2022). *Ordered community detection in directed networks*. Phys. Rev. E, 106(2), 024305.

## Installation

This project uses **Python** and **Conda** for environment and package management.

### Dependencies
- `graph-tool`
- `numpy`, `scikit-learn`, `matplotlib`, `cvxpy`, `seaborn`

### Setup

```bash
conda env create -f environment.yml
conda activate neurobridge
```

## Usage

1. **Download the data** from the open-neurodata portal:

   - [Functional matrices](http://open-neurodata.s3-website-us-east-1.amazonaws.com/Functional/HNU1-11-12-20-m2g-func/)
   - [Structural matrices](http://open-neurodata.s3-website-us-east-1.amazonaws.com/Diffusion/HNU1-8-27-20-m2g-native-csa-det/)

2. **Organize it** under:
   ```
   ./data/subject-<ID>/
       ├── functional/
       └── structural/
   ```

3. **Edit configuration** in `config/settings.json` to reflect:
   - input paths
   - graph type
   - clustering model 
   - thresholding strategy

4. **Run the pipeline**:

```bash
python scripts/run_pipeline.py
```

## Output
All results are saved under:
```
results/subject-<ID>/
```

Including:
- `graph_thresh-XX_directed.pdf`: raw functional graph
- `graph_nested_clustered.pdf`: graph with inferred clusters
- `A0_structural_mean.csv`: mean structural matrix
- `Ak_structural_equitable.csv`: refined equitable matrix
- `functional_partition.csv`: selected clustering labels

## Project Structure

```
src/
├── io/                  # loading and saving
├── graph/               # graph building
├── clustering/          # nested SBM
└── structural/          # A_k optimization
```

## License
TBD