# MLOps Zoomcamp Cohort 2024
# Project: Predict Online Gaming Behavior

## Predict Online Gaming Behavior
## Workflow Orchestrator

### Online Inference stage

As part of our solution, we also include a pipeline to run predictions on an array of inpuit data. This pipeline is triggered by an API that can be invoked to get the predictions.

Here is an example:
```bash
curl --location 'http://localhost:6789/api/runs' \
--header 'Authorization: Bearer 2a48283d377a4f1ca9297d19cf4cd40f' \
--header 'Content-Type: application/json' \
--header 'Cookie: lng=en' \
--data '{
    "run": {
        "pipeline_uuid": "online_inference",
        "block_uuid": "online_prediction",
        "variables": {
            "inputs": [{
    "Age": 43,
    "Gender": "Male",
    "Location": "Other",
    "GameGenre": "Strategy",
    "PlayTimeHours": 16.27,
    "InGamePurchases": "No",
    "GameDifficulty": "Medium",
    "SessionsPerWeek": 6,
    "AvgSessionDurationMinutes": 108,
    "PlayerLevel": 79,
    "AchievementsUnlocked": 25
			}]
        }
    }
}'
```

Flow diagram:

![Pipeline Online Inference](images/pipeline_online_inference.png)

	- Load the model from the Global Data Product
	- Make a prediction for a list of inputs via Trigger API.
