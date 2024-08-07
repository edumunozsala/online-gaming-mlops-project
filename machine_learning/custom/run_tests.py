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
    ref_data=args[0]
    curr_data=args[1]
    print("Reference data Shape: ", ref_data.shape)
    print("Current data Shape: ", curr_data.shape)
    #print(ref_data)
    #print(curr_data)
    #print(args)
    
    column_mapping= monitoring.get_column_mapping(curr_data, kwargs['prediction_col'])
    test_suites= monitoring.create_test_suite(datetime.now(), ref_data, curr_data, 
                  column_mapping)

    result = test_suites.as_dict()
    
    return result


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
