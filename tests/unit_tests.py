import pandas as pd

from datetime import datetime

from machine_learning.utils import preprocessing

def test_get_features_by_type():
    data = [
        (1, 'low', 100.0, 'Sports'),
        (2, 'low', 100.0, 'Action'),
        (3, 'medium', 1, 'Category'),
        (4, 'medium', 1, 'Category'),      
    ]

    columns = ['Id', 'level', 'quantity', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    num_cols= preprocessing.get_numeric_columns(df)
    cat_cols= preprocessing.get_categorical_columns(df)
    
    assert len(num_cols)==2, "Error returning numeric cols"
    assert len(cat_cols)==2, "Error returning categoric cols"
    