import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "churn_model.joblib"

def test_model_load():
    model = joblib.load(MODEL_PATH)
    assert model is not None


def test_model_prediction():
    model = joblib.load(MODEL_PATH)

    sample = [[
        1,  # Gender
        0,  # Senior Citizen
        1,  # Partner
        0,  # Dependents
        24, # Tenure Months
        1,  # Phone Service
        1,  # Multiple Lines
        1,  # Internet Service
        1,  # Online Security
        1,  # Online Backup
        1,  # Device Protection
        1,  # Tech Support
        1,  # Streaming TV
        1,  # Streaming Movies
        1,  # Contract
        1,  # Paperless Billing
        1,  # Payment Method
        70, # Monthly Charges
        1680, # Total Charges
        3000  # CLTV
    ]]

    prediction = model.predict(sample)

    assert prediction is not None