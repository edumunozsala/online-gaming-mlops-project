"""
Helper function to manage dataframes
"""
import numpy as np
import pandas as pd


def get_numeric_columns(df: pd.DataFrame) -> pd.Index:
    """
    Return a list containing the numeric columns
    """
    return df.select_dtypes(include=[np.number]).columns