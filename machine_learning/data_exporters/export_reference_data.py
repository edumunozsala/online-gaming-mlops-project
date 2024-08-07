import os
import pandas as pd
from datetime import datetime
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
    # Specify your data exporting logic here
    # Get the pipeline
    pipeline=data[1]
    # Get the dataset
    X_train, y_train, X_test, y_test = args[0]
    # Calculate the predictions for the test dataset
    X_reference= pd.concat([X_train, X_test], axis=0)
    y_preds= pipeline.predict(X_reference)
    # Add the date and the prediction  
    #X_test['label']= y_test
    X_reference['prediction']= y_preds
    current_date= datetime.utcnow()
    X_reference['pred_date']= current_date
    print("X_Reference Shape: ", X_reference.shape)

    # Set the S· bucket and folder
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    file_name= 'online_gaming_predictions'+current_date.strftime("%Y%m%d%H%M%S")+'.csv'

    print(bucket_name)
    print(file_name)

    preprocessing.save_csv_to_s3(X_reference, bucket_name, kwargs['monitoring_folder']+'/'+
            kwargs['reference_folder'], file_name)    
