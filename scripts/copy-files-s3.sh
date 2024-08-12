#!/usr/bin/env bash
set -x

echo $PWD
echo "Uploading the data files to S3"
aws s3 cp ./data/input s3://${AWS_BUCKET_NAME}/input --recursive
aws s3 cp ./data/processed s3://${AWS_BUCKET_NAME}/processed --recursive
aws s3 cp ./data/batch s3://${AWS_BUCKET_NAME}/batch --recursive
aws s3 cp ./data/monitoring s3://${AWS_BUCKET_NAME}/monitoring --recursive

ERROR_CODE=$?

if [ ${ERROR_CODE} == 0 ]; then
    echo "All files uploaded to S3"
    exit ${ERROR_CODE}
fi