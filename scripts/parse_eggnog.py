#!/usr/bin/env python3
import pandas as pd
from models import EggnogQuery, COGCategory, COGCategoryDescription, KEGGOrtholog, Base
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

        session.query(EggnogQuery).delete()
        session.query(KEGGOrtholog).delete()
        session.query(COGCategory).delete()
        session.query(COGCategoryDescription).delete()
        session.commit()

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

            # KEGG Orthologs
            if pd.notna(row.get('kegg_ko')):
                for ko in row['kegg_ko'].split(','):
                    ko = ko.strip()
                    if ko and ko != "-":
                        kegg_entry = KEGGOrtholog(query_id=row['query_id'], kegg_ko=ko)
                        session.add(kegg_entry)


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

    def create_cog_description_table(self):
        """Populate the cog_category_description table with all standard COG categories."""
        engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        cog_category_descriptions = {
            'A': 'RNA processing and modification',
            'B': 'Chromatin structure and dynamics',
            'C': 'Energy production and conversion',
            'D': 'Cell cycle control, cell division, chromosome partitioning',
            'E': 'Amino acid transport and metabolism',
            'F': 'Nucleotide transport and metabolism',
            'G': 'Carbohydrate transport and metabolism',
            'H': 'Coenzyme transport and metabolism',
            'I': 'Lipid transport and metabolism',
            'J': 'Translation, ribosomal structure and biogenesis',
            'K': 'Transcription',
            'L': 'Replication, recombination and repair',
            'M': 'Cell wall/membrane/envelope biogenesis',
            'N': 'Cell motility',
            'O': 'Post-translational modification, protein turnover, chaperones',
            'P': 'Inorganic ion transport and metabolism',
            'Q': 'Secondary metabolites biosynthesis, transport and catabolism',
            'R': 'General function prediction only',
            'S': 'Function unknown',
            'T': 'Signal transduction mechanisms',
            'U': 'Intracellular trafficking, secretion, and vesicular transport',
            'V': 'Defense mechanisms',
            'W': 'Extracellular structures',
            'Y': 'Nuclear structure',
            'Z': 'Cytoskeleton',
        }

        objects = [
            COGCategoryDescription(category=cat, description=desc)
            for cat, desc in cog_category_descriptions.items()
        ]

        for obj in objects:
            session.merge(obj)  # insert or update if exists
        session.commit()
        session.close()
        print("COG category description table populated.")




    def run(self):
        self.load_annotations()
        self.export_to_postgres()
        self.create_cog_description_table()


def main():
    filepath = "data/eggnog.emapper.annotations"
    parser = EggNOGAnnotationParser(filepath)
    parser.run()

if __name__ == "__main__":
    main()
