# MLOps Zoomcamp Cohort 2024
# Project: Predict Online Gaming Behavior

## Linting and formatting

First, we install pylint:
```bash
pipenv install --dev pylint
pipenv install --dev black
pipenv install --dev isort
```

## Sort omports

isort --diff

## Linting
First, we look for errors only:

pylint --errors_only machine_learning/utils

We get the posible errors:

````text
************* Module machine_learning.utils.training
machine_learning/utils/training.py:45:52: E0606: Possibly using variable 'lr' before assignment (possibly-used-before-assignment)
machine_learning/utils/training.py:45:69: E0606: Possibly using variable 'n_estimators' before assignment (possibly-used-before-assignment)
machine_learning/utils/training.py:45:93: E0606: Possibly using variable 'max_depth' before assignment (possibly-used-before-assignment)
```

Now, one its tested we run a errors-only review for all our code, machine_learning package. We exclude the errors about importing libraries, because they can not be evaluated properly by pylint.
```
pylint --errors-only --disable=E0401 machine_learning
```
We realized that the errors are due to the use of decorators, that are detected as variables that are used before assigment. So we can disable this kind of errors

```
************* Module machine_learning.transformers.train_evaluate
machine_learning/transformers/train_evaluate.py:11:1: E0606: Possibly using variable 'transformer' before assignment (possibly-used-before-assignment)
machine_learning/transformers/train_evaluate.py:60:1: E0606: Possibly using variable 'test' before assignment (possibly-used-before-assignment)
************* Module machine_learning.data_loaders.load_current_data
machine_learning/data_loaders/load_current_data.py:10:1: E0606: Possibly using variable 'data_loader' before assignment (possibly-used-before-assignment)
machine_learning/data_loaders/load_current_data.py:28:1: E0606: Possibly using variable 'test' before assignment (possibly-used-before-assignment)
************* Module machine_learning.data_loaders.load_processed_data
machine_learning/data_loaders/load_processed_data.py:13:1: E0606: Possibly using variable 'data_loader' before assignment (possibly-used-before-assignment)
machine_learning/data_loaders/load_processed_data.py:33:1: E0606: Possibly using variable 'test' before assignment (possibly-used-before-assignment)
```

#Checking warning and suggestions

pylint --disable=E0401,E0606 machine_learning/utils

Many warning because of functions without a docstring. We include many of them.
Let's focus in one module, we receive the following errors:
```text
************* Module machine_learning.utils.preprocessing
machine_learning/utils/preprocessing.py:26:0: C0303: Trailing whitespace (trailing-whitespace)
machine_learning/utils/preprocessing.py:29:0: C0303: Trailing whitespace (trailing-whitespace)
machine_learning/utils/preprocessing.py:53:0: C0301: Line too long (117/100) (line-too-long)
machine_learning/utils/preprocessing.py:55:0: C0301: Line too long (122/100) (line-too-long)
machine_learning/utils/preprocessing.py:70:0: C0301: Line too long (101/100) (line-too-long)
machine_learning/utils/preprocessing.py:72:78: C0303: Trailing whitespace (trailing-whitespace)
machine_learning/utils/preprocessing.py:89:0: C0301: Line too long (101/100) (line-too-long)
machine_learning/utils/preprocessing.py:92:0: C0303: Trailing whitespace (trailing-whitespace)
machine_learning/utils/preprocessing.py:100:0: C0301: Line too long (111/100) (line-too-long)
machine_learning/utils/preprocessing.py:118:75: C0303: Trailing whitespace (trailing-whitespace)
machine_learning/utils/preprocessing.py:119:0: C0303: Trailing whitespace (trailing-whitespace)
machine_learning/utils/preprocessing.py:120:0: C0304: Final newline missing (missing-final-newline)
machine_learning/utils/preprocessing.py:1:0: C0114: Missing module docstring (missing-module-docstring)
machine_learning/utils/preprocessing.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:40:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:50:4: C0103: Variable name "X" doesn't conform to snake_case naming style (invalid-name)
machine_learning/utils/preprocessing.py:55:4: C0103: Variable name "X_train" doesn't conform to snake_case naming style (invalid-name)
machine_learning/utils/preprocessing.py:55:13: C0103: Variable name "X_test" doesn't conform to snake_case naming style (invalid-name)
machine_learning/utils/preprocessing.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:93:0: C0116: Missing function or method docstring (missing-function-docstring)
machine_learning/utils/preprocessing.py:2:0: C0411: standard import "json" should be placed before third party import "pandas" (wrong-import-order)
machine_learning/utils/preprocessing.py:4:0: C0411: standard import "io.StringIO" should be placed before third party imports "pandas", "boto3" (wrong-import-order)
machine_learning/utils/preprocessing.py:2:0: W0611: Unused import json (unused-import)
-----------------------------------
Your code has been rated at 6.10/10
```
There are many warning not important, we solve some of them like the doc strins and some wghitesaces. We also disable the message about whitespaces, they are not interesting. We incluide a docstring for the whole module.

Once we've fixed many of them run the linter:

```
pylint --disable=E0401,E0606,C0303 machine_learning/utils/preprocessing.py
```

the poutput is:
```text
************* Module machine_learning.utils.preprocessing
machine_learning/utils/preprocessing.py:70:4: C0103: Variable name "X" doesn't conform to snake_case naming style (invalid-name)
machine_learning/utils/preprocessing.py:73:4: C0103: Variable name "X_train" doesn't conform to snake_case naming style (invalid-name)
machine_learning/utils/preprocessing.py:73:13: C0103: Variable name "X_test" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 9.48/10 (previous run: 9.14/10, +0.34)
```
The final rate is 9.48, good enough.

We should repeat this operation for all the modules. It is a convenient way to produce hugh quality code.!
We create `pyproject-toml` file with this configuration and run the linter easily.

For a future use in a CD/CI pipeline, we will also remove the invalid-name error (it is recommended not to remove this error until you are completely sure it is safe)

```text
(mlops-project) (base) ubuntu@ip-172-31-55-58:~/mlops-zoomcamp/mlops-project$ pylint machine_learning/utils/preprocessing.py 

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.48/10, +0.52)
```

##Formatting the code

We have apply `black` tool to check and format our code. We have configured the `pyproject.toml` file to set the python versin and to skip the string normalization.
```
[tool.black]
line-length = 100
target-version = ["py39", "py311"]
skip-string-normalization = true

```

### Apply everythin

```
isort --diff machine_learning
black --diff machine_learning
pylint --recursive=y machine_learning
pytest tests/
```


