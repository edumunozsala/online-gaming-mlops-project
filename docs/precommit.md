# MLOps Zoomcamp Cohort 2024
# Project: Predict Online Gaming Behavior

## Pre-commit Hook

First, we install the pre-commit library:
```bash
pipenv install --dev pre-commit
```

To test the pre-coomit, we generate a sample config file and then we can install `pre-commit`:
```bash
pre-commit install
```

And we commit a md file to check that our hook is working:
```bash
git commit -m "Testing pre commit hook"
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /home/codespace/.cache/pre-commit/patch1723826840-33871.
Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check Yaml...........................................(no files to check)Skipped
Check for added large files..............................................Passed
[INFO] Restored changes from /home/codespace/.cache/pre-commit/patch1723826840-33871.
[main b5b1ec9] Testing pre commit hook
 1 file changed, 1 insertion(+), 1 deletion(-)
```

We take the pre-commit config file from the MLOps zoomcamo repo as the initial source file. Then, we modify this config YAML file to apply our unit tests and confirm that the linter and formatter are also well configured.

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.2.0
  hooks:
    - id: trailing-whitespace
    - id: check-yaml
    - id: check-added-large-files
- repo: https://github.com/pycqa/isort
  rev: 5.12.0
  hooks:
    - id: isort
      name: isort (python)
- repo: https://github.com/psf/black
  rev: 22.6.0
  hooks:
    - id: black
      language_version: python3.10
- repo: local
  hooks:
    - id: pylint
      name: pylint
      entry: pylint
      language: system
      types: [python]
      args: [
        "-rn", # Only display messages
        "-sn", # Don't display the score
        "--recursive=y"
      ]
- repo: local
  hooks:
    - id: pytest-check
      name: pytest-check
      entry: pytest
      language: system
      pass_filenames: false
      always_run: true
      args: [
        "tests/unit_tests.py"
      ]

```

Now, we can commit some changes and test out pre-commit hook:

```bash
git commit -m "Adding pre commit config"
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /home/codespace/.cache/pre-commit/patch1723829155-50738.
Trim Trailing Whitespace.................................................Passed
Check Yaml...............................................................Passed
Check for added large files..............................................Passed
isort (python).......................................(no files to check)Skipped
black................................................(no files to check)Skipped
pylint...............................................(no files to check)Skipped
pytest-check.............................................................Passed
[INFO] Restored changes from /home/codespace/.cache/pre-commit/patch1723829155-50738.
[main b08c44f] Adding pre commit config
 2 files changed, 65 insertions(+)
 create mode 100644 .pre-commit-config.yaml
 ```

 Every time we commit a change this tests are applied.

