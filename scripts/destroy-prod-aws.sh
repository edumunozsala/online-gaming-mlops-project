#!/usr/bin/env bash
set -x

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