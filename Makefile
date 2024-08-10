conf-dev-env:
			echo "Set enviroment variables for dev enviroment"
			set -a
			source ./.dev.env
			set +a

integration-tests:
			LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash ./scripts/integration-test.sh
run-dev-env:
			echo "Building and running docker containers in DEV"
			REBUILD=${REBUILD} bash ./scripts/run-dev.sh

run-report-server:
			echo "Building and running the docker container Report Server"
			REBUILD=${REBUILD} bash ./scripts/run-report-server.sh
