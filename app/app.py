import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

.hero {
    background: linear-gradient(135deg,#1e293b,#334155);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    color: white;
}

.metric-card {
    background-color: #1e293b;
    padding: 2rem;
    border-radius: 18px;
    text-align: center;
    color: white;
    border: 1px solid #334155;
    min-height: 150px;
}
}

.metric-value {
    font-size: 2.8rem;
    font-weight: 700;
    color: #38bdf8;
}
}

.metric-label {
    font-size: 1rem;
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="hero">

<h1>📊 Customer Churn Prediction System</h1>

<p>
Predict customer attrition using Machine Learning.
</p>

<p>
Model: XGBoost | Industry: Telecom, Banking, SaaS
</p>

</div>
""", unsafe_allow_html=True)

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

predict = st.sidebar.button(
    "🚀 Predict Churn",
    use_container_width=True
)

if predict:

    try:

        prediction = model.predict(input_df)[0]

        probability = model.predict_proba(
            input_df
        )[0][1]
        risk = (
            "High"
            if probability >= 0.75
            else "Medium"
            if probability >= 0.40
            else "Low"
)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">
                    Churn Probability
                </div>
                <div class="metric-value">
                    {probability:.2%}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">
                    Prediction
                </div>
                <div class="metric-value">
                    {"Churn" if prediction == 1 else "Stay"}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">
                    Risk Level
                </div>
                <div class="metric-value">
                    {risk}
                </div>
            </div>
            """, unsafe_allow_html=True)
                
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">
                    ROC-AUC
                </div>
                <div class="metric-value">
                    0.85
                </div>
            </div>
            """, unsafe_allow_html=True)


        

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

        fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            title={
                "text": "Churn Probability (%)"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            }
        )
    )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

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

st.markdown("---")

st.markdown(
"""
Developed using:

- Python
- XGBoost
- Scikit-Learn
- Streamlit

End-to-End Customer Churn Prediction Project
"""
)
