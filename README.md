# Neurobridge: Bridging Functional and Anatomical Neural Connectivity through Dynamical Modeling

## Overview
The **neurobridge** project aims to investigate an approach to reconcile structural and functional neural 
connectivity to design dynamical models of the cerebral cortex. The goal is to use both functional and anatomical data to create a model that can simulate the dynamics of the brain and provide insights into its connectivity.

This project involves using both **graph theory** and **machine learning** tools to analyze brain connectivity data and apply dynamic modeling techniques to represent how different regions of the brain interact with each other.

## Objectives
- Import and pre-process biological data on structural and functional connectivity.
- Design a dynamical network model to reproduce biological data features.
- Validate the designed model.

## Approach
The project will use existing tools and algorithms for connectivity analysis:
1. **Peixoto's clustering algorithm** using the [graph-tool](https://graph-tool.skewed.de) library.
2. **Baruzzi's method** for integrating structural data and functional data.

The dataset provided contains two matrices:
- **Functional Matrix (`matrices.mat`)**: A correlation matrix between 116 brain regions (116x116) across 30 patients (300 sessions in total).
- **Connectivity Matrix (`matrices_HNU1.mat`)**: A structural matrix representing the number of nerve bundles connecting the regions.

## References
- Baruzzi, V., Lodi, M., Sorrentino, F., & Storace, M. (2023). *Bridging functional and anatomical neural connectivity through cluster synchronization*. Scientific Reports, 13, 22430. DOI: [10.1038/s41598-023-49746-2](https://doi.org/10.1038/s41598-023-49746-2)
- Peixoto, T.P. (2022). *Ordered community detection in directed networks*. Phys. Rev. E, 106(2), 024305.

## Requirements
This project uses **Python** and **Conda** for environment management. The required dependencies are listed below.

### Dependencies:
- **graph-tool** (for graph-based algorithms)

### Setting Up the Environment:
1. Create a new Conda environment using the `environment.yml` file:
    ```bash
    conda env create -f environment.yml
    ```

2. Activate the environment:
    ```bash
    conda activate neurobridge
    ```

## Usage
TBD

## Documentation
- The meeting logs and additional documentation can be found in the **`docs/`** folder, including:
    - **log.md**: A log of all meeting discussions, with a detailed introduction to the project.

## Future Improvements
TBD

## License
TBD
