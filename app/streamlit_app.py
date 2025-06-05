import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Konfigurera bred layout först
st.set_page_config(layout="wide")
st.title("EggNOG SQL Query Tool")

# Anslut till databasen
engine = create_engine("postgresql://eggnog:password@db:5432/eggnogdb")

# Skriv SQL-frågan
query = st.text_area("Write your SQL query here:", "SELECT * FROM eggnog_annotations LIMIT 5")

if st.button("Run Query"):
    try:
        df = pd.read_sql_query(query, engine)

        # Make sure the 'evalue' column is formatted correctly
        if "evalue" in df.columns:
            df["evalue"] = df["evalue"].map(lambda x: f"{x:.2e}" if pd.notnull(x) else x)

        st.dataframe(df, use_container_width=True, height=800)
    except Exception as e:
        st.error(f"Error: {e}")
