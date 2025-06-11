![CI](https://github.com/VickoT/breviate-database/actions/workflows/ci.yml/badge.svg?branch=try-ci)


# breviate-database
A Dockerized PostgreSQL database for storing functional annotations of breviate proteomes.



**EggNOG columns**


Data            | Description
----------------|-------------
seed_ortholog   |  Closest ortholog match found in the EggNOG database.
evalue          |  E-value of the ortholog match (lower is better).
score           |  Bit-score of the ortholog match (higher is better).
eggNOG_OGs      |  Orthologous groups (OG) to which the protein belongs, with taxonomic info.
max_annot_lvl   |  Most specific taxonomic level at which the annotation is valid.
COG_category    |  Functional category code (Cluster of Orthologous Genes).
Description     |  Description of the function of the ortholog.
Preferred_name  |  Preferred gene name or symbol.
GOs             |  Gene Ontology terms.
EC              |  Enzyme Commission numbers (if it's an enzyme).
KEGG_ko         |  KEGG Orthology identifiers.
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

    Eggnog_OG {
        id int PK
        query_id text FK
        og_name text
    }    

    GO_Term {
        int id PK
        int query_id FK
        text go_term
    }

    EC_Number {
        int id PK
        int query_id FK
        text ec_number
    }

    KEGG_Annotation {
        int id PK
        int query_id FK
        text kegg_ko
        text kegg_pathway
        text kegg_module
        text kegg_reaction
        text kegg_rclass
        text brite
        text kegg_tc
    }

    PfamDomain {
        int id PK
        int query_id FK
        text pfam_domain
    }

    COG_Category {
        int id PK
        int query_id FK
        text category
    }

    CAZyFamily {
        int id PK
        int query_id FK
        text family
    }

    BiGGReaction {
        int id PK
        int query_id FK
        text reaction
    }

    EggnogQuery ||--o{ Eggnog_OG : contains
    EggnogQuery ||--o{ GO_Term : contains
    EggnogQuery ||--o{ EC_Number : contains
    EggnogQuery ||--o{ KEGG_Annotation : contains
    EggnogQuery ||--o{ PfamDomain : contains
    EggnogQuery ||--o{ COG_Category : contains
    EggnogQuery ||--o{ CAZyFamily : contains
    EggnogQuery ||--o{ BiGGReaction : contains
