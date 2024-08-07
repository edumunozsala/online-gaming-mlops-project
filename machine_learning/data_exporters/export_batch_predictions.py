from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from pandas import DataFrame
from os import path
import os

from utils import preprocessing
from datetime import datetime

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#s3
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    #print(df)
    #print(config_path)

    bucket_name = os.getenv('AWS_BUCKET_NAME')
    file_name= 'online_gaming_predictions'+datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

    print(bucket_name)
    print(file_name)

    #object_key = kwargs['batch_folder']+'/'+kwargs['output_prefix']+'/'+'online_gaming_predictions.csv'
    
    print(kwargs['batch_folder']+'/'+kwargs['output_prefix'])

    preprocessing.save_csv_to_s3(df, bucket_name, kwargs['batch_folder']+'/'+kwargs['output_prefix'], 
        file_name)
