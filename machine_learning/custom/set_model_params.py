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
    params ={
        "learning_rate": 0.1,
        "n_estimators": 150,
        "max_depth": 4
    }
    return params


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert "learning_rate" in output.keys()
    assert "n_estimators" in output.keys()
    assert "max_depth" in output.keys()