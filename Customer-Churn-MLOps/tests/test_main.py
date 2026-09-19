from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["message"] == "Customer Churn Prediction API is running"


def test_health():
    response=client.get("/health")

    assert response.status_code==200

    data=response.json()

    assert data["status"]=="healthy"
    assert data["model"]=="customer-churn-model"
    assert "model_version" in data
    assert "threshold" in data


def test_prediction():

    customer={
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 2,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 95.5,
        "TotalCharges": 190.5
    }

    response=client.post("/predict",json=customer)

    assert response.status_code==200

    data=response.json()

    assert "churn_probability" in data
    assert "classification_threshold" in data
    assert "prediction" in data
    assert "churn" in data

    assert 0<=data["churn_probability"]<=1
    assert data["prediction"] in [0,1]
    assert data["churn"] in ["Yes","No"]

def test_invalid_prediction_input():
    customer={
        "gender":"Female",
        "SeniorCitizen":"hello"
    }

    response=client.post("/predict",json=customer)

    assert response.status_code==422

