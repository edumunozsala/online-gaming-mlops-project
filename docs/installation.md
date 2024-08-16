# MLOps Zoomcamp Cohort 2024

# Project: Predict Online Gaming Behavior

## How-to Guides to Run the Project

## Install the base software: Prerequisites to run the project demo

**Note:** You can use a GitHub Codespace to run this demo, it's installed both Docker and Git. You can watch [this video](https://youtu.be/XOSUt8Ih3zA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15) for instructions on how to prepare a Codespace.

1. Docker:
	You need to install docker for your OS. [Link to installation](https://docs.docker.com/engine/install/) 
2. Git
	You can install Git from this [link](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Terraform
	Installation: https://developer.hashicorp.com/terraform/install

4. AWS Cli v2
    You will need AWS Cli to deploy the project to AWS. You can read this [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for further instructions.
    You can run this commands in Ubuntu linux:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
## Create a AWS User to deploy the Project
This project uses AWS S3 as the storage layer for your input data as well as the data processed in each step or pipeline. Therefore, to run it you will need an AWS user with the necessary permissions.

To run the project in development mode, with Docker containers, the AWS user will only need permissions on S3 (for simplicity, we will give him S3 Admin permissions). 

On the other hand, if we want to deploy the project in AWS as in the production case, in addition to the full permission on S3 it will also require a multitude of permissions on other components that we will define in an AIM policy.

### Create a IAM user for the project

* Create a Policy using the file `scripts/policies/magedeploy.json`

Go to the AWS Console, IAM section and then, select Policies.
* Click on **Create a Policy**
- Select **Json as input** and copy the content of the file `scripts/policies/magedeploy.json`
- Then, **enter a name** for the policy and **save** it.

* Next, go to **Users** section and click on **Create user**

- Introduce a name, then next.
- In Permission Options, select `Add user to group`
- Then, click on **Create group**
    - Enter a name for the Group
    - Then, **select the policy created in the previous step** and the **`AmazonS3FullAccess`** policy.
    Note: **You can adjust this policies based on your needs**
    - Click on **Create** to save the user group 

- Once, the group is created and attached to the user, click Next.
- Finally, review and **Create** the user.

You will need to **create an Access Key and Secret ID** for the user.

## Prepare Python environment for DEV 

To run the tests, the linting and formatter libraries you will need to install `pipenv`. This [link](https://pipenv.pypa.io/en/latest/installation.html) guides you on how to do it.

```bash
pip install pipenv --user
```

Install packages in dev enviroment for testing, linting, formatting and pre-commit.

```bash
pipenv install --dev -r requirements.txt
```

## Run the DEV solution

This DEV deployment consis of:
- Mage Docker container running in port 6789
- Postgres db container used by Mage in port 5432
- Mlflow container running in port 5000 using a local SQLite database. The artifacts store is located in AWS S3.
- Report server, an container running Evidently AI UI in port 8001.
- A AWS S3 bucket containing several folder to store the input data and preprocessed data, the location to save the data for batch inference and its output, the datasets (current and reference) for monitoring performance and the reports.

### Run the following steps to deploy the dev solution.

Make sure you have the software installed and the right AWS User. Review items **Install the base software** and **Create a AWS User to deploy the Project** before proceeding.
1. Clone the repo
```bash
git clone https://github.com/edumunozsala/online-gaming-mlops-project
```
Go to dir `online-gaming-mlops-project`
```bash
cd online-gaming-mlops-project
```

2. **Modify the `.dev.env.bck` file and rename it to `.dev.env`**. Insert your AWS credentials and region. You do not need to set the others parameters, the default values are all OK.

3. Before executing any script, **You need to load the environment variables** with the AWS credentials and other parameters.

You can run:
```bash
set -a
source ./.dev.env
set +a
```
**Important**: You will have to load the env variables every time you start or open a session or terminal.

4. Run the command to create the AWS bucket and folders and to run the main containers (Mage, Mlflow and Postgres database):
```bash
make run-dev-env
```
Now, the script have **copied the data files in the local folder `data`** to the folders created in S3 automatically, by default the bucket_name is `mlops-gaming-dev`. 

if they are not in the bucket, You can run the `make` command to copy them automatically if you have aws cli installed:
```bash
make copy-files-s3
```
Or copy them manually to the S3 bucket.

5. You can access the applications through the following URLs:
- http://localhost:6789 - Mage
- http://localhost:5000 - Mlflow

6. Finally, you can start the report server container:
```bash
make run-report-server
```
7. Go to http://localhost:8001 to open the Evidently UI.

8. Once you finished you can destroy the AWS bucket and shutdown the containers:
```bash
make shutdown-dev-env
```
**Important**: Make sure that all components have been removed or you will still be charged for their use.

## Run the PROD solution

The PROD solutions deploys several AWS tools:
- ECS Cluster
- ECS Fargate services or containers for:
    - Mage
    - MlFlow
    - Report Server
- ECR repositories to registry the docker images
- Postgres RDS as database for Mage
- Load balancer
- VPC
- etcetera

### **Important: This deployment can incur relatively high costs, so we recommend using it for as long as necessary and then executing the removal of all deployed resources.**

### Run the following steps to deploy the prod solution.

Make sure you have the software installed and the right AWS User. Review items **Install the base software** and **Create a AWS User to deploy the Project** before proceeding.
1. Clone the repo
```bash
git clone https://github.com/edumunozsala/online-gaming-mlops-project
```
Go to dir `online-gaming-mlops-project`
```bash
cd online-gaming-mlops-project
```

2. **Modify the `.env.bck` file and rename it to `.dev.env`**. Insert your **AWS credentials**, **region** and your **local IP**, to configure netwrk access. You do not need to set the others parameters, the default values are all OK.

3. You need to **load the environment variables** with the AWS credentials and other parameters.

You can run:
```bash
set -a
source ./.env
set +a
```

4. First, we need to **create the AWS ECR repositories** for our container ipmages:
```bash
make deploy-ecr-prod
```

The output will show you the registry url,  that we need to log in to push the images. 
```text
container_repository_url = "http://**xxxxxxxxxxxx.dkr.ecr.yyyyyyy.amazonaws.com**/online-gaming-production-repository"
```
**Write down the container record xxxxxxx.dkr.ecr.yyyyyyyyy.amazonaws.com** as we will need it in the next step.

5. Set the env variable to the ECR registry:
```bash
export AWS_ECR_ACCOUNT="xxxxxxxxxxx.dkr.ecr.yyyyyyy.amazonaws.com"
```

6. Once, we have set the env variable `AWS_ECR_ACCOUNT`, we can create and push the container images to ECR:
```bash
make images-ecr-prod
```
7. Now, you can **copy the data files in the local folder `data`** to the folders created in S3 automatically, by default the bucket_name in PROD is `mlops-gaming-prod`. 

You can run the `make` command to copy them automatically if you have aws cli installed:
```bash
make copy-files-s3
```
Or copy them manually to the S3 bucket.

8. Our last step is to deploy all the AWS components:
```bash
make deploy-aws-prod
```
The output will show you the URL to access to the main application, Mage orchestrator.

9. Access the applications 

Go to the AWS Load balancer, and get the URL of the published balancer and click on it.
- URL : Mage Orchestrator
- URL:5000 : Mlflow
- URL:8001 : Evidently UI - Report App

10. Once you finished you can destroy the AWS components:
```bash
make destroy-ecr-prod
make destroy-aws-prod
```
**Important**: Make sure that all components have been removed or you will still be charged for their use.


