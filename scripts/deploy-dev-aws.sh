#!/usr/bin/env bash
set -x

echo $PWD
cd ./terraform/aws_dev
echo $PWD

echo "Creating the AWS bucket and folders for the MLOps project"
terraform init --upgrade
terraform plan
terraform apply -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "Bucket and folders created on AWS"
    exit ${ERROR_CODE}
fi