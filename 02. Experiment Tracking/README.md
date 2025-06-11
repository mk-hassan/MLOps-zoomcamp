# ML Experiment tracking with ML flow

## Prepare local environment

```sh
# create conda environment and install required packages
conda create -n new-env-name 
conda activate new-env-name 
pip install -r requirements.txt
```

## Running MLFlow Notes
```python
mlflow ui --backend-store-uri="sqlite:///mlflow.db"
```
this command will create mlflow.db file, for in-memory sqlite database, if --backend-store-uri property not specified `mlflow ui`
will create a local file system based store inside `miruns` repository contains the runs and the associated data.

A problem I faced that, initialized `mlflow ui` without specifying the database and then inside the code tried to connect to `sqlite:///mlflow.db` which created a new file for the database but the `UI` sees the local file system `mlruns` repository. Hence I couldn't see the Runs or anyThing.

## Notes after experimenting
1. Compare the RUNs and discover the plots so that you know which HPs are more corralted with the metrics.
2. You needn't always the best model with the lowest error, but also the take a look at the training time (Duration), and the size of the model. Maybe you want to go with another model that doesn't achieve the lowest error but it has a lower complexity and hence it can run faster.
3. When running mlflow with the autolog functionality, it records lots of artifacts like feature importance, model itself so you can load it and use it later in predictions, dependancies, and great info on how to run the model.