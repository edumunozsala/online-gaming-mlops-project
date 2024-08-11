#!/usr/bin/env bash
set -x

echo $PWD
cd ./terraform/aws
echo $PWD

terraform init
terraform plan
echo "Deploying components to AWS"
terraform apply -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "All components deployed to AWS"
    exit ${ERROR_CODE}
fi