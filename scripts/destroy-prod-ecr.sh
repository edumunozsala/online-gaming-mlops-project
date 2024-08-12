#!/usr/bin/env bash
set -x

echo $PWD
cd ./terraform/aws_ecr
echo $PWD


terraform destroy -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "Repositories destroyed successfully"
    exit ${ERROR_CODE}
fi