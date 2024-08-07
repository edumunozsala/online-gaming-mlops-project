from utils import preprocessing
import os

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    #summary_report, data_drift_report, pred_drift_report = tuple(args)
    file_names=args[0]
    #f= file_names[0].split('/')[-1]
    for file_name in file_names:
        preprocessing.save_json_to_s3(file_name, os.getenv('AWS_BUCKET_NAME'), kwargs['reports_folder_s3'], 
                    file_name.split('/')[-1])

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
