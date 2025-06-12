#!/usr/bin/env python3
import pandas as pd
from models import EggnogQuery, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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

    def export_to_postgres(self):
        engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        unique_df = self.df.drop_duplicates(subset='query_id')

        for _, row in unique_df.iterrows():
            entry = EggnogQuery(
                query_id=row['query_id'],
                seed_ortholog=row.get('seed_ortholog') if pd.notna(row.get('seed_ortholog')) else None,
                evalue=row.get('evalue') if pd.notna(row.get('evalue')) else None,
                score=row.get('score') if pd.notna(row.get('score')) else None,
                max_annot_lvl=row.get('max_annot_lvl') if pd.notna(row.get('max_annot_lvl')) else None,
                description=row.get('description') if pd.notna(row.get('description')) else None,
                preferred_name=row.get('preferred_name') if pd.notna(row.get('preferred_name')) else None,
            )
            session.add(entry)

        session.commit()
        session.close()
        print("Annotations exported to PostgreSQL database")


    def run(self):
        self.load_annotations()
        #self.parse_annotations()
        self.export_to_postgres()


def main():
    filepath = "data/eggnog.emapper.annotations"
    #filepath = "data/test/dummy_eggnog_annotations.tsv"
    parser = EggNOGAnnotationParser(filepath)
    parser.run()

if __name__ == "__main__":
    main()



