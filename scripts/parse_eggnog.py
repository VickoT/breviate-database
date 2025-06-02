#!/usr/bin/env python3

import pandas as pd

def load_eggnog_annotaions(filepath):
    """Load EggNOG annotations from a TSV file."""
    df = pd.read_csv(filepath, sep='\t', comment='#')
    print(f"Loaded {len(df)} EggNOG annotations from {filepath}")
    return df


def main():
    filepath = "data/test/dummy_eggnog_annotations.tsv"
    df = load_eggnog_annotaions(filepath)

    print(df)

if __name__ == "__main__":
    main()
