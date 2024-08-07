import os
import mlflow
import mlflow.sklearn
import pandas as pd

from utils import model_mngt

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
    best_version = args[0]
    model_name = kwargs['model_name']
    alias= 'production'

    print(best_version['version'])
    
    # Step 4: Retrieve registered model version
    mlflow.set_tracking_uri(os.getenv("MLFLOW_ENDPOINT_URL", "http://mlflow:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "online_gaming"))

    client = mlflow.tracking.MlflowClient()
    print("Tracking uri: ",client.tracking_uri)
    

    # Specify your custom logic here
    model_mngt.set_best_model_version(client, model_name,best_version['version'])
    
    best_model= model_mngt.get_model_alias(client, model_name, alias)
    

    return best_model


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
