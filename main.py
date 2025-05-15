from scripts import functional_partitioning


FUNCTIONAL_MAT_PATH = './data/matrices_func.mat'
STRUCTURAL_MAT_PATH = './data/matrices_struct.mat'
RESULTS_PATH = './results/'

def main():
    functional_partitioning.run(FUNCTIONAL_MAT_PATH, RESULTS_PATH)

if __name__ == "__main__":
    main()
