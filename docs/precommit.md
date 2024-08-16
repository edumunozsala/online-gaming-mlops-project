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

We take the pre-commit config file from the MLOps zoomcamo repo as the initial source file. Then, we modify this config YAML file to apply our unit tests and confirm that the linter and formatter are also well configured.


