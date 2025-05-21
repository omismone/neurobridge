from scripts.analyzer import Analyzer
from scripts.subject import Subject


def main():
    SUBJECT_ID = '25452'

    s = Subject(f"./data/subject-{SUBJECT_ID}", SUBJECT_ID)

    Analyzer.functional_partitionate(s, session=1)

    pass

if __name__ == "__main__":
    main()
