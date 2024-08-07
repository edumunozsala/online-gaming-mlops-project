import mlflow
import os

from machine_learning.utils import model_mngt

def test_search_best_model_by_metric():
    # Step 4: Retrieve registered model version
    mlflow.set_tracking_uri(os.getenv("MLFLOW_ENDPOINT_URL", "http://mlflow:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "online_gaming_1"))

    client = mlflow.tracking.MlflowClient()
    
    best_version=model_mngt.search_best_model_version(client, model_name='online_gaming_1', 
                                         metric='test_precision', 
                                         objetive='max')
    print("Best version: ", best_version['version'])
    print("Best value: ", best_version['value'])
    
    #assert best_version['version']
