import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from cyber_threat_model import (
    predict_2027,
    get_model_accuracy,
    get_results,
    get_dataset,
    get_parameters
)

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="MKU Cyber Threat Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# =====================================
# GOOGLE COLORS FUTURISTIC THEME
# =====================================
st.markdown("""
<style>
    /* 
       GOOGLE COLOR PALETTE:
       - Blue: #4285F4 (Primary)
       - Red: #EA4335 (Critical/Danger)
       - Yellow: #FBBC04 (Warnings/High)
       - Green: #34A853 (Success/Stable)
       - Background: Material Design Light
    */

    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* Global Background - Material Design Light with Google Blue tint */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e8f0fe 100%);
        color: #202124;
    }

    /* Typography: Roboto (Google's font) for headers, Calibri for body */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #4285F4 !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h1 {
        background: linear-gradient(90deg, #4285F4, #34A853);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-bottom: 3px solid #4285F4;
        padding-bottom: 15px;
        margin-bottom: 25px;
        font-size: 2.8rem !important;
    }

    h2 {
        color: #1a73e8 !important;
        margin-top: 30px;
        font-size: 2rem !important;
        border-left: 4px solid #FBBC04;
        padding-left: 15px;
    }
    
    h3 {
        color: #188038 !important;
        margin-top: 25px;
        font-size: 1.5rem !important;
    }

    /* Body Text: Calibri as requested */
    p, li, div, span, label, .stMarkdown, .stAlert {
        font-family: Calibri, 'Segoe UI', Candara, sans-serif !important;
        color: #3c4043 !important;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    p {
        margin-bottom: 1rem !important;
    }
    
    li {
        margin-bottom: 0.5rem !important;
        font-family: Calibri, sans-serif !important;
    }

    /* Navigation Tabs - Google Style */
    .stTabs [data-testid="stTab"] {
        color: #5f6368;
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500;
        font-size: 1rem;
        background: #ffffff;
        border: 2px solid #dadce0;
        border-radius: 24px;
        padding: 12px 28px;
        margin: 0 8px 15px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #4285F4;
        background: #e8f0fe;
        border-color: #4285F4;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.2);
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: #4285F4;
        color: #ffffff !important;
        border: 2px solid #4285F4;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
    }

    /* Metric Cards - Google Material Cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: none;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 20px rgba(66, 133, 244, 0.25);
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4285F4, #34A853);
    }

    [data-testid="stMetricValue"] {
        color: #4285F4 !important;
        font-family: 'Roboto', sans-serif !important;
        font-weight: 700;
        font-size: 3rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #5f6368 !important;
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 8px;
    }

    /* Tables - Google Style */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid #dadce0;
        border-radius: 12px;
        background: #ffffff;
        color: #202124;
        box-shadow: 0 1px 2px rgba(60,64,67,0.3);
    }

    /* Alert Boxes - Google Colors */
    .threat-high {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        border-left: 6px solid #FBBC04;
        border-radius: 12px;
        padding: 30px;
        color: #b06000 !important;
        box-shadow: 0 4px 12px rgba(251, 188, 4, 0.2);
    }

    .threat-high h1 {
        color: #e65100 !important;
        border-bottom: none;
        font-size: 2.2rem !important;
        margin-bottom: 10px !important;
        background: none;
        -webkit-text-fill-color: #e65100;
    }
    
    .threat-high h3 {
        color: #f57c00 !important;
        margin-top: 0 !important;
        border-left: none;
        padding-left: 0;
    }
    
    .threat-high p {
        color: #6c4f00 !important;
        font-family: Calibri, sans-serif !important;
    }

    .threat-critical {
        background: linear-gradient(135deg, #fce8e6 0%, #ffcfc9 100%);
        border-left: 6px solid #EA4335;
        border-radius: 12px;
        padding: 30px;
        color: #c5221f !important;
        box-shadow: 0 4px 12px rgba(234, 67, 53, 0.2);
    }

    .threat-critical h1 {
        color: #c5221f !important;
        border-bottom: none;
        font-size: 2.2rem !important;
        margin-bottom: 10px !important;
        background: none;
        -webkit-text-fill-color: #c5221f;
    }
    
    .threat-critical h3 {
        color: #d93025 !important;
        margin-top: 0 !important;
        border-left: none;
        padding-left: 0;
    }
    
    .threat-critical p {
        color: #5c0c0c !important;
        font-family: Calibri, sans-serif !important;
    }

    .threat-moderate {
        background: linear-gradient(135deg, #e6f4ea 0%, #c8e6c9 100%);
        border-left: 6px solid #34A853;
        border-radius: 12px;
        padding: 30px;
        color: #137333 !important;
        box-shadow: 0 4px 12px rgba(52, 168, 83, 0.2);
    }

    .threat-moderate h1 {
        color: #137333 !important;
        border-bottom: none;
        font-size: 2.2rem !important;
        margin-bottom: 10px !important;
        background: none;
        -webkit-text-fill-color: #137333;
    }
    
    .threat-moderate h3 {
        color: #188038 !important;
        margin-top: 0 !important;
        border-left: none;
        padding-left: 0;
    }
    
    .threat-moderate p {
        color: #0d5c1e !important;
        font-family: Calibri, sans-serif !important;
    }

    /* Info/Warning Boxes */
    .stAlert {
        background: #e8f0fe;
        border: 1px solid #4285F4;
        color: #1967d2 !important;
        border-radius: 12px;
        font-family: Calibri, sans-serif !important;
        border-left: 4px solid #4285F4;
    }
    
    .stAlert p {
        color: #1967d2 !important;
        font-family: Calibri, sans-serif !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: #5f6368 !important;
        font-family: Calibri, sans-serif !important;
        font-size: 0.95rem;
    }
    
    /* Divider */
    hr {
        border-color: #dadce0 !important;
        margin: 30px 0 !important;
    }

    /* Professional Container - Google Card Style */
    .professional-container {
        background: #ffffff;
        border: none;
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .professional-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4285F4, #EA4335, #FBBC04, #34A853);
    }
    
    /* Strong text */
    strong, b {
        color: #4285F4 !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION WITH ICONS
# =====================================
home, overview, dataset, models, parameters = st.tabs(
    [
        "🏠 HOME",
        "📄 PROJECT OVERVIEW", 
        "📊 DATASET",
        "🤖 AI MODELS",
        "⚙️ PARAMETERS"
    ]
)

# =====================================
# HOME / COMMAND CENTER
# =====================================
with home:
    st.title("🛡️ Cyber Threat Intelligence System")
    st.subheader("🏫 Mount Kenya University | MSc Cybersecurity")
    st.markdown("**👤 Author:** Stephen Musau Makau")
    st.caption(f"⏱️ System Active: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d %B %Y | %H:%M:%S EAT')}")
    
    st.divider()

    # Prediction Engine
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    st.markdown("### 📡 Live Threat Assessment")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="professional-container" style="text-align: center;">
            <h4 style="color: #5f6368; margin:15px 0 0 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1.5px; font-family: Roboto, sans-serif;">Core Algorithm</h4>
            <h2 style="margin: 15px 0; color: #4285F4; font-family: Roboto, sans-serif !important; font-size: 2.4rem; font-weight: 700;">XGBoost</h2>
            <p style="color: #80868b; font-size: 0.95rem; font-family: Calibri, sans-serif; margin-bottom: 15px;">Advanced Gradient Boosting</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.metric(
            "🎯 Model Accuracy",
            f"{accuracy:.2f}%",
            help="Based on historical training data validation"
        )

    with c3:
        st.markdown("""
        <div class="professional-container" style="text-align: center;">
            <h4 style="color: #5f6368; margin:15px 0 0 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1.5px; font-family: Roboto, sans-serif;">Forecast Horizon</h4>
            <h2 style="margin: 15px 0; color: #34A853; font-family: Roboto, sans-serif !important; font-size: 2.4rem; font-weight: 700;">2027</h2>
            <p style="color: #80868b; font-size: 0.95rem; font-family: Calibri, sans-serif; margin-bottom: 15px;">Predictive Analysis</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Threat Display
    st.header("🚨 2027 Threat Projection")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1>⚠️ HIGH RISK DETECTED</h1>
            <h3>Predicted Threat Level: HIGH</h3>
            <p>The predictive model indicates a significant escalation in cyber threats targeting government digital infrastructure. Immediate proactive measures and resource allocation are recommended.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1>🛑 CRITICAL ALERT</h1>
            <h3>Predicted Threat Level: CRITICAL</h3>
            <p>Critical infrastructure vulnerability detected. The model forecasts an unprecedented surge in attack vectors. Emergency protocols should be reviewed immediately.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1>✅ STABLE STATUS</h1>
            <h3>Predicted Threat Level: MODERATE</h3>
            <p>Threat levels are within manageable parameters. Continue standard monitoring and maintenance protocols.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# PROJECT OVERVIEW
# =====================================
with overview:
    st.title("📄 Project Overview & Research Context")
    
    st.subheader("🎯 Research Objective")
    st.write("""
    This system represents the core analytical engine of an MSc Cybersecurity thesis at Mount Kenya University. 
    The project addresses the critical need for proactive cyber defense mechanisms within Kenyan Government Digital Services.
    """)

    st.subheader("⚠️ The Challenge")
    st.write("""
    As digital transformation accelerates across public sectors, the threat landscape evolves exponentially. 
    Traditional reactive security measures are insufficient against modern, automated cyber attacks. 
    There is a critical gap in predictive capabilities for national-level digital infrastructure.
    """)

    st.subheader("🔬 Methodology")
    st.write("""
    This system utilizes **Machine Learning (XGBoost)** to analyze complex correlations between:
    """)
    st.markdown("""
    - **🎯 Historical cyber attack vectors:** DDoS, Malware, Phishing, Web Attacks
    - **🔒 System vulnerability metrics:** Critical CVEs, Patch Delays
    - **📡 Network traffic anomalies:** Unusual data flow patterns
    - **📈 Socio-economic factors:** Inflation and GDP Growth rates (which often correlate with cybercrime rates)
    
    By synthesizing these diverse data streams, the model forecasts future threat levels, enabling government agencies to 
    allocate resources and strengthen defenses **before** attacks occur.
    """)

    st.subheader("🌍 Strategic Importance")
    st.write("""
    This predictive capability is vital for:
    """)
    st.markdown("""
    - **🏛️ National Security Infrastructure Protection**
    - **💰 Pre-emptive Resource Allocation**
    - **📋 Policy Formulation for Digital Governance**
    - **🤝 Enhancing Public Trust in E-Government Services**
    """)

    st.info("🔒 **Data Privacy Note:** All data displayed in this system is synthetic or anonymized for research purposes. No real-time government data is exposed.")

# =====================================
# DATASET
# =====================================
with dataset:
    st.title("📊 Data Matrix")
    st.markdown("Accessing raw training data and feature set...")
    st.dataframe(
        get_dataset(),
        use_container_width=True,
        height=600
    )

# =====================================
# MODELS
# =====================================
with models:
    st.title("🤖 AI Model Performance")
    st.markdown("Comparative analysis of machine learning algorithms evaluated during research.")
    
    results = get_results()
    table_data = []
    for name, value in results.items():
        table_data.append({
            "Algorithm": name,
            "Accuracy": f"{value*100:.2f}%",
            "Status": "Active" if name == "XGBoost" else "Evaluated"
        })
    
    st.table(table_data)
    
    st.warning("⚠️ **Note:** XGBoost was selected as the primary model due to superior performance in handling imbalanced cybersecurity datasets and complex non-linear relationships.")

# =====================================
# PARAMETERS
# =====================================
with parameters:
    st.title("⚙️ Prediction Parameters")
    st.markdown("""
    The following variables constitute the feature set for the 2027 threat projection. 
    These parameters are derived from historical trends, economic forecasts, and technological growth projections.
    """)
    
    st.dataframe(
        get_parameters(),
        use_container_width=True,
        height=400
    )
    
    st.warning("⚠️ **Parameter Significance:** Each parameter is weighted by the model based on its historical correlation with threat escalation. Economic instability and patch delays often show high correlation with increased attack surfaces.")
