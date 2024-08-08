# MLOps Zoomcamp Cohort 2024
# Project: Predict Online Gaming Behavior

## Predict Online Gaming Behavior
## Workflow Orchestrator

### Model Selection stage

This pipeline simply search for the best model, between candidate and production models, based on the metric selected, in our case the precision score. And then, the best mode becomes the production model, setting an aliases, and is registered in a Global Data Product artifact in Mage.

The following inferences will use the new production model.

Flow diagram:

![Pipeline Best Model Selection](images/pipeline_select_best_model.png)

	- Search for the model, the one with the highest value of our selected metric
	- Promote the best model as the production model, setting the alias. This one will be loaded for inference.
	- Load the best model an save it in a Global Data Product component in Mage

