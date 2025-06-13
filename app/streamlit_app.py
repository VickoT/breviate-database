import streamlit as st
import streamlit_mermaid
import pandas as pd
from sqlalchemy import create_engine, text

# Konfigurera bred layout först
st.set_page_config(layout="wide")
st.title("EggNOG SQL Query Tool")

# Anslut till databasen
engine = create_engine("postgresql://eggnog:password@db:5432/eggnogdb")

# Skriv SQL-frågan
query = st.text_area("Write your SQL query here:", "SELECT * FROM eggnog_query LIMIT 5")

if st.button("Run Query"):
    try:
        df = pd.read_sql_query(query, engine)

        # Make sure the 'evalue' column is formatted correctly
        if "evalue" in df.columns:
            df["evalue"] = df["evalue"].map(lambda x: f"{x:.2e}" if pd.notnull(x) else x)

        st.dataframe(df, use_container_width=True, height=800)
    except Exception as e:
        st.error(f"Error: {e}")


search_term = st.text_input("🔍 Search annotations (any field):")

if search_term:
    like_pattern = f"%{search_term}%"
    try:
        query = text("""
            SELECT * FROM eggnog_query
            WHERE query_id ILIKE :term
               OR seed_ortholog ILIKE :term
               OR description ILIKE :term
               OR preferred_name ILIKE :term
        """)
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params={"term": like_pattern})
        st.dataframe(df, use_container_width=True, height=600)
    except Exception as e:
        st.error(f"Search failed: {e}")


with st.expander("💡 Example queries"):
    st.markdown("""
    - `SELECT * FROM eggnog_query LIMIT 5`
    - `SELECT c.id, c.query_id, c.category, d.description FROM cog_category c
      JOIN cog_category_description d ON c.category = d.category;`
    - `SELECT query_id, description FROM eggnog_query WHERE evalue < 1e-10`
    - `SELECT COUNT(*) FROM eggnog_query`
    - `SELECT * FROM eggnog_query ORDER BY score DESC LIMIT 10`
    """)

with st.expander("Tables in the database"):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            st.write(tables)
    except Exception as e:
        st.error(f"Error fetching tables: {e}")




uml_code = """
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
"""


if st.checkbox("Show UML Diagram"):
    streamlit_mermaid.st_mermaid(uml_code)
