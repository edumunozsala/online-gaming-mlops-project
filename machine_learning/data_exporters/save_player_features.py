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
    # Specify your data exporting logic here
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    print(bucket_name)

  
    preprocessing.save_csv_to_s3(data, bucket_name, kwargs['processed_folder'], 
        kwargs['features_file'])


