# Analytical Pipeline: Ordered Functional Clustering (Pre-structural Phase)

This pipeline outlines the concrete steps for identifying ordered clusters of functionally coherent brain regions using Peixoto's Ordered Stochastic Block Model (OSBM), stopping before the structural refinement or dynamical modeling.


## **Step 1: Data Preprocessing**

**Input**: CSV fMRI data from a public dataset (HNU1)  
**Output**: Functional connectivity matrices

- **Aggregate Scans**: Compute the mean correlation matrix or select a representative scan using clustering similarity metrics (as in Baruzzi et al.).


## **Step 2: Graph Construction**

**Input**: Correlation matrix $X$  
**Output**: Directed graph representation $G$

- **Construct Graph from Correlation Matrix**:
  - Threshold $X$ to remove weak or spurious correlations (e.g., retain top 20% of values)
  - Represent $X$ as a directed, weighted adjacency matrix $A_{ij}$


## **Step 3: Ordered Community Detection (Peixoto, 2022)**

**Input**: Graph $G$  
**Output**: Ordered partition of ROIs (clusters + rank)

1. **Run Ordered Stochastic Block Model (OSBM)**
   - Use `graph-tool` for nonparametric Bayesian inference
   - Model: Degree-corrected, ordered SBM (DC-OSBM)

2. **MCMC Inference**
   - Sample the posterior distribution over group assignments and orderings
   - Find the partition $b^*$ that minimizes the description length:
     $$ \Sigma(A, b) = -\log P(A | b) - \log P(b) $$

3. **Extract Ordered Clustering**
   - Assign nodes to groups $C_1, \dots, C_k$
   - Infer a ranking/order over the groups
   - Store the group-to-group edge preferences $e_{rs}$ (directional pattern)


## **Step 4: Cluster Stability and Granularity Analysis**

**Input**: MCMC samples from OSBM  
**Output**: Robust multi-resolution cluster hierarchy

1. **Compute Marginal Rank Distributions**
   - Estimate rank uncertainty $\pi_i(r)$ for each node

2. **Identify Stable Cluster Levels**
   - Use similarity indices (e.g., Fowlkes–Mallows index across multiple scans)
   - Select resolution levels $\ell_k^*$ with high intra-session consistency

3. **Export Clusters for Further Use**
   - Save representative partitions at selected granularities $\ell_k^*$


## **Step 5: Summary and Data Export**

**Output**: Final functional parcellations, cluster rankings, group-level adjacency matrix

- Ordered clustering: list of node → cluster + rank assignment
- Group interaction matrix $e_{rs}$
- Node-level rank uncertainty estimates
- Dendrogram or clustering visualization


## **Tools & Libraries**

- **Data Handling**:  
  - `pandas`, `numpy` — for CSV import and manipulation

- **Graph Construction & Manipulation**:  
  - `networkx` or `graph-tool` (preferred for Peixoto model compatibility)

- **Community Detection / Inference**:  
  - `graph-tool` — implements Peixoto’s ordered SBM with MCMC

- **Clustering Evaluation / Similarity Metrics**:  
  - `scikit-learn` — for Fowlkes–Mallows index and other metrics

- **Visualization**:  
  - `matplotlib`, `seaborn`, `plotly` — for matrix heatmaps, dendrograms, rank distributions

- **(Optional) Scientific Computing**:  
  - `scipy`, `joblib` — for parallelism and numerical stability

