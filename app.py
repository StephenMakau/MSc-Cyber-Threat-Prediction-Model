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
# PROFESSIONAL STYLE (TIMES NEW ROMAN / BLUE & WHITE)
# =====================================
st.markdown("""
<style>
    /* Global Settings */
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=fallback');

    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);
        color: #333333;
        font-family: 'Times New Roman', Times, serif;
    }

    /* Typography - Times New Roman */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, a, button {
        font-family: 'Times New Roman', Times, serif !important;
    }

    h1 {
        color: #003366 !important;
        font-size: 2.5rem !important;
        font-weight: bold;
        border-bottom: 2px solid #003366;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    h2, h3, h4 {
        color: #003366 !important;
        font-weight: bold;
    }

    p, li {
        color: #444444 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Navigation Tabs - Clean Professional Look */
    .stTabs [data-testid="stTab"] {
        color: #003366;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: bold;
        background: transparent;
        border: 1px solid transparent;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #0056b3;
        background: rgba(0, 51, 102, 0.05);
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: #ffffff;
        color: #003366 !important;
        border: 1px solid #ddd;
        border-bottom: 1px solid #ffffff;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* Metric Cards - White with Shadow */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
    }

    [data-testid="stMetricValue"] {
        color: #003366 !important;
        font-weight: bold;
        font-size: 2.0rem !important;
        font-family: 'Times New Roman', Times, serif !important;
    }

    [data-testid="stMetricLabel"] {
        color: #555555 !important;
        font-weight: bold;
        font-size: 0.9rem !important;
        font-family: 'Times New Roman', Times, serif !important;
    }

    /* Tables - Clean Academic Style */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid #ddd;
        border-radius: 4px;
        background: #ffffff;
    }

    /* Alert Boxes - Professional Warning Styles */
    .threat-high {
        background: #fff3e0;
        border-left: 5px solid #d35400;
        padding: 25px;
        border-radius: 4px;
        color: #333333 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .threat-high h1, .threat-high h3, .threat-high p {
        color: #333333 !important;
    }

    .threat-critical {
        background: #ffebee;
        border-left: 5px solid #c0392b;
        padding: 25px;
        border-radius: 4px;
        color: #333333 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .threat-critical h1, .threat-critical h3, .threat-critical p {
        color: #333333 !important;
    }

    .threat-moderate {
        background: #e8f5e9;
        border-left: 5px solid #27ae60;
        padding: 25px;
        border-radius: 4px;
        color: #333333 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .threat-moderate h1, .threat-moderate h3, .threat-moderate p {
        color: #333333 !important;
    }

    /* Info Boxes */
    .stAlert {
        background: #ffffff;
        border: 1px solid #ddd;
        color: #333333 !important;
    }
    
    /* Divider */
    hr {
        border-color: #ddd !important;
    }

    /* Custom Glass/White Container for sections */
    .professional-container {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION
# =====================================
home, overview, dataset, models, parameters = st.tabs(
    [
        "HOME",
        "PROJECT OVERVIEW",
        "DATASET",
        "AI MODELS",
        "PARAMETERS"
    ]
)

# =====================================
# HOME / COMMAND CENTER
# =====================================
with home:
    st.title("Cyber Threat Intelligence System")
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

    st.markdown("### Live Threat Assessment")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="professional-container" style="text-align: center;">
            <h4 style="color: #555555; margin:0; font-size: 0.9rem;">Core Algorithm</h4>
            <h2 style="margin: 10px 0; color: #003366;">XGBoost</h2>
            <p style="color: #777777; font-size: 0.8rem;">Advanced Gradient Boosting</p>
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
        <div class="professional-container" style="text-align: center;">
            <h4 style="color: #555555; margin:0; font-size: 0.9rem;">Forecast Horizon</h4>
            <h2 style="margin: 10px 0; color: #003366;">2027</h2>
            <p style="color: #777777; font-size: 0.8rem;">Predictive Analysis</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Threat Display
    st.header("2027 Threat Projection")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1 style="margin:0;">HIGH RISK DETECTED</h1>
            <h3 style="color: #d35400;">Predicted Threat Level: HIGH</h3>
            <p>The predictive model indicates a significant escalation in cyber threats targeting government digital infrastructure. Immediate proactive measures and resource allocation are recommended.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1 style="margin:0;">CRITICAL ALERT</h1>
            <h3 style="color: #c0392b;">Predicted Threat Level: CRITICAL</h3>
            <p>Critical infrastructure vulnerability detected. The model forecasts an unprecedented surge in attack vectors. Emergency protocols should be reviewed immediately.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1 style="margin:0;">STABLE STATUS</h1>
            <h3 style="color: #27ae60;">Predicted Threat Level: MODERATE</h3>
            <p>Threat levels are within manageable parameters. Continue standard monitoring and maintenance protocols.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# PROJECT OVERVIEW
# =====================================
with overview:
    st.title("Project Overview & Research Context")
    
    st.markdown("""
    <div class="professional-container">
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Research Objective")
    st.write("""
    This system represents the core analytical engine of an MSc Cybersecurity thesis at Mount Kenya University. 
    The project addresses the critical need for proactive cyber defense mechanisms within Kenyan Government Digital Services.
    """)

    st.subheader("The Challenge")
    st.write("""
    As digital transformation accelerates across public sectors, the threat landscape evolves exponentially. 
    Traditional reactive security measures are insufficient against modern, automated cyber attacks. 
    There is a critical gap in predictive capabilities for national-level digital infrastructure.
    """)

    st.subheader("Methodology")
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

    st.subheader("Strategic Importance")
    st.write("""
    This predictive capability is vital for:
    """)
    st.markdown("""
    - **National Security Infrastructure Protection**
    - **Pre-emptive Resource Allocation**
    - **Policy Formulation for Digital Governance**
    - **Enhancing Public Trust in E-Government Services**
    """)

    st.info("Data Privacy Note: All data displayed in this system is synthetic or anonymized for research purposes. No real-time government data is exposed.")

# =====================================
# DATASET
# =====================================
with dataset:
    st.title("Data Matrix")
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
    st.title("AI Model Performance")
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
    
    st.warning("Note: XGBoost was selected as the primary model due to superior performance in handling imbalanced cybersecurity datasets and complex non-linear relationships.")

# =====================================
# PARAMETERS
# =====================================
with parameters:
    st.title("Prediction Parameters")
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
    <div class="professional-container">
    </div>
    """, unsafe_allow_html=True)
    st.warning("Parameter Significance: Each parameter is weighted by the model based on its historical correlation with threat escalation. Economic instability and patch delays often show high correlation with increased attack surfaces.")
