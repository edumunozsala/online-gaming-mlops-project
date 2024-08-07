from datetime import datetime
from utils import monitoring

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
    ref_data= args[0]
    curr_data= args[1]

    # drop colum
    cols_to_drop=eval(kwargs['cols_ref_to_drop'])
    curr_data= curr_data.drop(columns=cols_to_drop)

    # Run and save the reports to a temprary folder
    summary_report, data_drift_report, pred_drift_report = monitoring.create_reports(datetime.utcnow(), 
                                                            ref_data, curr_data, kwargs['prediction_col'])
                                                            
    return [summary_report, data_drift_report, pred_drift_report]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
