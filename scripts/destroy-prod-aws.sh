#!/usr/bin/env bash
set -x

echo "Removing all files in the AWS bucket"
aws s3 rm s3://${AWS_BUCKET_NAME} --recursive

echo $PWD
cd ./terraform/aws
echo $PWD

echo "Destroying the components deployed to AWS"
terraform destroy -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "All components destroyed"
    exit ${ERROR_CODE}
fi