from utils import preprocessing

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df = preprocessing.column_featured_inference(data)
    # REMOVE THIS STEP AFTER INCLUDE IT IN COLUMN_FEATURED

    #X = df.drop(columns=['PlayerID','EngagementLevel'])
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(output.columns)>=10, 'Wrong number of columns for inference'
    assert 'EngagementLevel' not in output.columns, 'EngagementLevel is not allowed for inference'
    assert output is not None, 'The output is undefined'