#!/usr/bin/env python3

import pandas as pd


class EggNOGAnnotationParser: 
    """Class for parsing raw EggNOG annotations from a TSV file."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_annotations(self):
        """Load EggNOG annotations from a TSV file."""

        self.df = pd.read_csv(self.filepath, sep='\t', skiprows=4)
        print(f"Loaded {len(self.df)} EggNOG annotations from {self.filepath}")
        print(self.df)

    def parse_annotations(self):
        print(self.df.columns)
        #print(self.df[["GOs"]])

        columns_to_explode = ["eggNOG_OGs",
                              "GOs",
                              "COG_category",
                              "KEGG_ko",
                              "KEGG_Pathway",
                              "BRITE",
                              "PFAMs"]

        df_long = self.df

        for column in df_long.columns:
            df_long[column] = df_long[column].replace("-", pd.NA)
            if column in columns_to_explode:
                df_long[column] = df_long[column].str.split(",")
                df_long = df_long.explode(column)

        self.df = df_long

        print(df_long)

    def save_annotations(self):
        """Save the parsed annotations to a new TSV file."""
        output_filepath = self.filepath.replace(".tsv", "_parsed.tsv")
        self.df.to_csv(output_filepath, sep='\t', index=False)
        print(f"Parsed annotations saved to {output_filepath}")

    def run(self):
        self.load_annotations()
        self.parse_annotations()
        self.save_annotations()


def main():
    filepath = "data/test/dummy_eggnog_annotations.tsv"

    parser = EggNOGAnnotationParser(filepath)

    parser.run()

if __name__ == "__main__":
    main()
