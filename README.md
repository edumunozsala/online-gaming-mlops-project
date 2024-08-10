# MLOps Zoomcamp Cohort 2024

# Project: Predict Online Gaming Behavior

## Problem Description
### Business Context
The online gaming industry thrives on high player engagement, which directly correlates with increased revenue through in-game purchases, subscription fees, and sustained player base growth. Player engagement is a critical metric that impacts user retention, word-of-mouth promotion, and overall game popularity. Analyzing and predicting player engagement can help gaming companies develop strategies to enhance player experience, retain more players, and optimize revenue streams.

### Problem Statement
The **objective is to analyze the provided player data to predict the engagement level of the players**  ('High', 'Medium', 'Low'). Given features about the player and his gaming sessions' statistics, we'll try to forecast the engagement level of that player, the likelihood of continuing playing or leaving the platform. Using these predictions, the goal is to identify actionable insights and strategies to improve player engagement, thereby enhancing player retention and increasing revenue from in-game purchases and other monetization strategies.

**Return on Investment (ROI) and Benefits of higher Engagement**
* Increased Revenue: By enhancing player engagement, the company can boost in-game purchases and subscription renewals.
* Reduced Churn Rate: Improved engagement leads to higher retention, reducing the cost associated with acquiring new players.
* Customer Lifetime Value (CLV): Higher engagement generally increases the lifetime value of players, leading to long-term profitability.

### Approach Using Machine Learning

The next picture ilustrate the workflows or pipelines we have built using Mage AI to execute the relevant steps in a MLOps workflow to solve our problem:

![MLOps Workflow and Pipelines](images/flows.drawio.png)

- In our scenario, data about players and their playing behavior are collected every day.
- From the collected data, we can prepare and train an ML model to predict a player's engagement level.  
- Then, each day in the evening, we run a batch inference process to obtain a prediction of each player's engagement level and this data is stored in a shared, presistent cloud storage. 
- At the end of the week, we can compile the actual truth or target value based on the level of engagement the player has shown during the week. This means that we can have new training data.
- Every weekend, we can retrain our model and record a new version, a candidate model.
- Every Monday, we select the best model, compare the candidate model with the production model, establish the new best model and move it to production.
- Every night we run performance tests to check for problems related to data or model drift. If any of the relevant tests fail, we can force a retraining step.
- Some performance monitoring reports are also run every day. These are saved, and the ML team will have access to a dashboard and reports to keep up to date on model performance.


#### Data Understanding and Preprocessing
* Data Collection: Gather the dataset with fields about the gamers and their gaming behavior on the platform.
* Data Cleaning: Handle missing values, remove duplicates, and correct any inconsistencies in the data.
* Feature Engineering: Create or remove  features if necessary.
* Encode categorical variables (e.g., Gender, Location, GameGenre, EngagementLevel) using techniques like one-hot encoding or label encoding.
* Data Splitting: Divide the data into training, validation, and test sets to evaluate the model's performance.

#### Model Selection and Training
* Algorithm Choice: Consider various machine learning algorithms such as:
	- Logistic Regression: For baseline performance and interpretability.
	- Random Forest: For handling complex interactions and providing feature importance.
	- Gradient Boosting Machines (GBM): For high accuracy and robustness.
	- Neural Networks: If the data is sufficiently large and complex.

* Model Training: Train multiple models and perform hyperparameter tuning using techniques like cross-validation to optimize model performance.
* Feature Importance Analysis: Identify which features are most influential in predicting player engagement.

**Important**: We will not focus in the machine learning model and how to get the better approach. Therefore, **we will simplify tasks such as feature engineering, model selection, and hyperparameter tuning**. This project is about MLOps, and we will try to provide a solution to orchestrate the several pipelines this kind of problem requires. Consecuently, **we will not create any new feature**, **we have already chosen the model Gradient Booster** and we will not perform a hyperparameter tuning job, **we have selected some standard parameters**.

#### Model Evaluation
* Metrics:
	- Accuracy: Overall correctness of the model.
	- Precision, Recall, and F1-Score: For evaluating the balance between precision and recall, especially for the 'High' engagement category.
	- Confusion Matrix: To understand the types of errors the model is making.

#### Deployment and Monitoring
* Model Deployment: Deploy the best-performing model into the production environment.
* Continuous Monitoring: Track model performance over time to ensure it remains accurate and relevant, retraining as necessary.

### Business Objective and Optimization

Strategies to Improve Player Engagement
* In-Game Purchases: Recommend items or upgrades that align with the player's gaming behavior and preferences.
* Engagement Level-Based Campaigns: Create specific campaigns for 'Medium' and 'Low' engagement players to re-engage them with tailored offers, rewards, and incentives.
* Retention Programs: Design loyalty programs for 'High' engagement players to maintain their interest and reward their loyalty.
* In-Game Events and Achievements: Organize special in-game events and introduce new achievements to keep the game fresh and engaging.

## Dataset: Predict Online Gaming Behavior Dataset

This dataset is available on Kaggle website: https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset/data.


#### Overview:
This dataset captures comprehensive metrics and demographics related to player behavior in online gaming environments. It includes variables such as player demographics, game-specific details, engagement metrics, and a target variable reflecting player retention.

**Features**:
- PlayerID: Unique identifier for each player.
- Age: Age of the player.
- Gender: Gender of the player.
- Location: Geographic location of the player.
- GameGenre: Genre of the game the player is engaged in.
- PlayTimeHours: Average hours spent playing per session.
- InGamePurchases: Indicates whether the player makes in-game purchases (0 = No, 1 = Yes).
- GameDifficulty: Difficulty level of the game.
- SessionsPerWeek: Number of gaming sessions per week.
- AvgSessionDurationMinutes: Average duration of each gaming session in minutes.
- PlayerLevel: Current level of the player in the game.
- AchievementsUnlocked: Number of achievements unlocked by the player.

**Target Variable:**
- EngagementLevel: Indicates the level of player engagement categorized as 'High', 'Medium', or 'Low'.

**Potential Applications**:
* Predictive modeling of player retention and engagement patterns.
* Analysis of factors influencing player behavior and game performance.
* Optimization of game design, marketing strategies, and player experience enhancements.

**Usage**:
This dataset is suitable for exploring patterns in online gaming behavior, developing machine learning models for player engagement prediction, and conducting research in gaming analytics.

## Experiment tracking and Model Registry

![Experiment Tracking and Model Management with MLFlow ](images/MLflow-Logo.svg)

Mlflow is the platform of choice to track our training and evaluation stages. We will train a well-known scikit learn model and use Mlflow's Autolog feature to collect all relevant metrics during training. But we will also record evaluation metrics from the test data set.

Once our model is trained, we will log it (automatic logging is enabled) and it will be labeled as a candidate model. We have also built a pipeline to search for the best model and if the new model performs better than the current model, it will become the new production model and will be loaded for future predictions.

An mlflow server is deployed to track experiments and models, using S3 as a remote storage location. This is a very convenient way to share the model and artifacts with future instances of model deployment

You can read more detaiuls and see the pipeline in this [link]

## Workflow and process description

### Workflow Orchestrator
![Mage AI Workflow Orchestrator](images/mage-ai-icon.png)

We rely on Mage AI as our pipeline orchestrator, building a pipeline for each flow and a trigger to run the pipeline when it is required. Mage.ai, an open-source data engineering tool, combines the features of a Python library with workflow automation capabilities. It enables data professionals to utilize Python for a wide range of tasks, streamlining processes from data preparation to analysis and deployment.

#### IMAGE PIPELINES

### Data preparation stage:  

	- Download and read the available training CSV data file from a AWS S3 folder
	- Clean and transform the data
	- Upload and save the processed dataset into an AWS S3 folder
    - Upload and save the players features into an AWS S3 folder


Detailed information and pipeline diagram [HERE](docs/data_preparation.md)

### Training stage:



	- Download and read the processed CSV dataset from a AWS S3 folder
	- Split the dataset into a train and test set
	- Set the model parameters in a configuration dict
	- Build a Scikit learn pipeline containing:
		- Transformer to scale the numerical features
		- Transformer to encode the categorical features
		- Create a Gradient Boosting Classifier with a predefined set of hyperparameters
	- Train or fit the pipeline and model to learn the parameters:
		- Keep track of the experiment, loging the metrics for training and testing using Mlflow
		- Register the model as a candidate model in the Mlflow server
	- Upload and save the train and test set as our reference dataset for performance monitoring


Detailed information and pipeline diagram  [HERE](docs/training_workflow.md)

### Best model selection stage:

	- Search for the model, the one with the highest value of our selected metric
	- Promote the best model as the production model, setting the alias. This one will be loaded for inference.
	- Load the best model an save it in a Global Data Product component in Mage

Detailed information and pipeline diagram [HERE](docs/model_selection.md)

### Batch inference:

	- Download and read the processed CSV dataset from a AWS S3 folder
	- Prepare the dataset, apply the same transformation that we execute in the training stage.
	- Load the model from the Global Data Product
	- Make predictions on the dataset
	- Upload and save predictions to the destination folder in S3
	- Upload and save the input data to the monitoring folder in S3. It will become the current data for performance monitoring. 

Detailed information and pipeline diagram [HERE](docs/batch_inference.md)

### Online inference:

	- Load the model from the Global Data Product
	- Make a prediction for a list of inputs via Trigger API.

Detailed information and pipeline diagram [HERE](docs/online_inference.md)

### ML Retraining:
	This pipeline is triggered by code from the performance monitoring pipeline to retraining the model. IT simply triggers the Training pipeline.

	- Just one block to trigger the Training pipeline

### Performance Monitoring:

	- Load the reference and current data from an S3 folder
	- Run a Data Drift Test suite to check if any relevant column  has drifted.
	- Run a Prediction Drift Test suite to check if the prediction column  has drifted.
	- If the share of drifted columns is higher than 0.3 or prediction is drifted or AvgSessionDurationMinutes is drifted or SessionsPerWeek is drifted, then a retraining activated

Detailed information and pipeline diagram [HERE](docs/performance_monitoring.md)

### Performance Reports:

	- Load the reference and current data from an S3 folder
	- Prepare reference data for monitoring, removing the target column that is not present in the current data
	- Run a Summary Data Quality report, a Data Drift report and a Prediction Drift report
	- Upload and save the reports to an S3 folder. The Evidently UI will read and visualize them.

Detailed information and pipeline diagram [HERE](docs/performance_reports.md)

## Model Deployment

As we've mentioned in a previous section, we deploy our model on the Mage platform for both scenarios:

* Batch Inference: the preferred method. We want to predict the player's engagement level every day, then, business analyst will take actions based on this predicted behavior. More [info](docs/batch_inference.md) about this pipeline or process.

* Online Inference: A pipeline triggered via API. We also provide a POST API request. More [info](docs/online_inference.md) about this pipeline.


## Model Monitoring
![Performance Monitoring framework Evidently AI](images/evidentlyai-logo.png)

Evidently AI helps run ML in production reliably. Evidently gives visibility into how ML models behave in the wild and helps detect and debug issues, from data drift to segments of low performance. All with an open-source approach: extensible, open, and built together with the community. 

For this project we use Evidently AI and have considered two actions in the surveillance strategy:

* **Performance Monitoring**: We run some tests on the current data (vs reference data), check the failure tests and retrain a model if any of the predefined conditions fails. You can read about these conditions and review the pipeline [here](docs/performance_monitoring.md)

* **Performance Reports**: Every day data is collected and then we run some reports on performance to visualize the evolution of some relevant metrics. The reports to execute: Data Quality, Data Drift and Prediction Drift. More information and the pipeline [here](docs/performance_reports.md)

And **you can navigate to our Evidently UI** (This URL depends on how the solutions is deployed, you can read it later in the Instalation guide) and visualize a main **Dashboard** where you can easily evaluate the data quality and performance. You can also navigate to individual **reports** to go deeper into detailed information like columns drifted, correlations, etc.

## Cloud

![I-a-C Tool Terraform](images/terraform.225x256.png) 						![Amazon Web Services](images/aws-logo.png)

This MLOps Workflows and solution can be deployed to Amazon Web Services using Terraform. Terraform is an Infraestructure-as-Code tool, used primarily by DevOps teams to automate various infrastructure tasks. The provisioning of cloud resources is one of the main use cases of Terraform. It’s a cloud-agnostic, open-source provisioning tool written in the Go language and created by HashiCorp.

The production solution includes the following architecture:


![Production Architecture](images/diagram-flows.drawio.png)


* Amazon ECS: Fargate containers distribuited in 2 Services:

- Mage, the Workflow Orchestrator: runing in a 4096 CPU and 8192 GB container and connected to a Amazon RDS PostGres database. And accesing to several S3 folder containing the CSV dataset and the transformed version depending on the stage.

- Mlflow, the experiment tracker and model registry: A Fargate service runing a Mlflow container, small size 1024 CPU and 2048 GB. The info is stored in a local SQLite to reduce cost and complexity. The artifacts are stored in a folder in an S3 bucket.

- Evidently UI: A new task and Fargate service, runing in 1024 CPU and 2048 GB Mem. It collects reports from an S3 folder and generate the reports and dashboard when it starts up. 

* Amazon Load Balancer: An application balancer to route the traffic to one of the three containers.

* Amazon VPC: All components are protected inside a VPC to control access and networking.
	-	Several subnets and security groups to keep the solution secure.
* 

## Best practices

### Unit testing

We have include some unit test to show how to fit them into this kind of project. Once we have created a DEV enviroment, you can install pytest (instruction are included in the following section) and run the test to check if things are working fine:

```bash
pytest tests/unit_tests.py

```

All relevant code and the functions we use in the Mage pipelines have been included in the package utils, that's why we only check that folder. And the results of the pytest execution is:
```
========================================================================================= test session starts =========================================================================================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
rootdir: /workspaces/online-gaming-mlops-project
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 3 items                                                                                                                                                                                     

tests/unit_tests.py ...                                                                                                                                                                         [100%]

========================================================================================== 3 passed in 7.19s ==========================================================================================
```

### Integration test

We are going to test our mlflow container as a sample on how to apply integration tests. 

* Set the environment variables
```bash
set -a
source ./.dev.env
set +a
```

if you do not want to build or rebuild the container image set the env variable to `LOCAL_IMAGE_NAME`.

And now we can run the test using the `make` command and the task defined in the `Makefile`:
```bash
make scripts/integration-tests
```

The content of this section of the `Makefile` is:
```make
integration-tests:
			LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash ./scripts/integration-test.sh

```
Output:
```text
LOCAL_IMAGE_NAME=mlflow_tracker_5000 bash ./scripts/integration-test.sh
No need to build image. Runing container
[+] Running 2/2
 ✔ Network online-gaming-mlops-project_app-network  Created                                                                                                                                                                                  0.1s 
 ✔ Container mlflow_tracker_5000                    Started                                                                                                                                                                                  0.5s 
pwd
Loading .env environment variables...
============================================================================================================== test session starts ===============================================================================================================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
rootdir: /workspaces/online-gaming-mlops-project
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 0 items                                                                                                                                                                                                                                

============================================================================================================= no tests ran in 0.00s ==============================================================================================================
ERROR: file or directory not found: ./tests/integration_tests.py

mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [11] [INFO] Starting gunicorn 22.0.0
mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [11] [INFO] Listening at: http://0.0.0.0:5000 (11)
mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [11] [INFO] Using worker: sync
mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [12] [INFO] Booting worker with pid: 12
mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [13] [INFO] Booting worker with pid: 13
mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [14] [INFO] Booting worker with pid: 14
mlflow_tracker_5000  | [2024-08-10 16:38:57 +0000] [15] [INFO] Booting worker with pid: 15
[+] Running 2/2
 ✔ Container mlflow_tracker_5000                    Removed                                                                                                                                                                                 10.5s 
 ✔ Network online-gaming-mlops-project_app-network  Removed                                                                                                                                                                                  0.1s 
make: *** [Makefile:8: integration-tests] Error 4
@edumunozsala ➜ /workspaces/online-gaming-mlops-project (main) $ 

@edumunozsala ➜ /workspaces/online-gaming-mlops-project (main) $ 
@edumunozsala ➜ /workspaces/online-gaming-mlops-project (main) $ make integration-tests
LOCAL_IMAGE_NAME=mlflow_tracker_5000 bash ./scripts/integration-test.sh
+ [[ -z '' ]]
++ dirname ./scripts/integration-test.sh
+ cd ./scripts
+ export MLFLOW_PORT=5000
+ MLFLOW_PORT=5000
+ export MLFLOW_ENDPOINT_URL=http://127.0.0.1:5000
+ MLFLOW_ENDPOINT_URL=http://127.0.0.1:5000
+ export BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
+ BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
+ export MLFLOW_EXPERIMENT_NAME=online_gaming_1
+ MLFLOW_EXPERIMENT_NAME=online_gaming_1
+ export DEFAULT_ARTIFACT_ROOT=s3://mlops-zoomcamp-gaming
+ DEFAULT_ARTIFACT_ROOT=s3://mlops-zoomcamp-gaming
+ export DEFAULT_ARTIFACTS_DESTINATION=s3://mlops-zoomcamp-gaming
+ DEFAULT_ARTIFACTS_DESTINATION=s3://mlops-zoomcamp-gaming
+ '[' mlflow_tracker_5000 == '' ']'
+ echo 'No need to build image. Runing container'
No need to build image. Runing container
+ docker compose up -d mlflow
[+] Running 2/2
 ✔ Network online-gaming-mlops-project_app-network  Created                                                                                                                                                                                  0.1s 
 ✔ Container mlflow_tracker_5000                    Started                                                                                                                                                                                  0.6s 
+ sleep 15
+ echo /workspaces/online-gaming-mlops-project/scripts
/workspaces/online-gaming-mlops-project/scripts
+ pipenv run pytest ./tests/integration_tests.py
Loading .env environment variables...
============================================================================================================== test session starts ===============================================================================================================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
rootdir: /workspaces/online-gaming-mlops-project
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 0 items                                                                                                                                                                                                                                

============================================================================================================= no tests ran in 0.00s ==============================================================================================================
ERROR: file or directory not found: ./tests/integration_tests.py

+ ERROR_CODE=4
+ '[' 4 '!=' 0 ']'
+ docker compose logs
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [11] [INFO] Starting gunicorn 22.0.0
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [11] [INFO] Listening at: http://0.0.0.0:5000 (11)
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [11] [INFO] Using worker: sync
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [12] [INFO] Booting worker with pid: 12
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [13] [INFO] Booting worker with pid: 13
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [14] [INFO] Booting worker with pid: 14
mlflow_tracker_5000  | [2024-08-10 16:42:19 +0000] [15] [INFO] Booting worker with pid: 15
+ docker compose down
[+] Running 2/2
 ✔ Container mlflow_tracker_5000                    Removed                                                                                                                                                                                 10.4s 
 ✔ Network online-gaming-mlops-project_app-network  Removed                                                                                                                                                                                  0.1s 
+ exit 4
make: *** [Makefile:8: integration-tests] Error 4
@edumunozsala ➜ /workspaces/online-gaming-mlops-project (main) $ make integration-tests
LOCAL_IMAGE_NAME=mlflow_tracker_5000 bash ./scripts/integration-test.sh
+ [[ -z '' ]]
++ dirname ./scripts/integration-test.sh
+ cd ./scripts
+ export MLFLOW_PORT=5000
+ MLFLOW_PORT=5000
+ export MLFLOW_ENDPOINT_URL=http://127.0.0.1:5000
+ MLFLOW_ENDPOINT_URL=http://127.0.0.1:5000
+ export BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
+ BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
+ export MLFLOW_EXPERIMENT_NAME=online_gaming_1
+ MLFLOW_EXPERIMENT_NAME=online_gaming_1
+ export DEFAULT_ARTIFACT_ROOT=s3://mlops-zoomcamp-gaming
+ DEFAULT_ARTIFACT_ROOT=s3://mlops-zoomcamp-gaming
+ export DEFAULT_ARTIFACTS_DESTINATION=s3://mlops-zoomcamp-gaming
+ DEFAULT_ARTIFACTS_DESTINATION=s3://mlops-zoomcamp-gaming
+ '[' mlflow_tracker_5000 == '' ']'
+ echo 'No need to build image. Runing container'
No need to build image. Runing container
+ docker compose up -d mlflow
[+] Running 2/2
 ✔ Network online-gaming-mlops-project_app-network  Created                                                                                                                                                                                  0.1s 
 ✔ Container mlflow_tracker_5000                    Started                                                                                                                                                                                  0.6s 
+ sleep 15
+ echo /workspaces/online-gaming-mlops-project/scripts
/workspaces/online-gaming-mlops-project/scripts
+ pipenv run pytest ../tests/integration_tests.py
Loading .env environment variables...
============================================================================================================== test session starts ===============================================================================================================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0
rootdir: /workspaces/online-gaming-mlops-project
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 3 items                                                                                                                                                                                                                                

../tests/integration_tests.py ...                                                                                                                                                                                                          [100%]

================================================================================================================ warnings summary ================================================================================================================
../../../home/codespace/.local/share/virtualenvs/online-gaming-mlops-project-uvzvqTV3/lib/python3.10/site-packages/mlflow/utils/requirements_utils.py:20
  /home/codespace/.local/share/virtualenvs/online-gaming-mlops-project-uvzvqTV3/lib/python3.10/site-packages/mlflow/utils/requirements_utils.py:20: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
    import pkg_resources  # noqa: TID251

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================================================================================================== 3 passed, 1 warning in 7.90s ==========================================================================================================
+ ERROR_CODE=0
+ '[' 0 '!=' 0 ']'
+ docker-compose down
[+] Running 2/2
 ✔ Container mlflow_tracker_5000                    Removed                                                                                                                                                                                 10.4s 
 ✔ Network online-gaming-mlops-project_app-network  Removed 
```

## Prerequisites to run the project demo
1. Docker:
	You need to install docker for your OS. [Link to installation](https://docs.docker.com/engine/install/) 
2. Git
	You can install Git from this [link](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Terraform
	Installation: https://developer.hashicorp.com/terraform/install

**Note:** You can use a GitHub Codespace to run this demo, it's installed both Docker and Git. You can watch [this video](https://youtu.be/XOSUt8Ih3zA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15) for instructions on how to prepare a Codespace.

## Instruction to prepare your GCP for this demo
1. Create a GCP Project 
	Our example Project_id = 'gdelt-project-data'
2. Create a service account in the project, grant it the permissions:
	- Storage Admin
	- Bigquery Admin
	- Service Usage Admin
	- Service Management Administrator
    You can include more permissions if you want to expand this project for a future use.
3. Create an access key JSON file, you need to download its private key file. 
	- This key file will be used to authenticate requests to GCP services.
	- Select the service account you just created to view its details, Click on the "Keys" tab and then click the "Add Key" button.
	- Select the "JSON" key type and click "Create" to download the private key file. 
	  **Rename your json file to `gdelt-project-credentials.json` and copy it to the mage directory `mage-gdelt` and the terraform folder `terraform`**

## To run the demo project
1. Clone the repo to your local folder or to a VM or Github Codespace
```bash
git clone https://github.com/edumunozsala/GDELT-Events-Data-Eng-Project.git
```

2. Copy the json file with the GCP service account credentials to the folders `terraform` and `mage-gdelt` with the filename `gdelt-project-credentials.json`
3. Create the GCP objects with Terraform

**You can modify the file `variables.tf`, if you want to change the names of the GCP object to create for this demo. You will also need to modify the `.env`**

4.  `cd` into the terraform directory.
5. Initialize terraform folder

```bash
terraform init
```
6. To show changes to apply:

```bash
terraform plan
```
7. To create or update infrastructure:

```bash
terraform apply
```
**Our terraform script enable the BigQuery API**

8. `cd` into mage directory `mage-gdelt`
9. Rename the file `dev.env` to `.env` and review the parameters.

	**Values you can change: the buckets name and dataset you create with terraform
	but you must not change PROJECT_NAME, SPARK_MASTER_HOST, GOOGLE_APPLICATION_CREDENTIALS, ENV**
	
		Days to collect: you can change this value if you want to collect more or less data. Be carefull with the value you include.

10. Build the container
	`docker compose build`
11. Run the contaier
`docker compose up`
12. Open Mage UI in your web browser.
	If you are running it locally go to http://localhost:6789, but this link may differ depending on where and how you run the docker container.
13. To run the whole workflow you just need to open the `load_bronze_gcs` pipeline and click the run once button.
![Pipelines](images/pipelines.png)

Click on run@nce:
![Load_bronze_gcs](images/run_load_bronze_gcs.png)

Go to logs to watch how the process advance, when a pipeline finish the next one is automatically launch. Open every pipeline to see the logs.

**It takes about 15 minutes to download and move to Cloud Storage all the csv files, 4,700, and about 10 minutos to process them and create the dataframes and tables.**

14. Once the workflow has finished you can go to the dashboard on [Looker Studio](https://lookerstudio.google.com/reporting/f1018a56-01ea-422b-8c40-ea9b1a87ee01)

Some Visualizations:

**TOTAL EVENTS**
![Total amount of events, articles and mentions](images/total_events.png)

![Events by Country](images/events_by_country.png)


**IMPORTANT**: When you are done you can destroy the GCP bjects :

```bash
terraform destroy
```



