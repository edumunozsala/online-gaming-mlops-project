#!/usr/bin/env bash
set -x

echo "Removing all files in the AWS bucket"
aws s3 rm s3://${AWS_BUCKET_NAME} --recursive

echo $PWD
cd ./terraform/aws_ecr
echo $PWD


terraform destroy -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "Repositories destroyed successfully"
    exit ${ERROR_CODE}
fi