#!/usr/bin/env bash
set -x

echo $PWD
cd ./terraform/aws_dev
echo $PWD

echo "Destroy the AWS bucket and folders for the MLOps project"
terraform destroy -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "Bucket and folders destroyed on AWS"
    exit ${ERROR_CODE}
fi