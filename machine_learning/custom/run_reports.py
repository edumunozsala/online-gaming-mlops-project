from utils import monitoring
from utils import preprocessing
import os
from datetime import datetime

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
    ref_data=args[1]
    curr_data=args[0]
    #print(ref_data)
    #print(curr_data)
    #print(args)
    print("Init reports")
    column_mapping= monitoring.get_column_mapping(curr_data, kwargs['prediction_col'], 
                                                    kwargs['label_col'])
    summary_report= monitoring.create_summary_report(datetime.now(), ref_data, curr_data, 
                  column_mapping)

    print("Seummary report executed")
    preprocessing.save_json_to_s3(summary_report.json(), os.getenv('AWS_BUCKET_NAME'), 
                                  'monitoring/report/', 'summary_report.json')
    """
    data_drift_report= monitoring.create_data_drift_report(datetime.now(), ref_data, curr_data, 
                  column_mapping)

    prediction_drift_report= monitoring.create_prediction_drift_report(datetime.now(), ref_data, curr_data, 
                  column_mapping)

    """
    return []


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    #assert len(output)==3, f"Created only {len(output)} reports out of 3" 
    assert output is not None, 'The output is undefined'
