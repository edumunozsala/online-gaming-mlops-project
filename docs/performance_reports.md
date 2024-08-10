# MLOps Zoomcamp Cohort 2024
# Project: Predict Online Gaming Behavior

## Workflow Orchestrator

### Performance Reports stage

We complete the monitoring strategy, generating performance reports using Evidently AI for the next topics:
    - Data Quality Report
    - Data Drift Report
    - Prediction Drift Report

Every night, this reports are saved to an S3 folder to share them with the Evidently UI service. Then, analysts and ML engineers can visualized them to check for any issues.

Flow diagram:

![Pipeline Performance Reports](../images/pipeline_performance_reports.png)

	- Load the reference and current data from an S3 folder
	- Prepare reference data for monitoring, removing the target column that is not present in the current data
	- Run a Summary Data Quality report, a Data Drift report and a Prediction Drift report
	- Upload and save the reports to an S3 folder. The Evidently UI will read and visualize them.
