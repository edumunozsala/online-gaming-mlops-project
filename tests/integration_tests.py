import mlflow
import os

from machine_learning.utils import model_mngt

def test_get_model_by_alias():
    # Step 4: Retrieve registered model version
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "online_gaming"))

    client = mlflow.tracking.MlflowClient()
    model_name="online_gaming"
    alias="production"
    
    best_model = model_mngt.get_model_by_alias(client, 
                                            model_name,
                                            alias)
    
   
    assert best_model is not None, 'Model not restored'


def test_search_best_model_by_metric():
    # Step 4: Retrieve registered model version
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "online_gaming"))

    client = mlflow.tracking.MlflowClient()
    
    best_version=model_mngt.search_best_model_version(client, model_name='online_gaming', 
                                         metric='test_precision', 
                                         objetive='max')
    print("Best version: ", best_version['version'])
    print("Best value: ", best_version['value'])
    
    assert int(best_version['version'])>0, 'Model version incorrect'

def test_get_model_alias():
    # Step 4: Retrieve registered model version
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "online_gaming"))

    client = mlflow.tracking.MlflowClient()
    model_name="online_gaming"
    alias="production"
    
    best_model = model_mngt.get_model_alias(client, 
                                            model_name,
                                            alias)
    
   
    assert best_model is not None, 'Model not restored'
