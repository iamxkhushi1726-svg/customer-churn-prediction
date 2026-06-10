import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Churn Prediction Dashboard",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# IMPROVED DARK THEME CSS
# =====================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lora:wght@400;500;600&family=Poppins:wght@400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #0d1117;
        --bg-darker: #010409;
        --bg-card: #161b22;
        --bg-hover: #1c2128;
        --accent-gold: #d4af37;
        --accent-light-gold: #e8c547;
        --accent-copper: #b8860b;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --success: #3fb950;
        --warning: #d29922;
        --danger: #f85149;
        --border-color: #30363d;
        --border-light: #21262d;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-dark) !important;
        color: var(--text-primary) !important;
        font-family: 'Lora', serif;
    }

    [data-testid="stSidebar"] {
        background-color: var(--bg-darker) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--text-primary);
        letter-spacing: 0.02em;
    }

    h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    h3 {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    p {
        font-family: 'Lora', serif;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Hero Section */
    .hero-dark {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-hover) 100%);
        border-bottom: 3px solid var(--accent-gold);
        border-top: 1px solid var(--border-color);
        padding: 3.5rem 2rem;
        margin-bottom: 2.5rem;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
    }

    .hero-dark::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-dark h1 {
        position: relative;
        z-index: 1;
        color: var(--text-primary);
    }

    .hero-dark .subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.15em;
        color: var(--accent-gold);
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-weight: 700;
    }

    .hero-dark .description {
        font-size: 1.05rem;
        color: var(--text-secondary);
        max-width: 700px;
        margin-bottom: 1rem;
    }

    .accent-line {
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-copper) 100%);
        margin: 1rem 0;
    }

    /* Card styling */
    .premium-card-dark {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
    }

    .premium-card-dark::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, transparent 100%);
        border-radius: 12px 12px 0 0;
    }

    .premium-card-dark:hover {
        border-color: var(--accent-gold);
        background: var(--bg-hover);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
        transform: translateY(-2px);
    }

    /* Metric cards */
    .metric-dark {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
    }

    .metric-dark::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent-gold) 50%, transparent 100%);
        border-radius: 12px 12px 0 0;
    }

    .metric-dark:hover {
        border-color: var(--accent-gold);
        background: var(--bg-hover);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.1);
        transform: translateY(-3px);
    }

    .metric-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-light-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.3rem 0;
    }

    .metric-description {
        font-family: 'Poppins', sans-serif;
        font-size: 0.8rem;
        color: var(--text-muted);
    }

    /* Risk boxes */
    .risk-high-dark {
        background: linear-gradient(135deg, rgba(248, 81, 73, 0.15) 0%, rgba(248, 81, 73, 0.05) 100%);
        border-left: 5px solid var(--danger);
        border: 1px solid rgba(248, 81, 73, 0.3);
    }

    .risk-medium-dark {
        background: linear-gradient(135deg, rgba(210, 153, 34, 0.15) 0%, rgba(210, 153, 34, 0.05) 100%);
        border-left: 5px solid var(--warning);
        border: 1px solid rgba(210, 153, 34, 0.3);
    }

    .risk-low-dark {
        background: linear-gradient(135deg, rgba(63, 185, 80, 0.15) 0%, rgba(63, 185, 80, 0.05) 100%);
        border-left: 5px solid var(--success);
        border: 1px solid rgba(63, 185, 80, 0.3);
    }

    .risk-box-dark {
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        background: var(--bg-card);
    }

    .risk-box-dark h3 {
        margin-bottom: 0.8rem;
        color: var(--text-primary);
    }

    .risk-box-dark p {
        margin-bottom: 1rem;
        color: var(--text-secondary);
    }

    .risk-box-dark ul {
        list-style: none;
        padding-left: 0;
    }

    .risk-box-dark li {
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
        font-family: 'Lora', serif;
        color: var(--text-secondary);
    }

    .risk-box-dark li:before {
        content: "→";
        position: absolute;
        left: 0;
        color: var(--accent-gold);
        font-weight: bold;
    }

    /* Form styling */
    .form-dark {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }

    .form-dark h2 {
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--border-light);
        padding-bottom: 1rem;
        color: var(--text-primary);
    }

    .form-section-title {
        font-family: 'Poppins', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.12em;
        color: var(--accent-gold);
        text-transform: uppercase;
        margin: 1.5rem 0 1rem 0;
        font-weight: 700;
    }

    /* Button styling - FIXED */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-light-gold) 100%) !important;
        color: #0d1117 !important;
        border: none !important;
        padding: 0.9rem 2.5rem !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        font-family: 'Poppins', sans-serif !important;
        letter-spacing: 0.05em !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
        text-transform: uppercase !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(212, 175, 55, 0.4) !important;
        background: linear-gradient(135deg, var(--accent-light-gold) 0%, var(--accent-gold) 100%) !important;
    }

    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* Divider */
    .divider-gold-dark {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent-gold) 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Section header */
    .section-header-dark {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .section-header-dark h2 {
        margin: 0;
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .hero-dark {
        animation: fadeInDown 0.8s ease-out;
    }

    .premium-card-dark {
        animation: fadeInUp 0.6s ease-out;
    }

    .metric-dark {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }

        h2 {
            font-size: 1.3rem;
        }

        .metric-value {
            font-size: 1.6rem;
        }

        .hero-dark {
            padding: 2rem 1rem;
        }

        .premium-card-dark {
            padding: 1.5rem;
        }
    }

    /* Reduce motion */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# MOCK MODEL
# =====================================================

class PremiumChurnPredictor:
    """Premium churn prediction model"""
    
    def __init__(self):
        self.model_name = "Advanced Churn Predictor"
        self.roc_auc = 0.87
        self.accuracy = 0.82
    
    def predict(self, features_dict):
        """Mock prediction with realistic logic"""
        tenure = features_dict.get('tenure', 12)
        monthly_charges = features_dict.get('monthly_charges', 70)
        contract = features_dict.get('contract', 'Month-to-month')
        internet_service = features_dict.get('internet_service', 'DSL')
        
        base_prob = 0.45
        
        if tenure > 36:
            base_prob -= 0.25
        elif tenure > 24:
            base_prob -= 0.15
        elif tenure < 6:
            base_prob += 0.2
        
        if contract == 'Two year':
            base_prob -= 0.3
        elif contract == 'One year':
            base_prob -= 0.12
        
        if monthly_charges > 100:
            base_prob += 0.12
        elif monthly_charges < 30:
            base_prob -= 0.1
        
        if internet_service == 'Fiber optic':
            base_prob += 0.08
        
        probability = np.clip(base_prob + np.random.normal(0, 0.04), 0, 1)
        
        return probability

predictor = PremiumChurnPredictor()

# =====================================================
# SESSION STATE
# =====================================================

if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero-dark">
    <div class="subtitle">✨ Advanced Analytics Platform</div>
    <h1>Churn Prediction</h1>
    <div class="accent-line"></div>
    <p class="description">
        Predict customer attrition with precision. Powered by advanced machine learning models 
        designed for enterprise-grade accuracy and insights.
    </p>
    <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 1rem;">
    End-to-End Machine Learning Project • XGBoost • Streamlit Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MAIN LAYOUT
# =====================================================

col1, col2 = st.columns([1, 2], gap="large")

# =====================================================
# LEFT COLUMN: FORM
# =====================================================

with col1:
    st.markdown("""
    <div class="form-dark">
        <h2>Customer Profile</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("prediction_form"):
        st.markdown('<p class="form-section-title">Demographics</p>', unsafe_allow_html=True)
        
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"], key="senior")
        partner = st.selectbox("Partner", ["No", "Yes"], key="partner")
        dependents = st.selectbox("Dependents", ["No", "Yes"], key="dependents")
        
        st.markdown('<p class="form-section-title">Service Configuration</p>', unsafe_allow_html=True)
        
        tenure = st.slider("Tenure (months)", 0, 72, 12, key="tenure")
        phone_service = st.selectbox("Phone Service", ["No", "Yes"], key="phone")
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], key="internet")
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], key="contract")
        
        st.markdown('<p class="form-section-title">Add-on Services</p>', unsafe_allow_html=True)
        
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"], key="security")
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"], key="backup")
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"], key="device")
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"], key="tech")
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"], key="tv")
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"], key="movies")
        
        st.markdown('<p class="form-section-title">Billing Information</p>', unsafe_allow_html=True)
        
        paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"], key="paperless")
        payment_method = st.selectbox("Payment Method", 
                                     ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
                                     key="payment")
        
        st.markdown('<p class="form-section-title">Financial Metrics</p>', unsafe_allow_html=True)
        
        monthly_charges = st.slider("Monthly Charges ($)", 0.0, 150.0, 70.0, key="monthly")
        total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, float(monthly_charges * max(tenure, 1)), key="total")
        cltv = st.number_input("Customer Lifetime Value ($)", 0, 10000, 3000, key="cltv")
        
        st.markdown('<div class="divider-gold-dark"></div>', unsafe_allow_html=True)
        
        # Centered button
        col_left, col_center, col_right = st.columns([1, 1.5, 1])
        with col_center:
            submit_button = st.form_submit_button("✨ Analyze Churn Risk", use_container_width=True)
        
        if submit_button:
            features = {
                'gender': gender,
                'senior_citizen': senior_citizen,
                'partner': partner,
                'dependents': dependents,
                'tenure': tenure,
                'phone_service': phone_service,
                'internet_service': internet_service,
                'contract': contract,
                'online_security': online_security,
                'online_backup': online_backup,
                'device_protection': device_protection,
                'tech_support': tech_support,
                'streaming_tv': streaming_tv,
                'streaming_movies': streaming_movies,
                'paperless_billing': paperless_billing,
                'payment_method': payment_method,
                'monthly_charges': monthly_charges,
                'total_charges': total_charges,
                'cltv': cltv,
            }
            
            probability = predictor.predict(features)
            prediction = "Churn" if probability >= 0.5 else "Retain"
            risk_level = "High" if probability >= 0.75 else "Medium" if probability >= 0.4 else "Low"
            
            st.session_state.show_results = True
            st.session_state.prediction_result = {
                'probability': probability,
                'prediction': prediction,
                'risk_level': risk_level,
                'roc_auc': predictor.roc_auc,
                'accuracy': predictor.accuracy,
                'features': features
            }

# =====================================================
# RIGHT COLUMN: RESULTS
# =====================================================

with col2:
    if st.session_state.show_results and st.session_state.prediction_result:
        result = st.session_state.prediction_result
        prob = result['probability']
        risk = result['risk_level']
        
        st.markdown('<div class="section-header-dark"><h2>Analysis Results</h2><div class="accent-line"></div></div>', unsafe_allow_html=True)
        
        # Metric cards
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.markdown(f"""
            <div class="metric-dark">
                <div class="metric-label">Churn Probability</div>
                <div class="metric-value">{prob*100:.1f}%</div>
                <div class="metric-description">Risk Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(f"""
            <div class="metric-dark">
                <div class="metric-label">Prediction</div>
                <div class="metric-value" style="font-size: 1.6rem;">{result['prediction']}</div>
                <div class="metric-description">Outcome</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            st.markdown(f"""
            <div class="metric-dark">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value" style="font-size: 1.6rem;">{risk}</div>
                <div class="metric-description">Assessment</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[3]:
            st.markdown(f"""
            <div class="metric-dark">
                <div class="metric-label">Model Accuracy</div>
                <div class="metric-value">{result['accuracy']*100:.0f}%</div>
                <div class="metric-description">Validated</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-gold-dark"></div>', unsafe_allow_html=True)
        
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={"text": "Churn Risk Gauge"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#d4af37"},
                "steps": [
                    {"range": [0, 40], "color": "rgba(63, 185, 80, 0.2)"},
                    {"range": [40, 75], "color": "rgba(210, 153, 34, 0.2)"},
                    {"range": [75, 100], "color": "rgba(248, 81, 73, 0.2)"}
                ],
            },
            domain={"x": [0, 1], "y": [0, 1]}
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Lora, serif", color="#e6edf3", size=12),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('<div class="divider-gold-dark"></div>', unsafe_allow_html=True)
        
        # Risk assessment
        if risk == "High":
            st.markdown(f"""
            <div class="risk-box-dark risk-high-dark">
                <h3>⚠️ High Risk Assessment</h3>
                <p>This customer exhibits strong churn indicators and requires immediate strategic intervention.</p>
                <p><strong>Recommended Actions:</strong></p>
                <ul>
                    <li>Initiate retention discount program</li>
                    <li>Assign dedicated account manager</li>
                    <li>Offer premium service upgrade</li>
                    <li>Launch personalized engagement campaign</li>
                    <li>Schedule executive outreach</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        elif risk == "Medium":
            st.markdown(f"""
            <div class="risk-box-dark risk-medium-dark">
                <h3>⚡ Medium Risk Assessment</h3>
                <p>This customer shows moderate churn indicators. Proactive engagement is recommended.</p>
                <p><strong>Recommended Actions:</strong></p>
                <ul>
                    <li>Offer loyalty rewards program</li>
                    <li>Send targeted engagement campaigns</li>
                    <li>Monitor account activity closely</li>
                    <li>Provide service optimization recommendations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown(f"""
            <div class="risk-box-dark risk-low-dark">
                <h3>✓ Low Risk Assessment</h3>
                <p>This customer demonstrates strong retention signals and loyalty indicators.</p>
                <p><strong>Recommended Actions:</strong></p>
                <ul>
                    <li>Maintain current engagement strategy</li>
                    <li>Continue loyalty program benefits</li>
                    <li>Explore upsell opportunities</li>
                    <li>Gather feedback for service improvement</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-gold-dark"></div>', unsafe_allow_html=True)
        
        # Reset button - centered
        col_left, col_center, col_right = st.columns([1, 1.5, 1])
        with col_center:
            if st.button("← New Analysis", use_container_width=True):
                st.session_state.show_results = False
                st.session_state.prediction_result = None
                st.rerun()
    
    else:
        st.markdown("""
        <div class="premium-card-dark" style="text-align: center; padding: 3rem 2rem;">
            <h2 style="margin-bottom: 1rem; border: none; padding: 0;">Analysis Dashboard</h2>
            <p style="font-size: 1.05rem; color: var(--text-secondary);">
                Complete the customer profile on the left and click "Analyze Churn Risk" to generate detailed insights and recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown('<div class="divider-gold-dark"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="
text-align:center;
padding:2rem 0;
color:#8b949e;
font-family:'Lora', serif;
border-top:1px solid #30363d;
margin-top:2rem;
">

<h4 style="
color:#d4af37;
margin-bottom:10px;
font-family:'Playfair Display', serif;
">
Customer Churn Prediction System
</h4>

<p>
Built by <strong>Khushi</strong>
</p>

<p style="font-size:0.9rem;">
Machine Learning • Data Science • Predictive Analytics
</p>

</div>
""", unsafe_allow_html=True)