#!/usr/bin/env bash
set -x

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

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