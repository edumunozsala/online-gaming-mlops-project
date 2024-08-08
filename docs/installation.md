## Prepare DEV enviroment

Install pipenv

Install packages in dev enviroment
```bash
pipenv install --dev pylint
pipenv install --dev black
pipenv install --dev isort
```

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