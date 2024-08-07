from datetime import datetime
import os
from utils import preprocessing

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    
    # Get the actual date
    current_date= datetime.now()
    data['pred_date']= current_date
    print("Current data shape: ", data.shape)
    # Set the S· bucket and folder
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    file_name= 'online_gaming_predictions'+current_date.strftime("%Y%m%d%H%M%S")+'.csv'

    print(bucket_name)
    print(file_name)

    #object_key = kwargs['batch_folder']+'/'+kwargs['output_prefix']+'/'+'online_gaming_predictions.csv'
    
    print(kwargs['monitoring_folder'])

    preprocessing.save_csv_to_s3(data, bucket_name, kwargs['monitoring_folder'], 
        file_name)    

