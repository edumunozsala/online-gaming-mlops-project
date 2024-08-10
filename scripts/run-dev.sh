#!/usr/bin/env bash
set -x

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

export PROJECT_NAME="machine_learning"
export MAGE_CODE_PATH="/home/src"
# Load custom files
PYTHONPATH="${MAGE_CODE_PATH}/${PROJECT_NAME}:${PYTHONPATH}"

export MLFLOW_PORT="5000"
export MLFLOW_ENDPOINT_URL="http://mlflow:5000"
export BACKEND_STORE_URI="sqlite:////mlflow/mlflow.db"
export MLFLOW_EXPERIMENT_NAME="online_gaming"

export DEFAULT_ARTIFACT_ROOT="s3://${AWS_BUCKET_NAME}"
export DEFAULT_ARTIFACTS_DESTINATION="s3://${AWS_BUCKET_NAME}"

echo $PWD
cd ..
echo $PWD

if [ "${REBUILD}" == "N" ]; then 
    echo "No need to build images. Runing the containers"
    docker compose up -d
else
    echo "Building and runing the containers"
    docker compose up -d --build
fi

sleep 45

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
fi