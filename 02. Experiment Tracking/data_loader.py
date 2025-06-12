import numpy as np
import pandas as pd

from typing import Optional
from sklearn.feature_extraction import DictVectorizer

_required_columns = ["lpep_dropoff_datetime", "lpep_pickup_datetime", "PULocationID", "DOLocationID", "trip_distance"]
  
def read_dataframe(filename: str, *more_files) -> pd.DataFrame:
    df = pd.read_parquet(filename, columns=_required_columns)

    for other_file in more_files:
        other_df = pd.read_parquet(other_file, columns=_required_columns)
        df = pd.concat([df, other_df], ignore_index=True)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    
    return df[["PU_DO", "trip_distance", "duration"]]


def encode_data(data: pd.DataFrame, features: list[str], target: str) -> tuple[np.ndarray, pd.Series, DictVectorizer]:
    dv = DictVectorizer()
    data_dicts = data[features].to_dict(orient='records')
    X = dv.fit_transform(data_dicts)
    y = data[target]

    return (X, y, dv)