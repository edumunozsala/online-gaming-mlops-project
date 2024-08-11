#!/usr/bin/env bash
set -x

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_ACCOUNT}

if [ "${REBUILD}" != "N" ]; then 
    echo "Building the Mage image"
    docker build --platform linux/amd64 --tag onlinegamingprod:latest -f Dockerfile.deploy .
    docker tag onlinegamingprod:latest ${AWS_ECR_ACCOUNT}/online-gaming-production-repository:latest
    docker push ${AWS_ECR_ACCOUNT}/online-gaming-production-repository:latest

    echo "Building the Mlflow image"
    docker build --platform linux/amd64 --tag mlflow:latest mlflow
    docker tag mlflow:latest ${AWS_ECR_ACCOUNT}/mlflow-repository:latest
    docker push ${AWS_ECR_ACCOUNT}/mlflow-repository:latest

    echo "Building the Report Server image"
    docker build --platform linux/amd64 --tag report-server:latest report_server
    docker tag report-server:latest ${AWS_ECR_ACCOUNT}/report-server-repository:latest
    docker push ${AWS_ECR_ACCOUNT}/report-server-repository:latest
fi

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    exit ${ERROR_CODE}
fi