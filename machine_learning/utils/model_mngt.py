"""
Helper functions to mantain the registered models
"""
import mlflow
from mlflow import MlflowClient
import mlflow.sklearn

def get_model_by_alias(client: MlflowClient, model_name: str, model_version_alias: str):
    """
    Return the model filtered by model name and version
    """
    # Get informawtion about the model
    model_info = client.get_model_version_by_alias(model_name, model_version_alias)

    # Get the model version using a model URI
    model_uri = f"models:/{model_name}@{model_version_alias}"
    model = mlflow.sklearn.load_model(model_uri)

    return model

def compare_metric_value(value: float, best: float, objetive= str):
    """
    Compare value and best and return the best one considering the objetive, max o min.
    """
    
    if objetive=='max':
        compare= True if value >= best else False
    else:
        compare= True if value <= best else False

    return compare

def get_metric_value(history):
    """
    Return the metric value from the history of values
    """
    value= history[0].value if len(history)>0 else -1
    return value

def print_metric_info(history):
    """
    Print the metric info
    """
    for m in history:
        print(f"name: {m.key}")
        print(f"value: {m.value}")
        print(f"step: {m.step}")
        print(f"timestamp: {m.timestamp}")
        print("--")

def search_best_model_version(client: mlflow.tracking.MlflowClient, model_name: str, 
                            metric: str, objetive: str):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # Fetch all registered model versions
    registered_model_versions = client.search_model_versions(f"name='{model_name}'")

    # Print the details of the registered model versions
    best_metric_value=-1
    best_version=-1
    for version in registered_model_versions:
        print(f"Model Name: {version.name}")
        print(f"Version: {version.version}")
        
        metric_value=get_metric_value(client.get_metric_history(version.run_id, metric))

        print("Metric: ", metric_value)
        if compare_metric_value(metric_value, best_metric_value,objetive):
            best_metric_value= metric_value
            best_version= version.version

        print("-" * 20)
        
    print("Best version: ", best_version)
    print("Best value: ", best_metric_value)

    return {'version': best_version, 'value': best_metric_value}

def set_best_model_version(client: mlflow.tracking.MlflowClient, model_name: str, 
                            version: str):
    """
    Set aliases for production to the model and version 
    Returns:
        Set the model name and version as the best model using the proper alias
    """
    alias_best= 'best'
    alias_production= 'production'

    # Specify your custom logic here
    client.set_registered_model_alias(model_name, alias_production, version)
    client.set_registered_model_alias(model_name, alias_best, version)

def get_model_alias(client: mlflow.tracking.MlflowClient, model_name: str, 
                            alias: str):
    """
    Returns:
        Return the model object by model name and alias
    """
    # Load the model by alias
    best_model = mlflow.sklearn.load_model(f"models:/{model_name}@{alias}")

    return best_model
