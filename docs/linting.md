# MLOps Zoomcamp Cohort 2024

# Project: Predict Online Gaming Behavior

## Linting and Code Formatting

**Installation steps before runing**

First, we install the libraries in the `dev` environment:

```bash
pipenv install --dev pylint
pipenv install --dev black
pipenv install --dev isort
```

Set the environment variables:

```bash
set -a
source ./.dev.env
set +a
```

## Sort imports

**isort** is a Python utility / library to sort imports alphabetically and automatically separate into sections and by type. It provides a command line utility, Python library and plugins for various editors to quickly sort all your imports

First, we recommend to only show the differences:
```bash
isort --diff
```

Now, review the changes, and if everything looks fine then we will apply it:

```bash
isort machine_learning/utils
```

## Formatting

We install and apply `black` tool to check and format our code. 
We have configured the `pyproject.toml` file to set the python versin and to skip the string normalization, we want black not to change the single quotes..

This is conf section in the `pyproject.toml":

```
[tool.black]
line-length = 100
target-version = ["py39", "py311"]
skip-string-normalization = true

```

First, let's check the differences before applying it directly.

```bash
black --diff machine_learning/utils
```

We review the changes and when we feel comfortable and we can not detect any "issues", so we can apply them:

```bash
black machine_learning/utils
```

Output:

```text
 black machine_learning/utils/
reformatted /workspaces/online-gaming-mlops-project/machine_learning/utils/columns.py
reformatted /workspaces/online-gaming-mlops-project/machine_learning/utils/model_mngt.py
reformatted /workspaces/online-gaming-mlops-project/machine_learning/utils/monitoring.py
reformatted /workspaces/online-gaming-mlops-project/machine_learning/utils/preprocessing.py
reformatted /workspaces/online-gaming-mlops-project/machine_learning/utils/training.py

All done! ✨ 🍰 ✨
5 files reformatted, 1 file left unchanged.
```

## Linting

Pylint is a static code analyser for Python 2 or 3. The latest version supports Python 3.8.0 and above. Pylint analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored.

Our first step is to look for errors only:

```bash
pylint --errors-only machine_learning/utils
```

We get some posible errors:

```text
************* Module machine_learning.utils.training
machine_learning/utils/training.py:45:52: E0606: Possibly using variable 'lr' before assignment (possibly-used-before-assignment)
machine_learning/utils/training.py:45:69: E0606: Possibly using variable 'n_estimators' before assignment (possibly-used-before-assignment)
machine_learning/utils/training.py:45:93: E0606: Possibly using variable 'max_depth' before assignment (possibly-used-before-assignment)
```

We added a section in the `pyproject.toml` file to disable some pylint messages that we do not want it to consider.
```text
[tool.pylint.'MESSAGES_CONTROL']
# if you do not have applied isort and black previously, uncomment the lines
disable=[#"trailing-whitespace", 
        #"missing-final-newline",
        #"possibly-used-before-assignment",
        #"import-error",
        "invalid-name",
        "simplifiable-if-expression"]
```

Now, We review the code and solve some of the possible issues detected. It's time to check for warning or other messages but disabling some messages already fixed:

```bash
pylint --disable=E0401,E0606 machine_learning/utils
```

```text
************* Module machine_learning.utils.preprocessing
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
-----------------------------------
Your code has been rated at 6.10/10
```

There are many warning, not important, we solve some of them like the doc strins and some whitespaces.

Once we've fixed many of them run the linter:

```bash
pylint machine_learning/utils
```

The output is:

```text
************* Module machine_learning.utils.model_mngt
machine_learning/utils/model_mngt.py:16:4: W0612: Unused variable 'model_info' (unused-variable)
machine_learning/utils/model_mngt.py:107:20: W0613: Unused argument 'client' (unused-argument)
------------------------------------------------------------------
Your code has been rated at 9.48/10 (previous run: 9.14/10, +0.34)
```
The final rate is 9.48, good enough.

For a future use in a **CD/CI pipeline**, we will also remove the invalid-name error (it is recommended not to remove this error until you are completely sure it is safe)

```text
(mlops-project) (base) ubuntu@ip-172-31-55-58:~/mlops-zoomcamp/mlops-project$ pylint machine_learning/utils/preprocessing.py 

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.48/10, +0.52)
```

### Apply everythin together

```
isort machine_learning/utils
black machine_learning/utils
pylint --recursive=y machine_learning/utils
```


