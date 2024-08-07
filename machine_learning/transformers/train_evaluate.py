from utils import training
import os
import mlflow

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
    X_train, y_train, X_test, y_test=data
    print("X_train: ", X_train.shape)
    print("y_train: ", y_train.shape)
    print("X_test: ", X_test.shape)
    print("y_test: ", y_test.shape)
    
    pipeline= args[0]
    mlflow_tracking_server=os.getenv('MLFLOW_ENDPOINT_URL')
    print("MLflow server: ", mlflow_tracking_server)

    #mlflow.set_tracking_uri(mlflow_tracking_server)
    mlflow.set_tracking_uri(mlflow_tracking_server)
    mlflow.set_experiment("online_gaming")
    
    mlflow.sklearn.autolog(log_input_examples=True, registered_model_name=kwargs['model_name'])
    
    with mlflow.start_run() as run:
    
        pipeline, results= training.train_evaluate_model(pipeline, X_train, y_train,
                         X_test, y_test)
        mlflow.log_metric("test_accuracy", results[0])
        mlflow.log_metric("test_precision",results[1])
        mlflow.log_metric("test_recall", results[2])
        mlflow.log_metric("test_f1_score", results[3])
        # When using autolog the model is logged
        #mlflow.sklearn.log_model(pipeline, artifact_path="models")

    model_uri = "runs:/{}/model".format(run.info.run_id)
    print("Results: ", results)
    
    return run.info.run_id, pipeline, results


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'