#!/usr/bin/env bash
set -x

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

echo $PWD
cd ../report_server
echo $PWD

if [ "${REBUILD}" == "N" ]; then 
    echo "No need to build image. Runing the container"
    docker compose up -d
else
    echo "Building and runing the container"
    docker compose up -d --build
fi

sleep 10

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
fi