#!/usr/bin/env bash
set -x

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

echo $PWD
cd ..
echo $PWD

docker compose down

sleep 1

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
fi