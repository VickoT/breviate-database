import pandas as pd
from scripts.parse_eggnog import EggNOGAnnotationParser


def test_load_raw_eggnog_annotation_data():
    parser = EggNOGAnnotationParser("data/test/dummy_eggnog_annotations.tsv")
    parser.load_annotations()
    
    assert parser.df is not None
    assert len(parser.df) == 9
