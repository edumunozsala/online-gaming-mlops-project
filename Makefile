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
run-dev-env:
			echo "Building and running docker containers in DEV"
			REBUILD=${REBUILD} bash ./scripts/run-dev.sh

run-report-server:
			echo "Building and running the docker container Report Server"
			REBUILD=${REBUILD} bash ./scripts/run-report-server.sh
