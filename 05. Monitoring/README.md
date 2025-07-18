# ML Model Monitoring in Production

This repository contains a collection of notes on the critical aspects of monitoring machine learning models in a production environment. It's hard to train ML models, but it's even harder to build and maintain robust production services for these models. Over time, the quality of ML models can degrade, making monitoring an essential practice.

There are four fundamental areas to monitor to ensure the reliability and performance of a production ML system.

## 1. Monitoring Service Health

Service health monitoring is the most critical layer. If the service hosting the model is down, nothing else matters. This involves tracking the operational health of the web service or application that serves the model.

**Key Metrics:**
- **Uptime:** Is the service available and responding to requests?
- **Latency:** How long does it take for the service to process a request and return a prediction?
- **Memory/CPU Usage:** Is the service consuming resources efficiently, or are there leaks or bottlenecks?
- **Error Rates:** How many requests are failing?

## 2. Monitoring Model Health

Model health focuses on the performance of the machine learning model itself. This requires comparing the model's predictions to ground truth labels.

### General Metrics
These are standard performance metrics that can be applied to most models, such as accuracy, F1-score, etc.

### Specific Metrics
The choice of metrics is heavily dependent on the specific problem the model is solving:
- **Regression Problems:** Mean Absolute Error (MAE), Mean Absolute Percentage Error (MAPE).
- **Classification Problems:** Log-loss, Precision, Recall.
- **Ranking Problems:** Metrics specific to ranking algorithms, crucial for search engines or recommender systems.

## 3. Monitoring Data Health

Often, it's not feasible to get ground truth labels in real-time to measure model health directly. In these cases, monitoring the health of the input data serves as a powerful proxy. Issues in the model's performance often originate from problems with the input data.

**Key areas to monitor:**
- **Missing Values:** A sudden increase in the share of missing values for a feature.
- **Data Schema:** Changes in the data types of features (e.g., a feature that was a number is now a string).
- **Data Distribution:** Significant changes in the statistical distribution of a feature. This is known as **Data Drift**.

## 4. Data and Concept Drift

Drift is the phenomenon where the statistical properties of the data change over time, making the model's learned patterns less relevant. It's a primary reason for model performance degradation.

### Types of Drift

#### a. Data Drift (Covariate Shift)
- **What it is:** The distribution of the model's input features (X) changes.
- **Why it matters:** The model is forced to make predictions on data it has never seen during training.
- **Example:** A retail model trained on summer sales data performs poorly during the winter season.
- **Detection Metrics:** Population Stability Index (PSI), KL Divergence, Kolmogorov-Smirnov (KS) Test.

#### b. Concept Drift
- **What it is:** The relationship between the input features (X) and the target variable (Y) changes. The underlying meaning of the data has shifted.
- **Why it matters:** The model's fundamental assumptions are no longer valid.
- **Example:** The features defining a "spam" email change as spammers evolve their techniques.
- **Detection Metrics:** A decline in accuracy (if labels are available), or more advanced methods like the Drift Detection Method (DDM).

Monitoring for drift involves comparing the incoming production data against a stable, reference dataset (e.g., the training or validation set). A significant drift is a strong signal to investigate the data and potentially retrain the model.

## Other ML Metrics to Collect from Monitoring

Beyond the foundational metrics, several other types of monitoring can be crucial depending on the use case, associated risks, and available resources.

### 1. Performance by Segment
- **When to use:** When your model serves a diverse audience or deals with a wide variety of data objects.
- **What it is:** Instead of just looking at overall performance, you should collect quality metrics for specific segments or groups within your data. This helps ensure the model works well for all subgroups and not just for the majority.

### 2. Model Bias / Fairness
- **When to use:** Critical for models operating in sensitive domains like finance, healthcare, or hiring, where biased decisions can have serious consequences.
- **What it is:** This involves specifically monitoring the model's performance across different demographic groups (e.g., race, gender, age) to ensure that it is making fair and equitable decisions.

### 3. Outliers
- **When to use:** When the cost of a single, significant error is very high.
- **What it is:** This involves monitoring for input data that is unusual or far from the training data distribution, as these outliers can cause the model to make unpredictable or costly errors. These cases often require manual review by a human.

### 4. Explainability
- **When to use:** Important for systems where user trust is paramount, such as recommendation engines or financial loan applications.
- **What it is:** This involves monitoring the explanations for the model's predictions. For example, a recommendation system should be able to explain *why* it recommended a particular item, which helps build trust with users.
