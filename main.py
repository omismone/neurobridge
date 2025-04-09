from scripts import functional_partitioning


FUNCTIONAL_MAT_PATH = './data/matrices.mat'
STRUCTURAL_MAT_PATH = './data/matrices_HNU1.mat'
RESULTS_PATH = './results/'

def main():
    functional_partitioning.run(FUNCTIONAL_MAT_PATH, RESULTS_PATH)

if __name__ == "__main__":
    main()
