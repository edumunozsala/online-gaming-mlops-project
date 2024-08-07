import pandas as pd
import os

from utils import preprocessing

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    bucket_name=os.getenv('AWS_BUCKET_NAME')
    prefix=kwargs['reference_folder']

    data= preprocessing.load_csv_to_s3(bucket_name, prefix)

   
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(output.columns) >=11
    assert 'prediction' in output.columns, 'Prediction column is not present in current data'
    assert output is not None, 'The output is undefined'