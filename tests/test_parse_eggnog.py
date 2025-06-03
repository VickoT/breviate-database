import pandas as pd
from scripts.parse_eggnog import EggNOGAnnotationParser

def test_parse_annotations_explodes_columns():
    parser = EggNOGAnnotationParser("data/test/dummy_eggnog_annotations.tsv")
    parser.load_annotations()
    parser.parse_annotations()

    assert not parser.df["gos"].str.contains(",").any() 


def test_all_columns_are_atomic():
    parser = EggNOGAnnotationParser("data/test/dummy_eggnog_annotations.tsv")
    parser.load_annotations()
    parser.parse_annotations()

    exploded_columns = [
        "eggnog_ogs",
        "gos",
        "cog_category",
        "kegg_ko",
        "kegg_pathway",
        "brite",
        "pfams"
    ]

    
    for col in exploded_columns:
        if parser.df[col].dtype == object:
            assert not parser.df[col].astype(str).str.contains(",").any(), f"{col} contains non-atomic values"
