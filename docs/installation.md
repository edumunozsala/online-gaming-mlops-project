
## Install the softyware

### Install aws cli v2

```bash
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Prepare Python environment for DEV 

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

## Run the DEV solution

Modify the .env y .dev.env files with the AWS credentials. You do not need to set the others parameters.

You need to load the environment variables with the AWS credentials and other parameters.

You can run:
```bash
set -a
source ./.env
set +a
```
Run the command to create the AWS bucket and folders and to run the main containers (Mage, Mlflow and Postgres database):
```bash
make run-dev-env
```
Now, you can copy the files in the folder `data` to the folders created in S3, by default the bucket_name is `mlops-zoomcamp-gaming`. 

## Run the DEV solution

Modify the .env y .dev.env files with the AWS credentials. You do not need to set the others parameters.

You need to load the environment variables with the AWS credentials and other parameters.

You can run:
```bash
set -a
source ./.env
set +a
```

First, we need to create the AWS ECR repositories for our container ipmages:
```bash
make deploy-ecr-prod
```

The output will show you the registry url that we need to log in to push the images. 
container_repository_url = "http://**223817798831.dkr.ecr.us-west-2.amazonaws.com**/online-gaming-production-repository"

Set the env variable:
```bash
export AWS_ECR_ACCOUNT="223817798831.dkr.ecr.us-west-2.amazonaws.com"
```

Once, we have set the env variable `AWS_ECR_ACCOUNT`, we can create and push the container images to ECR:
```bash
make images-ecr-prod
```

And our last step is to deploy all the components:

