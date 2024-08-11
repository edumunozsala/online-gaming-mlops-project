#!/usr/bin/env bash
set -x

echo $PWD
cd ./terraform/aws_ecr
echo $PWD

terraform init
terraform plan
terraform apply -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "Repositories created successfully"

    exit ${ERROR_CODE}
fi