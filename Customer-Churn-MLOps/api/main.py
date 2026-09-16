from fastapi import FastAPI
import pandas as pd

import mlflow
import mlflow.sklearn

from mlflow import MlflowClient

from api.schemas import CustomerData


# ------------------------------------------------
# API configuration
# ------------------------------------------------

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Production-style API for predicting customer churn.",
    version="1.0.0"
)


# ------------------------------------------------
# MLflow configuration
# ------------------------------------------------

MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"

MODEL_NAME = "customer-churn-model"

mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)


# ------------------------------------------------
# Load Champion model
# ------------------------------------------------

MODEL_URI = f"models:/{MODEL_NAME}@champion"

model = mlflow.sklearn.load_model(
    MODEL_URI
)


# ------------------------------------------------
# Load Champion metadata
# ------------------------------------------------

client = MlflowClient(
    tracking_uri=MLFLOW_TRACKING_URI
)

champion_version = client.get_model_version_by_alias(
    name=MODEL_NAME,
    alias="champion"
)

champion_run = client.get_run(
    champion_version.run_id
)

classification_threshold = float(
    champion_run.data.params[
        "classification_threshold"
    ]
)


# ------------------------------------------------
# Root endpoint
# ------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Customer Churn Prediction API is running"
    }


# ------------------------------------------------
# Health endpoint
# ------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "model_version": champion_version.version,
        "threshold": classification_threshold
    }


# ------------------------------------------------
# Prediction endpoint
# ------------------------------------------------

@app.post("/predict")
def predict(customer: CustomerData):

    customer_dict = customer.model_dump()

    input_df = pd.DataFrame(
        [customer_dict]
    )

    probability = model.predict_proba(
        input_df
    )[0, 1]

    prediction = int(
        probability >= classification_threshold
    )

    return {
        "churn_probability": float(probability),
        "classification_threshold": classification_threshold,
        "prediction": prediction,
        "churn": "Yes" if prediction == 1 else "No"
    }