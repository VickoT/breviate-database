#!/usr/bin/env python3
import pandas as pd
from sqlalchemy import create_engine


class EggNOGAnnotationParser: 
    """
    Class for parsing raw EggNOG annotations from a TSV file.

    This class handles loading, parsing, and exporting EggNOG annotations
    to a PostgreSQL database. It processes the annotations to ensure
    consistent formatting and handles multiple annotations in a single
    cell by exploding lists into separate rows.

    Attributes:
        filepath (str): Path to the EggNOG annotations TSV file.
        df (pd.DataFrame): DataFrame containing the loaded annotations.

    Methods:
        load_annotations(): Load annotations from the TSV file.
        parse_annotations(): Parse and explode the annotations DataFrame.
        save_annotations(): Save the parsed annotations to a new TSV file.
        export_to_postgres(table_name): Export the DataFrame to a PostgreSQL table.
        run(): Execute the full parsing and exporting workflow.

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_annotations(self):
        """Load EggNOG annotations from a TSV file."""

        self.df = pd.read_csv(self.filepath, sep='\t', skiprows=4)

        # Make colnames are consistent with the schema format
        self.df = self.df.rename(columns={"#query": "query_id"})
        self.df.columns = [col.lower() for col in self.df.columns]

        print(f"Loaded {len(self.df)} EggNOG annotations from {self.filepath}")

    def parse_annotations(self):
        """Parse and explode the annotations DataFrame."""

        df_long = self.df.copy()

        # Replace "-" with NaN globally
        df_long.replace("-", pd.NA, inplace=True)

        columns_to_explode = [
            "eggnog_ogs",
            "gos",
            "cog_category",
            "kegg_ko",
            "kegg_pathway",
            "brite",
            "pfams"]


        # Explode only the relevant columns
        for column in columns_to_explode:
            if column in df_long.columns:
                df_long[column] = df_long[column].str.split(",")
                df_long = df_long.explode(column)

        self.df = df_long
        print(f"Parsed annotations into long format with {len(self.df)} rows")
        print(df_long)

    def save_annotations(self):
        """Save the parsed annotations to a new TSV file."""
        output_filepath = self.filepath.replace(".tsv", "_parsed.tsv")
        self.df.to_csv(output_filepath, sep='\t', index=False)
        print(f"Parsed annotations saved to {output_filepath}")

    def export_to_postgres(self, table_name="eggnog_annotations"):
        engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
        self.df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Annotations exported to PostgreSQL table '{table_name}'")

    def run(self):
        self.load_annotations()
        self.parse_annotations()
        self.save_annotations()
        self.export_to_postgres()


def main():
    filepath = "data/test/dummy_eggnog_annotations.tsv"
    parser = EggNOGAnnotationParser(filepath)
    parser.run()

if __name__ == "__main__":
    main()
