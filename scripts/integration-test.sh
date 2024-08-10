#!/usr/bin/env bash
set -x

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

export MLFLOW_PORT="5000"
export MLFLOW_ENDPOINT_URL="http://127.0.0.1:5000"
export BACKEND_STORE_URI="sqlite:////mlflow/mlflow.db"
export MLFLOW_EXPERIMENT_NAME="online_gaming_1"

export DEFAULT_ARTIFACT_ROOT="s3://${AWS_BUCKET_NAME}"
export DEFAULT_ARTIFACTS_DESTINATION="s3://${AWS_BUCKET_NAME}"

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    echo "Building and runing mlflow container"
    docker compose up -d mlflow --build
else
    echo "No need to build image. Runing container"
    docker compose up -d mlflow
fi

sleep 15

echo $PWD
pipenv run pytest ../tests/integration_tests.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
fi

docker-compose down
