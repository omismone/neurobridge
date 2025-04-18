# LAB 24: BRIDGING FUNCTIONAL AND ANATOMICAL NEURAL CONNECTIVITY THROUGH DYNAMICAL MODELING

## Objective
The aim of this lab is to investigate an approach to reconcile information about structural and functional connectivity to design dynamical models of the cerebral cortex.

## Rationale
The dynamics of the brain results from the complex interplay of several neural populations and is affected by both the individual dynamics of these areas and their connection structure. Hence, a fundamental challenge is to derive models of the brain that reproduce both structural and functional features measured experimentally.

## Task
Use MATLAB and its toolboxes to 

I. import and pre-process biological data on structural and functional connectivity

II. select an atlas and parcellate our data accordingly

III. design a dynamical network model able to reproduce some features of the biological data

IV. validate the designed model

### References
V. Baruzzi, M. Lodi, F. Sorrentino, M. Storace, "Bridging functional and anatomical neural connectivity through cluster synchronization," Scientific Reports, vol. 13, p. 22430, Dec. 2023, doi: 10.1038/s41598-023-49746-2.

T.P. Peixoto, "Ordered community detection in directed networks", Phys. Rev. E, 106 (2) (2022), Article 024305

## Deliverable
Documented code and a small presentation to let them see the workflow and how the code works.

## Project
1. ML tool for connectivity identification available in the literature: I share both the tool [webpage](https://graph-tool.skewed.de) and the reference paper (Peixoto.pdf)

~~2. ad hoc tool, clusterization connectivity, difficult parameters of this tool, machine learning to find good parameters~~

~~3. new data online, parcellation of data, spatial distribution too dense, we have to resample data, open mind for the programming language~~ 

## Meeting 1 - 27/03/2025

Use Peixoto's tool for clustering and Baruzzi's method (which shares the dataset with this project) for the second part on structural data integration.

The dataset includes two matrices:
- `matrices.mat`: functional matrix
- `matrices_HNU1.mat`: connectivity matrix

The dimensions are 116x116x300. The 116x116 dimensions represent brain regions (see the [supplemental material](https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-49746-2/MediaObjects/41598_2023_49746_MOESM1_ESM.pdf) of Baruzzi's paper on the publisher's website), and the z-axis indicates the session and the patient: for each patient (30), 10 sessions were conducted. From z=1 to z=10, we have the 10 sessions of the first patient; from z=11 to z=20, those of the second patient, and so on.

The functional matrix indicates the correlation between brain regions. For example, row 1, column 3 indicates the correlation between region 1 and region 3. Being a correlation matrix, the values range from -1 to 1.

The structural matrix, on the other hand, is constructed by only tracking the **number** of nerve bundles connecting the regions. For this reason, it is normalized.

It may be necessary to convert the `.mat` files into formats readable by Python.

## Meeting 2 - 03/04/2025

We need a model for each patient, the goal is to provide to a patient coming with a fMRI a description of his brain.

Ignore "importConnectivityMatrix" and "Readme" uploaded on teams, they were redundant info.

Connectivity matrix _e_ constraints are only maximum constraints, not both minimum and maximum: we need to have __at least__ $e_{ij}$ connections between the node _i_ and the node _j_.

The implementation of Peixoto's model is already done in the _graph\_tool_, I only need to use it. Start with one matrix and one patient, a following issue will be the integration of different matrices for one patient, since the tool works with only one.

## Meeting 3 - 10/04/2025

Review the theory of the Monte Carlo algorithm and reread Baruzzi's paper.

Continue in the same way as Baruzzi post-clusterization, using the new material loaded. The structural matrix must allow the clusterization found with the functional matrix: neurons belonging to the same cluster should have similar characteristics (something like: the weighted sum of the inputs of two neurons from the same cluster should be equal), the structural matrix should be adjusted to ensure this.

Make sure to integrate the various sessions of the same patient.

## To Do
- Adjust the application of Peixoto's algorithm using the graph tool and compare it with Baruzzi's results.

### See
- SBM
- MCMC
- Baruzzi


## Questions
1.  
