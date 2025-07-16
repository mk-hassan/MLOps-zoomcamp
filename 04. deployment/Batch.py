#!/usr/bin/env python
# coding: utf-8
"""
prefect deploy \
  --name="batch-run" \
  --description="apply duration prediction model monthly in batch mode" \
  --pool="batch-runs-pool" \
  --cron="0 0 15 * *" \
  --timezone "Africa/Cairo" \
  --param taxi_type=green \
  --param run_id=d537fa0f7d34414396175da3712222e6 \
  Batch.py:run
"""
import uuid
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta

import mlflow
import mlflow.sklearn

import numpy as np
import pandas as pd

from prefect import flow, task, runtime, get_run_logger

from enums import TaxiType

@task(retries=2, retry_delay_seconds=5)
def load_data(month: int, year: int, taxi_type: TaxiType) -> pd.DataFrame:
    """
    Load and preprocess NYC taxi data for a given month and year from S3.

    Parameters
    ----------
    month : int
        The month of the data (1-12).
    year : int
        The year of the data (e.g., 2022).
    taxi_type : TaxiType
        The type of taxi to load (e.g., "green").

    Returns
    -------
    pd.DataFrame
        A cleaned DataFrame containing trip records with added duration,
        pickup-dropoff codes, and unique ride IDs.
    """
    logger = get_run_logger()

    data_source_uri = f"s3://tyc-taxi/green/{month}-{year:02d}.parquet"
    logger.info(f"start loading and formatting data from {data_source_uri}")

    df = pd.read_parquet(data_source_uri)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df['PU_DO'] = f"{df['PULocationID']}_{df['DOLocationID']}"
    df['ride_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    return df

@task(retries=3, retry_delay_seconds=10)
def apply_model(run_id: uuid, data: pd.DataFrame) -> np.ndarray:
    """
    Apply a trained MLflow model to the given taxi trip data.

    Parameters
    ----------
    run_id : uuid.UUID
        The MLflow run ID of the trained model to load.
    data : pd.DataFrame
        The input DataFrame containing preprocessed features, including
        'PU_DO' and 'trip_distance'.

    Returns
    -------
    np.ndarray
        The predicted values from the model.
    """
    logger = get_run_logger()
    logger.info(f"📦 Loading model from MLflow run ID: {run_id}")

    def load_model():
        return mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    data_dicts = data[["PU_DO", "trip_distance"]].to_dict(orient="records")
    model = load_model()
    predictions = model.predict(data_dicts)

    logger.info(f"📈 Generated predictions for {len(predictions)} records")
    return predictions

@task(retries=2, retry_delay_seconds=5)
def build_output(df: pd.DataFrame, predictions: np.ndarray) -> pd.DataFrame:
    """
    Construct a result DataFrame combining actual and predicted trip durations.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing trip details and actual durations.
    predictions : np.ndarray
        Predicted trip durations from the ML model.

    Returns
    -------
    pd.DataFrame
        A new DataFrame containing:
        - ride_id
        - lpep_pickup_datetime
        - PULocationID
        - DOLocationID
        - actual_duration
        - predicted_duration
        - diff (actual - predicted)
    """
    logger = get_run_logger()
    result = pd.DataFrame()

    result['ride_id'] = df['ride_id']
    result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    result['PULocationID'] = df['PULocationID']
    result['DOLocationID'] = df['DOLocationID']
    result['actual_duration'] = df['duration']
    result["predicted_duration"] = predictions
    result['diff'] = result['actual_duration'] - result['predicted_duration']

    logger.info("📊 Output DataFrame built successfully")
    logger.info(f"📉 Mean prediction error: {result['diff'].mean():.2f} minutes")
    return result

@task(retries=2, retry_delay_seconds=5)
def save_predictions(result: pd.DataFrame, outfile: str):
    result.to_parquet(f"s3://tyc-taxi/predictions/green/{outfile}.parquet", index=False)

@flow(name="batch-run", retries=3, retry_delay_seconds=5)
def run(taxi_type: str, run_id: str, date: datetime | None = None) -> None:
    logger = get_run_logger()
    if date is None:
        date = runtime.flow_run.scheduled_start_time
    
    prev_month = date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month 

    data = load_data(month, year, taxi_type)
    predictios = apply_model(run_id, data)
    result = build_output(data, predictios)
    save_predictions(result, f"{month}-{year}")

    logger.info("✅ Batch run completed successfully")

def parse_args() -> dict:
    accepted_taxi_type_values = [t.value for t in TaxiType]
    parser = argparse.ArgumentParser(description="Apply ML model to NYC taxi data")
    
    parser.add_argument("--month", type=int, required=True, help="Month of the trip data (1–12)")
    parser.add_argument("--year", type=int, required=True, help="Year of the trip data (e.g., 2023)")
    parser.add_argument(
        "--taxi-type",
        type=lambda s: s.lower(),
        choices=accepted_taxi_type_values,
        required=True,
        help="Taxi type: 'green' or 'yellow' (case-insensitive)"
    )
    parser.add_argument("--run-id", type=str, required=True, help="MLflow run ID for the model to use")

    return vars(parser.parse_args())

if __name__ == "__main__":
    args = parse_args()
    run(args["taxi_type"], args["run_id"], datetime(day=1, month=args["month"], year=args["year"]))
