from typing import List
import pandas as pd

from mage_ai.data_preparation.models.global_data_product import GlobalDataProduct

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

DEFAULT_INPUTS=[{
    'Age': 43,
    'Gender': 'Male',
    'Location': 'Other',
    'GameGenre': 'Strategy',
    'PlayTimeHours': 16.27,
    'InGamePurchases': 'No',
    'GameDifficulty': 'Medium',
    'SessionsPerWeek': 6,
    'AvgSessionDurationMinutes': 108,
    'PlayerLevel': 79,
    'AchievementsUnlocked': 25
}]


@custom
def online_inference(*args, **kwargs) -> List[int]:
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Read the input data

    input_features= kwargs.get('inputs', DEFAULT_INPUTS)
    X= pd.DataFrame(input_features)

    # Load the model from a GDP
    gdp_best_model=args[0]
    best_model = gdp_best_model['set_best_model'][0]
    #print(gdp_best_model['set_best_model'])
    #print(type(gdp_best_model['set_best_model'][0]))
    #print(best_model)
    # Get the prediction
    y_pred= best_model.predict(X)

    if len(y_pred)>0:
        #prediction= y_pred[0]
        print('y_pred: ', y_pred)

        #return {'prediction': prediction}
        return y_pred.tolist()
    else:
        print("No predictions")
        return []


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
