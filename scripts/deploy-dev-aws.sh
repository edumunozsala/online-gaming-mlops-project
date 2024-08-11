#!/usr/bin/env bash
set -x

echo $PWD
cd ./terraform/aws_dev
echo $PWD

terraform init
terraform plan
terraform apply -auto-approve

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    aws s3 cp ../../data/input/* s3://${AWS_BUCKET_NAME}/input
    aws s3 cp ../../data/processed/* s3://${AWS_BUCKET_NAME}/processed
    aws s3 cp ../../data/batch/* s3://${AWS_BUCKET_NAME}/batch
    aws s3 cp -r ../../data/monitoring/* s3://${AWS_BUCKET_NAME}/monitoring

    exit ${ERROR_CODE}
fi