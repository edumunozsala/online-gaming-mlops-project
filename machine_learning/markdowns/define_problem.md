## Business Context

The online gaming industry thrives on high player engagement, which directly correlates with increased revenue through in-game purchases, subscription fees, and sustained player base growth. Player engagement is a critical metric that impacts user retention, word-of-mouth promotion, and overall game popularity. Analyzing and predicting player engagement can help gaming companies develop strategies to enhance player experience, retain more players, and optimize revenue streams.

### Problem Statement
The objective is to analyze the provided player data to predict the engagement level of the players  ('High', 'Medium', 'Low'). Given features about the player and his gaming sessions' statistics, we'll try to forecast the engagement level of that player, the likelihood of continuing playing or leaving the platform. Using these predictions, the goal is to identify actionable insights and strategies to improve player engagement, thereby enhancing player retention and increasing revenue from in-game purchases and other monetization strategies.

- In our scenario, data about about the players and their gaming behavior is collected every day. 
- Then, dayly at night, we run a batch inference process to get a predicted Engagement Level for every player and this data is stored in a shared and presistent storage on the cloud. 
- At the end of the week, we can collect the ground truth or actual target value, based on the engagement level the player has shown during the week. This means we may have new training data.
- Every weekend, we can retrain our model and register a new version, a candidate model.
- Every monday, we select the best model, comparing candidate/s model vs production model and we set the new best model and promote it to production.
- We run performace tests every night to check issues about data or model drift. If any of the relevent tests fails then we can force a retraining stage.
- Some performance monitoring reports are also executed every day. They are saved, and the ML team will access to a dashboard and the reports to keep up to date of the model performance.

### Approach Using Machine Learning
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
