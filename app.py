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
    page_title="MKU Cyber Threat Intelligence | MSc Project",
    page_icon="🛡️",
    layout="wide"
)

# =====================================
# FUTURISTIC STYLE (ROYAL PURPLE THEME)
# =====================================
st.markdown("""
<style>
    /* Global Background - Deep Royal Purple Space */
    .stApp {
        background: linear-gradient(135deg, #0f0518 0%, #1a0b2e 100%);
        color: #e0e0e0;
    }

    /* Typography Overrides for Safety and Visibility */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        text-shadow: 0 0 10px rgba(188, 19, 254, 0.5);
    }

    p, div, span, label, li {
        color: #c5c5c5 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Glassmorphism Containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(188, 19, 254, 0.2);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    /* Metric Cards - Futuristic Style */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(30, 10, 50, 0.8), rgba(10, 5, 20, 0.9));
        border: 1px solid #bc13fe;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(188, 19, 254, 0.3);
        text-align: center;
    }

    [data-testid="stMetricValue"] {
        color: #00f3ff !important;
        font-weight: 900;
        font-size: 2.5rem !important;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
    }

    [data-testid="stMetricLabel"] {
        color: #bc13fe !important;
        font-weight: 600;
        font-size: 1.1rem !important;
    }

    /* Tables - Cyber Grid Style */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 10px;
        overflow: hidden;
    }

    /* Custom Alert Boxes */
    .threat-high {
        background: linear-gradient(90deg, rgba(245, 124, 0, 0.2), rgba(255, 87, 34, 0.1));
        border-left: 5px solid #ff5722;
        padding: 25px;
        border-radius: 8px;
        color: #ffccbc !important;
        box-shadow: 0 0 20px rgba(255, 87, 34, 0.2);
    }

    .threat-critical {
        background: linear-gradient(90deg, rgba(211, 47, 47, 0.2), rgba(255, 0, 0, 0.1));
        border-left: 5px solid #d32f2f;
        padding: 25px;
        border-radius: 8px;
        color: #ffcdd2 !important;
        box-shadow: 0 0 20px rgba(211, 47, 47, 0.2);
    }

    .threat-moderate {
        background: linear-gradient(90deg, rgba(0, 150, 136, 0.2), rgba(0, 200, 83, 0.1));
        border-left: 5px solid #00c853;
        padding: 25px;
        border-radius: 8px;
        color: #b2dfdb !important;
        box-shadow: 0 0 20px rgba(0, 200, 83, 0.2);
    }

    /* Navigation Tabs */
    .stTabs [data-testid="stTab"] {
        color: #bc13fe;
        border: 1px solid rgba(188, 19, 254, 0.3);
        background: rgba(255, 255, 255, 0.05);
        margin-right: 5px;
    }

    .stTabs [data-testid="stTab"]:hover {
        border: 1px solid #00f3ff;
        color: #00f3ff;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: linear-gradient(90deg, #bc13fe, #7b1fa2);
        color: white !important;
        border: none;
        box-shadow: 0 0 15px rgba(188, 19, 254, 0.5);
    }

    /* Divider */
    hr {
        border-color: rgba(188, 19, 254, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION
# =====================================
home, overview, dataset, models, parameters = st.tabs(
    [
        "🏠 COMMAND CENTER",
        "📜 PROJECT OVERVIEW",
        "📊 DATA MATRIX",
        "🤖 AI MODELS",
        "⚙ PARAMETERS"
    ]
)

# =====================================
# HOME / COMMAND CENTER
# =====================================
with home:
    col_header, col_logo = st.columns([4, 1])
    with col_header:
        st.title("CYBER THREAT INTELLIGENCE SYSTEM")
        st.subheader("Mount Kenya University | MSc Cybersecurity")
        st.markdown("**Author:** Stephen Musau Makau")
        st.caption(f"System Active: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d %B %Y | %H:%M:%S EAT')}")
    
    st.divider()

    # Prediction Engine
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    st.markdown("### 🛡️ Live Threat Assessment")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-container">
            <h4 style="color:#00f3ff; margin:0;">Core Algorithm</h4>
            <h2 style="margin:0;">XGBoost</h2>
            <p style="color:#888; font-size:0.8rem;">Advanced Gradient Boosting</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.metric(
            "Model Accuracy",
            f"{accuracy:.2f}%",
            help="Based on historical training data validation"
        )

    with c3:
        st.markdown("""
        <div class="glass-container">
            <h4 style="color:#bc13fe; margin:0;">Forecast Horizon</h4>
            <h2 style="margin:0;">2027</h2>
            <p style="color:#888; font-size:0.8rem;">Predictive Analysis</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Threat Display
    st.header("🚨 2027 Threat Projection")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1 style="color:#ff5722; margin:0;">⚠️ HIGH RISK DETECTED</h1>
            <h3 style="color:#ffccbc;">Predicted Threat Level: HIGH</h3>
            <p>The predictive model indicates a significant escalation in cyber threats targeting government digital infrastructure. Immediate proactive measures and resource allocation are recommended.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1 style="color:#d32f2f; margin:0;">🛑 CRITICAL ALERT</h1>
            <h3 style="color:#ffcdd2;">Predicted Threat Level: CRITICAL</h3>
            <p>Critical infrastructure vulnerability detected. The model forecasts an unprecedented surge in attack vectors. Emergency protocols should be reviewed immediately.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1 style="color:#00c853; margin:0;">✅ STABLE STATUS</h1>
            <h3 style="color:#b2dfdb;">Predicted Threat Level: MODERATE</h3>
            <p>Threat levels are within manageable parameters. Continue standard monitoring and maintenance protocols.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# PROJECT OVERVIEW (FIXED SECTION)
# =====================================
with overview:
    st.title("📜 Project Overview & Research Context")
    
    # Using native Streamlit components for reliability and safety
    st.markdown("""
    <div class="glass-container">
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎯 Research Objective", divider=False)
    st.write("""
    This system represents the core analytical engine of an MSc Cybersecurity thesis at Mount Kenya University. 
    The project addresses the critical need for proactive cyber defense mechanisms within Kenyan Government Digital Services.
    """)

    st.subheader("⚠️ The Challenge", divider=False)
    st.write("""
    As digital transformation accelerates across public sectors, the threat landscape evolves exponentially. 
    Traditional reactive security measures are insufficient against modern, automated cyber attacks. 
    There is a critical gap in predictive capabilities for national-level digital infrastructure.
    """)

    st.subheader("🔬 Methodology", divider=False)
    st.write("""
    This system utilizes **Machine Learning (XGBoost)** to analyze complex correlations between:
    """)
    st.markdown("""
    - **Historical cyber attack vectors:** DDoS, Malware, Phishing, Web Attacks
    - **System vulnerability metrics:** Critical CVEs, Patch Delays
    - **Network traffic anomalies:** Unusual data flow patterns
    - **Socio-economic factors:** Inflation and GDP Growth rates (which often correlate with cybercrime rates)
    
    By synthesizing these diverse data streams, the model forecasts future threat levels, enabling government agencies to 
    allocate resources and strengthen defenses **before** attacks occur.
    """)

    st.subheader("🌍 Strategic Importance", divider=False)
    st.write("""
    This predictive capability is vital for:
    """)
    st.markdown("""
    - **National Security Infrastructure Protection**
    - **Pre-emptive Resource Allocation**
    - **Policy Formulation for Digital Governance**
    - **Enhancing Public Trust in E-Government Services**
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
    st.title("⚙ Prediction Parameters")
    st.markdown("""
    The following variables constitute the feature set for the 2027 threat projection. 
    These parameters are derived from historical trends, economic forecasts, and technological growth projections.
    """)
    
    st.dataframe(
        get_parameters(),
        use_container_width=True,
        height=400
    )
    
    st.markdown("""
    <div class="glass-container">
    </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ **Parameter Significance:** Each parameter is weighted by the model based on its historical correlation with threat escalation. Economic instability and patch delays often show high correlation with increased attack surfaces.")
