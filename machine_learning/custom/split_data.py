from utils import preprocessing

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
    df= args[0]
    print("Dataset Shape: ",df.shape)

    X_train, y_train, X_test, y_test = preprocessing.split_dataset(df,0.2,['PlayerID','EngagementLevel'],
                                     label= 'EngagementLevel')
    print("X_train: ", X_train.shape)
    print("y_train: ", y_train.shape)
    print("X_test: ", X_test.shape)
    print("y_test: ", y_test.shape)

    return X_train, y_train, X_test, y_test 


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    X_train, y_train, X_test, y_test = output
    assert len(X_train)==len(y_train), 'Number of rows not equal: X_train'
    assert len(X_test)==len(y_test), 'Number of rows not equal: X_train'
    assert output is not None, 'The output is undefined'
