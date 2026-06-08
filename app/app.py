
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD FILES
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "churn_model.joblib"
ENCODER_PATH = BASE_DIR / "models" / "encoders.joblib"

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)

# =====================================================
# TITLE
# =====================================================

st.title("📊 Customer Churn Prediction System")

st.markdown(
    """
    Predict whether a customer is likely to churn using
    a trained XGBoost machine learning model.
    """
)

# =====================================================
# SIDEBAR INPUTS
# =====================================================

st.sidebar.header("Customer Information")

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

senior = st.sidebar.selectbox(
    "Senior Citizen",
    ["Yes", "No"]
)

partner = st.sidebar.selectbox(
    "Partner",
    ["Yes", "No"]
)

dependents = st.sidebar.selectbox(
    "Dependents",
    ["Yes", "No"]
)

tenure = st.sidebar.slider(
    "Tenure Months",
    min_value=0,
    max_value=72,
    value=12
)

phone_service = st.sidebar.selectbox(
    "Phone Service",
    ["Yes", "No"]
)

multiple_lines = st.sidebar.selectbox(
    "Multiple Lines",
    ["Yes", "No", "No phone service"]
)

internet_service = st.sidebar.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

online_security = st.sidebar.selectbox(
    "Online Security",
    ["Yes", "No", "No internet service"]
)

online_backup = st.sidebar.selectbox(
    "Online Backup",
    ["Yes", "No", "No internet service"]
)

device_protection = st.sidebar.selectbox(
    "Device Protection",
    ["Yes", "No", "No internet service"]
)

tech_support = st.sidebar.selectbox(
    "Tech Support",
    ["Yes", "No", "No internet service"]
)

streaming_tv = st.sidebar.selectbox(
    "Streaming TV",
    ["Yes", "No", "No internet service"]
)

streaming_movies = st.sidebar.selectbox(
    "Streaming Movies",
    ["Yes", "No", "No internet service"]
)

contract = st.sidebar.selectbox(
    "Contract",
    [
        "Month-to-month",
        "One year",
        "Two year"
    ]
)

paperless_billing = st.sidebar.selectbox(
    "Paperless Billing",
    ["Yes", "No"]
)

payment_method = st.sidebar.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly_charges = st.sidebar.slider(
    "Monthly Charges",
    min_value=0.0,
    max_value=150.0,
    value=70.0
)

total_charges = st.sidebar.number_input(
    "Total Charges",
    min_value=0.0,
    value=float(monthly_charges * max(tenure, 1))
)

cltv = st.sidebar.number_input(
    "Customer Lifetime Value (CLTV)",
    min_value=0,
    value=3000
)

# =====================================================
# INPUT DATAFRAME
# =====================================================

input_df = pd.DataFrame([{
    "Gender": gender,
    "Senior Citizen": senior,
    "Partner": partner,
    "Dependents": dependents,
    "Tenure Months": tenure,
    "Phone Service": phone_service,
    "Multiple Lines": multiple_lines,
    "Internet Service": internet_service,
    "Online Security": online_security,
    "Online Backup": online_backup,
    "Device Protection": device_protection,
    "Tech Support": tech_support,
    "Streaming TV": streaming_tv,
    "Streaming Movies": streaming_movies,
    "Contract": contract,
    "Paperless Billing": paperless_billing,
    "Payment Method": payment_method,
    "Monthly Charges": monthly_charges,
    "Total Charges": total_charges,
    "CLTV": cltv
}])

# =====================================================
# FEATURE ORDER
# =====================================================

feature_order = [
    "Gender",
    "Senior Citizen",
    "Partner",
    "Dependents",
    "Tenure Months",
    "Phone Service",
    "Multiple Lines",
    "Internet Service",
    "Online Security",
    "Online Backup",
    "Device Protection",
    "Tech Support",
    "Streaming TV",
    "Streaming Movies",
    "Contract",
    "Paperless Billing",
    "Payment Method",
    "Monthly Charges",
    "Total Charges",
    "CLTV"
]

# =====================================================
# ENCODING
# =====================================================

for col, encoder in encoders.items():

    if col in input_df.columns:

        try:
            input_df[col] = encoder.transform(
                input_df[col].astype(str)
            )

        except Exception:
            pass

input_df = input_df[feature_order]

# =====================================================
# PREDICTION
# =====================================================

if st.button("Predict Churn"):

    try:

        prediction = model.predict(input_df)[0]

        probability = model.predict_proba(
            input_df
        )[0][1]

        st.subheader("Prediction Result")

        if prediction == 1:

            st.error(
                f"⚠️ Customer likely to churn ({probability:.2%})"
            )

        else:

            st.success(
                f"✅ Customer likely to stay ({1 - probability:.2%})"
            )

        # ==============================================
        # RISK LEVEL
        # ==============================================

        st.subheader("Risk Level")

        if probability >= 0.75:

            st.error("🔴 High Risk")

        elif probability >= 0.40:

            st.warning("🟠 Medium Risk")

        else:

            st.success("🟢 Low Risk")

        # ==============================================
        # PROBABILITY BAR
        # ==============================================

        st.subheader("Churn Probability")

        st.progress(float(probability))

        st.write(
            f"Predicted churn probability: {probability:.2%}"
        )

        # ==============================================
        # RECOMMENDATIONS
        # ==============================================

        st.subheader("Retention Recommendations")

        if probability >= 0.75:

            st.markdown("""
            - Offer retention discount
            - Assign dedicated support representative
            - Upgrade service plan
            - Launch personalized retention campaign
            """)

        elif probability >= 0.40:

            st.markdown("""
            - Offer loyalty rewards
            - Send engagement campaigns
            - Monitor account activity
            """)

        else:

            st.markdown("""
            - Maintain current customer engagement
            - Continue loyalty programs
            """)

    except Exception as e:

        st.error(f"Prediction Error: {e}")


