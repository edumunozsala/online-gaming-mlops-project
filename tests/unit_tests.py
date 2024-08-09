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
    
def test_column_featured():
    data = [
        (1, 0, 'Low', 'Easy'),
        (2, 0, 'Medium', 'Medium'),
        (3, 1, 'High', 'Hard'),
        (4, 1, 'Low', 'Easy'),      
    ]

    data_processed = [
        (1, 'No', 0, 'Easy'),
        (2, 'No', 1, 'Medium'),
        (3, 'Yes', 2, 'Hard'),
        (4, 'Yes', 0, 'Easy'),      
    ]
    columns = ['Id', 'InGamePurchases', 'EngagementLevel', 'GameDifficulty']
    df = pd.DataFrame(data, columns=columns)
    df_processed = pd.DataFrame(data_processed, columns=columns)
    df_processed = df_processed.astype({'InGamePurchases': 'category', 'GameDifficulty': 'category'})
    
    df= preprocessing.column_featured(df)
    
    print(df.head())
    print(df_processed.head())
        
    assert df.equals(df_processed), "Column featured: Both Dataframes are nor equals"

def test_split_dataset():
    data = [
        (1, 'No', 0, 'Easy'),
        (2, 'No', 1, 'Medium'),
        (3, 'Yes', 2, 'Hard'),
        (4, 'Yes', 0, 'Easy'), 
        (5, 'No', 1, 'Medium'),             
        (6, 'Yes', 2, 'Hard'),        
        (7, 'No', 0, 'Easy'),
        (8, 'No', 1, 'Medium'),
        (9, 'Yes', 2, 'Hard'),
        (10, 'Yes', 0, 'Easy'), 
        (11, 'No', 1, 'Medium'),             
        (12, 'Yes', 2, 'Hard'),        
        
    ]
    columns = ['Id', 'InGamePurchases', 'EngagementLevel', 'GameDifficulty']
    df = pd.DataFrame(data, columns=columns)
    #df_processed = pd.DataFrame(data_processed, columns=columns)
    df = df.astype({'InGamePurchases': 'category', 'GameDifficulty': 'category'})
    
    X_train, y_train, X_test, y_test= preprocessing.split_dataset(df, 0.25, ['GameDifficulty'], 'EngagementLevel')
    
    print(X_train.shape, X_test.shape)
    assert len(X_train)==9, "Column featured: Rows in X_train wrong"
    assert len(y_train)==9, "Column featured: Rows in y_train wrong"
    assert len(X_test)==3, "Column featured: Rows in X_test wrong"
    assert len(y_test)==3, "Column featured: Rows in y_test wrong"
