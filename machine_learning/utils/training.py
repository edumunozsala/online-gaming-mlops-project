"""
Helper functions to train our ML model
"""
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import accuracy_score, precision_score,recall_score, f1_score


def build_model_pipeline(X: pd.DataFrame, params: dict):
    """
    Define the model pipeline and return it
    """
    # Define the types of columns
    numeric_col = X.select_dtypes(exclude=['category','object']).columns.tolist()
    categorical_col= X.select_dtypes(include=['category','object']).columns.tolist()
    
    # Make Pipeline
    # Define pipeline for numeric columns
    num = Pipeline([
        ('imp',SimpleImputer(strategy='mean')),
        ('scl',StandardScaler()),
    ])
    #  Define pipeline for categorical columns
    cat = Pipeline([
        ('imp',SimpleImputer(strategy='most_frequent')),
        ('enc',OneHotEncoder()),
    ])
    # Define the transformer
    preprocessor = ColumnTransformer([
        ('num',num,numeric_col),
        ('cat',cat,categorical_col),
    ])    
    #Check the params to use
    if "learning_rate" in params:
        lr= params['learning_rate']
    else:
        lr= 0.1
    if "n_estimators" in params:
        n_estimators= params['n_estimators']
    else:
        n_estimators=100
        
    if "max_depth" in params:
        max_depth= params['max_depth']
    else:
        max_depth= 3
    # Create the model    
    model= GradientBoostingClassifier(learning_rate=lr, n_estimators=n_estimators, max_depth=max_depth)
    # Create the pipeline
    pipeline = Pipeline([
        ('prep',preprocessor),
        ('model',model),
    ])
    
    print("Pipeline created")
    
    return pipeline

def train_evaluate_model(pipeline: Pipeline, X_train: pd.DataFrame, y_train: np.ndarray,
                         X_test: pd.DataFrame, y_test: np.ndarray):
    """
    Train the model/pipeline and evaluate it. Return the metrics on the test dataset
    """
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred,average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
        
    print("Results: ", [accuracy, precision, recall, f1])
    
    return pipeline, [accuracy, precision, recall, f1]

