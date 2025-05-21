from scripts import functional_partitioning
from scripts.subject import Subject
import numpy as np


SUBJECT_ID = '25452'

def main():
    s = Subject(f"./data/subject-{SUBJECT_ID}", SUBJECT_ID)
    np.set_printoptions(suppress=True)
    print(s.functionals[:,:,9])
    pass

if __name__ == "__main__":
    main()
