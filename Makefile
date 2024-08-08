conf-dev-env:
			echo "Set enviroment variables for dev enviroment"
			set -a
			source ./.dev.env
			set +a

run-dev-env:
			echo "Building and running docker containers in DEV"
			docker compose up --build
