import mlflow
from utils import model_mngt
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
    # Specify your custom logic here
    # Step 4: Retrieve registered model version
    #mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_tracking_uri(os.getenv("MLFLOW_ENDPOINT_URL", "http://mlflow:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "online_gaming"))

    client = mlflow.tracking.MlflowClient()
    
    print("Tracking uri: ",client.tracking_uri)
    # Assume the model name you registered is "RandomForestClassifier"
    model_name = kwargs['model_name']

    best_version= model_mngt.search_best_model_version(client,model_name, 
                            "test_precision", "max")

    print("Best version: ", best_version['version'])
    print("Best value: ", best_version['value'])

    return best_version


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
