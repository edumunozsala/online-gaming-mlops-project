## Prepare DEV enviroment

Install pipenv

Install packages in dev enviroment for linting, formatting and pre-commit
```bash
pipenv install --dev pylint
pipenv install --dev black
pipenv install --dev isort
```

pipenv install --dev mlflow==2.14.0



## Run the DEV soluction

```bash
set -a
source ./.dev.env
set +a
```

then:

```bash
docker compose up --build
```