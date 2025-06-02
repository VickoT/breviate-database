#!/usr/bin/env python3

import pandas as pd


class EggNOGAnnotaionParser: 
    """Class for parsing raw EggNOG annotations from a TSV file."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

def load_eggnog_annotations(filepath):
    """Load EggNOG annotations from a TSV file."""
    df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
    print(f"Loaded {len(df)} EggNOG annotations from {filepath}")
    return df

def parse_eggnog_annotations(df):
    df_clean = df[[0, 1, 2, 3, 4, 6, 10, 11, 12, 16]].copy()
    df_clean.columns = [
    "query_id", "seed_ortholog", "evalue", "score",
    "eggnog_OGs", "description", "go_terms",
    "kegg_pathways", "pfam_domains", "cog_category"
    ]
    return df_clean

def convert_to_NF1(df):

    muliti_valued_cols = ["go_terms", "kegg_pathways",
                          "pfam_domains", "cog_category"]
    return df.columns



def main():
    filepath = "data/test/dummy_eggnog_annotations.tsv"
    df = load_eggnog_annotations(filepath)
    df_parsed = parse_eggnog_annotations(df)

    df_parsed.to_csv("data/test/parsed_eggnog_annotations.tsv",
                     sep='\t',
                     index=False)

    print(convert_to_NF1(df_parsed))





if __name__ == "__main__":
    main()
