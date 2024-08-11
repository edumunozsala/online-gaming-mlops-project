
## Install the softyware

### Install aws cli v2

```bash
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Prepare DEV enviroment

Install pipenv

Install packages in dev enviroment for linting, formatting and pre-commit
```bash
pipenv install --dev pylint
pipenv install --dev black
pipenv install --dev isort
```

pipenv install --dev mlflow==2.14.0
pipenv install --dev boto3== 1.34.156

## Create a AWS User to deploy the Project

* Create a Policy using the file xxxxx

Go to AWS Console, to IAM section and Policies.
* Click in Create a Policy
- Select Json as input and copy the content of the file xxxx
- Give it a name and save it

* Next, go to users and click on Create user
- Introduce a name, then next.
- In Permission Options, select Add user to group
- Click on create group
    - Insert the name
    - Select the policy created and the `AmazonS3FullAccess` policy.
    **You can adjust this policies based on your needs**
    - Then, click Create the user group 
- Once, the group is created and attached to the user, Next.
- Finally, review and create the user.





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