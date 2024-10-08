conf-dev-env:
			echo "Set enviroment variables for dev enviroment"
			set -a
			source ./.dev.env
			set +a
pylint-errors:
			echo "Checking pylint errors"
			pipenv run pylint --errors-only machine_learning/utils

pylint:
			echo "Checking pylint"
			pipenv run pylint machine_learning/utils

unit-tests:
			echo "Running Unit tests"
			pipenv run pytest tests/unit_tests.py

integration-tests:
			echo "Running Integration tests"
			LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash ./scripts/integration-test.sh

quality-checks:
			echo "Running quality code checks and tests"
			pipenv run isort machine_learning/utils
			pipenv run black machine_learning/utils
			pipenv run pylint machine_learning/utils
copy-files-s3:
			echo "Uploading the necessary datafiles to AWS S3 bucket"
			bash ./scripts/copy-files-s3.sh
plan-deploy-dev:
			echo "Terraform plan for DEV environment"
			bash ./scripts/deploy-dev-aws.sh
run-dev-env: plan-deploy-dev copy-files-s3
			echo "Building and running docker containers in DEV"
			REBUILD=${REBUILD} bash ./scripts/run-dev.sh

run-report-server:
			echo "Building and running the docker container Report Server"
			REBUILD=${REBUILD} bash ./scripts/run-report-server.sh

destroy-dev-aws:
			echo "Destroy Terraform actions for DEV environment"
			bash ./scripts/destroy-dev-aws.sh

shutdown-dev-env: destroy-dev-aws
			echo "Destroy Terraform actions for DEV environment and Shutdown containers"
			bash ./scripts/shutdown-dev.sh

deploy-ecr-prod:
			echo "Creating the AWS ECR repositories"
			bash ./scripts/deploy-prod-ecr.sh

images-ecr-prod: 
			echo "Pushing images to AWS ECR"
			REBUILD=${REBUILD} bash ./scripts/push-images.sh

destroy-ecr-prod:
			echo "Destroy the container repositories on AWS"
			bash ./scripts/destroy-prod-ecr.sh

deploy-aws-prod:
			echo "Deploy the project to AWS"
			bash ./scripts/deploy-prod-aws.sh

destroy-aws-prod:
			echo "Destroy the project on AWS"
			bash ./scripts/destroy-prod-aws.sh
