# MLOps Zoomcamp Cohort 2024

# Project: Predict Online Gaming Behavior

## Unit testing

**Important**: Follow the instructions in the Installation and How-to guides before runing this commands.

We have include some unit test to show how to fit them into this kind of project. These unit tests check functions that are invoked from the Magew blocks to transform and prepare Pandas dataframe. Once we have created a DEV enviroment, you can install pytest (instruction are included in the following section) and run the test to check if things are working fine:

```bash
pytest tests/unit_tests.py
```

To make things easier, you can also run the command `make unit-tests` to run the unit tests.

```bash
make unit-tests
```

All relevant code and the functions we use in the Mage pipelines have been included in the package utils, that's why we only check that folder. And the results of the pytest execution is:
```
========================================================================================= test session starts =========================================================================================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
rootdir: /workspaces/online-gaming-mlops-project
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 3 items                                                                                                                                                                                     

tests/unit_tests.py ...                                                                                                                                                                         [100%]

========================================================================================== 3 passed in 7.19s ==========================================================================================
```

### Integration test

**Integration testing** is a type of software testing where components of the software are gradually integrated and then tested as a whole. Usually, these components are already working well individually. However, they may break when integrated with other components.

For this project, we have prepared a test scenario where we run the mlflow server container and test the code in `machine_learning/utils' that creates a mlclient and connects to the container. 

* Set some evironment variables
* Start the mlflow Docker container
* Run the integration tests
* Show the error output and logs.

Next, we show you how to run this test:

First, you need to set some environment variables to access AWS from the mlflow container:
```bash
set -a
source ./.dev.env
set +a
```

If you do not want to build or rebuild the container image, you have to set up the env variable `LOCAL_IMAGE_NAME` to `mlflow`.

And now we can run the test using the `make` command and the task defined in the `Makefile`:
```bash
make scripts/integration-tests
```

The content of this section of the `Makefile` is:
```make
integration-tests:
			LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash ./scripts/integration-test.sh

```

Let's print the output:

```text
LOCAL_IMAGE_NAME=mlflow_tracker_5000 bash ./scripts/integration-test.sh
+ [[ -z '' ]]
++ dirname ./scripts/integration-test.sh
+ cd ./scripts
+ export MLFLOW_PORT=5000
+ MLFLOW_PORT=5000
+ export MLFLOW_ENDPOINT_URL=http://127.0.0.1:5000
+ MLFLOW_ENDPOINT_URL=http://127.0.0.1:5000
+ export BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
+ BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
+ export MLFLOW_EXPERIMENT_NAME=online_gaming_1
+ MLFLOW_EXPERIMENT_NAME=online_gaming_1
+ export DEFAULT_ARTIFACT_ROOT=s3://mlops-zoomcamp-gaming
+ DEFAULT_ARTIFACT_ROOT=s3://mlops-zoomcamp-gaming
+ export DEFAULT_ARTIFACTS_DESTINATION=s3://mlops-zoomcamp-gaming
+ DEFAULT_ARTIFACTS_DESTINATION=s3://mlops-zoomcamp-gaming
+ '[' mlflow_tracker_5000 == '' ']'
+ echo 'No need to build image. Runing container'
No need to build image. Runing container
+ docker compose up -d mlflow
[+] Running 2/2
 ✔ Network online-gaming-mlops-project_app-network  Created                                                                                                                                                                                  0.1s 
 ✔ Container mlflow_tracker_5000                    Started                                                                                                                                                                                  0.6s 
+ sleep 15
+ echo /workspaces/online-gaming-mlops-project/scripts
/workspaces/online-gaming-mlops-project/scripts
+ pipenv run pytest ../tests/integration_tests.py
Loading .env environment variables...
============================================================================================================== test session starts ===============================================================================================================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
rootdir: /workspaces/online-gaming-mlops-project
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 3 items                                                                                                                                                                                                                                

../tests/integration_tests.py ...                                                                                                                                                                                                          [100%]

================================================================================================================ warnings summary ================================================================================================================
../../../home/codespace/.local/share/virtualenvs/online-gaming-mlops-project-uvzvqTV3/lib/python3.10/site-packages/mlflow/utils/requirements_utils.py:20
  /home/codespace/.local/share/virtualenvs/online-gaming-mlops-project-uvzvqTV3/lib/python3.10/site-packages/mlflow/utils/requirements_utils.py:20: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
    import pkg_resources  # noqa: TID251

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================================================================================================== 3 passed, 1 warning in 7.90s ==========================================================================================================
+ ERROR_CODE=0
+ '[' 0 '!=' 0 ']'
+ docker-compose down
[+] Running 2/2
 ✔ Container mlflow_tracker_5000                    Removed                                                                                                                                                                                 10.4s 
 ✔ Network online-gaming-mlops-project_app-network  Removed 
```
We have show a full detailed output where you can follow the steps taken and the results.
