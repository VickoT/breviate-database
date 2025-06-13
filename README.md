![CI](https://github.com/VickoT/breviate-database/actions/workflows/ci.yml/badge.svg?branch=main)


# breviate-database
A Dockerized PostgreSQL database for storing functional annotations of breviate proteomes.



## Database setup pipeline

1. The containers and accessing them

1. The raw data is stored in `data/test/...`
2. By running `python scripts/models.py`, the database is initialized using an Object-Relational Mapper (ORM). With ORM, each table is represented by a Python class. After all tables have been defined as classes the function bellow is executed. This function:    
    * Connecects to the PostgreSQL database running inside the Docker container (via localhost:5432).
    * Generates all tables defined by the ORM model (if they don't already exists).

    ```
    def init_db():
        engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
        Base.metadata.create_all(engine)
        print("Database initialized successfully.")
    ```

3. With the database schema in place inside the container, populate the tables by running `scripts/parse_eggnog.py`. This script:
    * Loads the raw eggnog data.
    * Parse the data and makes each cell contain one value per cell
    * Exports the data to the database. This is done using this function:

   ```
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

   ```
   This function:
   
   * Creates a SQLAlchemy engine to connect to the PostgreSQL database.
   * Sets up a session factory (sessionmaker) bound to the engine and opens a session — this is used to interact with the database.
   * Loops over each row in the DataFrame, constructs an EggnogQuery object from it, and adds it to the session.
   * Commits all pending entries and closes the section.
        



**EggNOG columns**


Data            | Description
----------------|-------------
**seed_ortholog**   |  Closest ortholog match found in the EggNOG database.
**evalue**          |  E-value of the ortholog match (lower is better).
**score**           |  Bit-score of the ortholog match (higher is better).
eggNOG_OGs      |  Orthologous groups (OG) to which the protein belongs, with taxonomic info.
**max_annot_lvl**   |  Most specific taxonomic level at which the annotation is valid.
**COG_category**    |  Functional category code (Cluster of Orthologous Genes).
**Description**     |  Description of the function of the ortholog.
**Preferred_name**  |  Preferred gene name or symbol.
GOs             |  Gene Ontology terms.
EC              |  Enzyme Commission numbers (if it's an enzyme).
**KEGG_ko**         |  KEGG Orthology identifiers.
KEGG_Pathway    |  KEGG pathways in which the gene is involved.
KEGG_Module     |  KEGG modules (functional units).
KEGG_Reaction   |  Specific biochemical reactions (if available).
KEGG_rclass     |  KEGG reaction class.
BRITE           |  BRITE functional hierarchy classification.
KEGG_TC         |  KEGG Transported Classification.
CAZy            |  Carbohydrate-Active Enzymes family, if any.
BiGG_Reaction   |  Metabolic reaction in the BiGG database.
PFAMs           |  PFAM protein domain identified. 


## Database structure (ER-diagram)

```mermaid
erDiagram
    EggnogQuery {
        int id PK
        text query_id
        text seed_ortholog
        float evalue
        float score
        text max_annot_lvl
        text description
        text preferred_name
        timestamp created_at
    }


    KEGG_ko {
        int id PK
        int query_id FK
        text kegg_ko
    }

    KEGG_Pathway {
        int id PK
        int query_id FK
        text kegg_pathway
    }

    COG_Category {
        int id PK
        int query_id FK
        text category
    }

   COG_Category_Description {
         text category PK
         text description 
   }


    EggnogQuery ||--o{ KEGG_ko : contains
    EggnogQuery ||--o{ KEGG_Pathway : contains
    EggnogQuery ||--o{ COG_Category : contains
    COG_Category ||--o{ COG_Category_Description : contains
    

