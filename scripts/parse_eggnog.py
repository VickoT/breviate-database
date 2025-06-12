#!/usr/bin/env python3
import pandas as pd
from models import EggnogQuery, COGCategory, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class EggNOGAnnotationParser: 

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_annotations(self):
        """Load EggNOG annotations from a TSV file."""

        self.df = pd.read_csv(self.filepath, sep='\t', skiprows=4)
        # Remove the last non data rows
        self.df = self.df[~self.df['#query'].str.startswith('##')]

        # Make colnames are consistent with the schema format
        self.df = self.df.rename(columns={"#query": "query_id"})
        self.df.columns = [col.lower() for col in self.df.columns]

        print(f"Loaded {len(self.df)} EggNOG annotations from {self.filepath}")
        print(self.df.columns)


    def export_to_postgres(self):
        engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        cog_rows = []

        for _, row in self.df.iterrows():
            # Create EggnogQuery object and add to session
            entry = EggnogQuery(
                query_id=row['query_id'],
                seed_ortholog=row.get('seed_ortholog'),
                evalue=row.get('evalue'),
                score=row.get('score'),
                max_annot_lvl=row.get('max_annot_lvl'),
                description=row.get('description'),
                preferred_name=row.get('preferred_name'),
            )
            session.add(entry)
            session.flush()

            # Create COGCategory objects for each category in the row
            if pd.notna(row.get('cog_category')):
                # Some are stored in the format 'ADEG'
                for category in str(row['cog_category']):
                    category = category.strip()
                    if category and category != "-":
                        cog_rows.append(COGCategory(query_id=row['query_id'],
                                                    category=category))

        session.bulk_save_objects(cog_rows)
        session.commit()
        session.close()
        print("Annotations exported to PostgreSQL database")


    def run(self):
        self.load_annotations()
        self.export_to_postgres()


def main():
    filepath = "data/eggnog.emapper.annotations"
    parser = EggNOGAnnotationParser(filepath)
    parser.run()

if __name__ == "__main__":
    main()



