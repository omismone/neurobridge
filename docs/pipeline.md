# Analytical Pipeline: Functional Clustering and Structural Refinement

This pipeline outlines the concrete steps followed in the **Neurobridge** project to identify clusters of functionally coherent brain regions and integrate structural data through equitable refinement of anatomical connectivity.

---

## **Step 1: Data Preprocessing**

**Input**: CSV fMRI data from a public dataset (HNU1)  
**Output**: Session-wise functional connectivity matrices

- Load 10 functional matrices (one per session)
- Each matrix corresponds to a 48x48 correlation matrix across brain regions

---

## **Step 2: Functional Clustering**

**Input**: One graph per functional session  
**Output**: Set of node partitions, one per session

- Build a graph from each functional matrix using a percentile-based threshold
- Run community detection (Nested SBM) on each graph
- Store resulting group assignments per session

---

## **Step 3: Session Selection**

**Input**: 10 sets of group assignments (one per session)  
**Output**: Representative session and its functional partition

- Compute pairwise Fowlkes–Mallows similarity between all session partitions
- Select the session with the highest mean similarity to the others
- Use its graph and partition as the functional reference

---

## **Step 4: Graph Visualization**

**Input**: Functional graph and clustering result  
**Output**: PDF visualizations

- Plot the raw functional graph after thresholding
- Plot the clustered graph using graph-tool's state-drawing and inferred layout
- Include vertex labels and edge weights

---

## **Step 5: Structural Integration**

**Input**: 10 structural matrices (connectomes) and functional partition  
**Output**: Equitable matrix \( A_k \)

- Average the 10 structural matrices to obtain \( A_0 \)
- Solve a convex optimization problem to find \( A_k \), the closest symmetric matrix to \( A_0 \) that is equitable w.r.t. the functional partition
- Save both \( A_0 \) and \( A_k \) to disk

---

## **Outputs**

All outputs are saved in `results/subject-<ID>/`:

- `graph_thresh-XX_directed.pdf`: Raw functional graph
- `graph_nested_clustered.pdf`: Clustered graph after SBM
- `functional_partition.csv`: Final partition used for structural refinement
- `A0_structural_mean.csv`: Mean structural matrix across sessions
- `Ak_structural_equitable.csv`: Optimized equitable matrix

---

## **Tools & Libraries**

- **Data Handling**:  
  - `numpy`, `pandas`, `cvxpy`

- **Graph Construction & Clustering**:  
  - `graph-tool` — for graph representation and stochastic block model inference

- **Clustering Evaluation**:  
  - `scikit-learn` — for Fowlkes–Mallows index

- **Visualization**:  
  - `matplotlib`, `graph-tool`

---

## Notes
This pipeline prepares the necessary inputs for the final phase of the Baruzzi et al. framework: dynamic simulation and synchronization validation — not implemented here.