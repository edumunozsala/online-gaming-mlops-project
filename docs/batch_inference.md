# MLOps Zoomcamp Cohort 2024
# Project: Predict Online Gaming Behavior

## Workflow Orchestrator

### Batch Inference stage

The platform collects the data about players and gaming behaviour every day and runs a batch inference once a day to predict the engagement level. Consecuently, these predictions are analyzed and some actions will be taken. This inference process is the main one for our problem.

Flow diagram:

![Pipeline Batch Inference](../images/pipeline_batch_inference.png)

	- Download and read the processed CSV dataset from a AWS S3 folder
	- Prepare the dataset, apply the same transformation that we execute in the training stage.
	- Load the model from the Global Data Product
	- Make predictions on the dataset
	- Upload and save predictions to the destination folder in S3
	- Upload and save the input data to the monitoring folder in S3. It will become the current data for performance monitoring. 
