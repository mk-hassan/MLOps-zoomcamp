
# MLOps Pipeline: NYC Taxi Trip Duration Prediction

This document outlines the end-to-end MLOps pipeline for training a regression model and using it for batch predictions on NYC Green Taxi trip data. The pipeline uses MLflow for experiment tracking, Prefect for workflow orchestration, and AWS S3 for data storage.

## Pipeline Execution Flow

The process is executed in the following sequence:

1.  **Model Training**: A regression model is trained and logged using MLflow.
2.  **Data Loading**: Raw taxi trip data is downloaded and moved to an S3 bucket.
3.  **Batch Prediction**: A Prefect workflow applies the trained model to the data in S3 and saves the predictions.
4.  **Historical Backfilling**: Prefect runs are created for past data to generate historical predictions.
5.  **Worker Execution**: A Prefect worker handles the execution of all scheduled and backfilled runs.

---

### 1. Model Training (`Model builder.ipynb`)

The first step is to train a simple scikit-learn regression model to predict trip durations.

-   **Functionality**:
    -   Loads historical NYC Green Taxi data.
    -   Preprocesses the data by calculating trip duration and creating feature combinations.
    -   Uses a `DictVectorizer` and `LinearRegression` model within a scikit-learn pipeline.
    -   Connects to an MLflow tracking server to log the model, parameters, and artifacts.
-   **Output**: A trained model is saved and tracked under the "nyc-taxi-experiment" in MLflow. The `run_id` from this process is essential for the batch prediction step.

---

### 2. Data Loading (`s3 data loader.py`)

This script is responsible for populating the S3 bucket with the raw data needed for batch processing.

-   **Functionality**:
    -   Downloads NYC Green Taxi trip data (in Parquet format) for a specified year and range of months from a public data source.
    -   Uploads each Parquet file to the `s3://tyc-taxi/green/` path in an S3 bucket.
-   **Usage**: This is typically run once to set up the data lake or whenever new historical data is needed.

---

### 3. Batch Prediction (`Batch.py`)

This script defines a Prefect workflow to automate the process of generating monthly predictions.

-   **Functionality**:
    -   The flow is designed to be deployed and run on a schedule (e.g., monthly).
    -   It loads the taxi data for the previous month from the S3 bucket.
    -   It fetches the trained model from the MLflow registry using a specific `run_id`.
    -   It applies the model to predict trip durations.
    -   The results, including the ride ID, actual duration, and predicted duration, are saved back to `s3://tyc-taxi/predictions/green/`.
-   **Deployment**:
    The workflow is deployed to a Prefect server using the following command, which sets up a cron-based schedule to run on the 15th of every month:
    ```bash
    prefect deploy \
      --name="batch-run" \
      --description="apply duration prediction model monthly in batch mode" \
      --pool="batch-runs-pool" \
      --cron="0 0 15 * *" \
      --timezone "Africa/Cairo" \
      --param taxi_type=green \
      --param run_id=d537fa0f7d34414396175da3712222e6 \
      Batch.py:run
    ```
    The `--param` flags set default values for the flow's parameters. These defaults are used when the flow is triggered by the cron schedule.

    *   `--param taxi_type=green`: Sets the default `taxi_type` to "green".
    *   `--param run_id=d537fa0f7d34414396175da3712222e6`: Sets the default MLflow `run_id`.

    These parameters can be overridden for specific runs, as demonstrated in the `Batch backfill.py` script, where a `date` parameter is explicitly provided in the API call to create a flow run. Any parameter included in the API call payload will take precedence over the default value set in the deployment.


---

### 4. Historical Backfilling (`Batch backfill.py`)

This utility script is used to generate predictions for past months that were not covered by the regular scheduled runs.

-   **Functionality**:
    -   It programmatically creates Prefect flow runs for a specified date range (e.g., from February 2022 to January 2023).
    -   For each month in the range, it calls the Prefect API to trigger a new run of the "batch-run" deployment.
    -   It waits for each run to complete before starting the next one, ensuring sequential processing.

---

### 5. Prefect Worker

To execute the scheduled deployments and backfill runs, a Prefect worker must be running and connected to the correct work pool.

-   **Functionality**:
    -   The worker polls the Prefect server for any new runs in its designated work pool (`batch-runs-pool`).
    -   When a run is available, the worker pulls the flow definition and executes the tasks, handling retries and logging as defined in the workflow.

