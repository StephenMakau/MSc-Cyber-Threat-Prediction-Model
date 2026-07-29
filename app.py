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
# PROFESSIONAL CYBERSECURITY STYLE
# =====================================
st.markdown("""
<style>
    /* Global Background - Deep Slate/Charcoal (Real SOC Aesthetic) */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e0e0e0;
    }

    /* Typography Configuration */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Times New Roman', Times, serif !important;
        color: #ffffff !important;
        font-weight: bold;
        letter-spacing: 0.5px;
    }

    h1 {
        border-bottom: 2px solid #0f3460;
        padding-bottom: 15px;
        margin-bottom: 20px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    p, li, div, span, label, a, button {
        font-family: 'Times New Roman', Times, serif !important;
        color: #c5c5c5 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Navigation Tabs - Technical/Professional Look */
    .stTabs [data-testid="stTab"] {
        color: #a8b2d1;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.9rem;
        background: transparent;
        border: 1px solid transparent;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #0f3460;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: #0f3460;
        color: #ffffff !important;
        border: 1px solid #16213e;
        border-bottom: 1px solid #16213e;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
        font-weight: bold;
    }

    /* Metric Cards - Dark Technical Style */
    [data-testid="stMetric"] {
        background: #0f3460;
        border: 1px solid #1a1a2e;
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    [data-testid="stMetricValue"] {
        color: #00f3ff !important; /* Cyan for data values */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 700;
        font-size: 2.0rem !important;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
    }

    [data-testid="stMetricLabel"] {
        color: #a8b2d1 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Tables - Dark Grid Style */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid #0f3460;
        border-radius: 4px;
        background: #16213e;
        color: #e0e0e0;
    }

    /* Alert Boxes - Professional Security Alerts */
    .threat-high {
        background: rgba(211, 84, 0, 0.15);
        border-left: 5px solid #d35400;
        padding: 25px;
        border-radius: 4px;
        color: #ffccbc !important;
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.2);
    }

    .threat-high h1, .threat-high h3, .threat-high p {
        color: #ffccbc !important;
    }

    .threat-critical {
        background: rgba(192, 57, 43, 0.15);
        border-left: 5px solid #c0392b;
        padding: 25px;
        border-radius: 4px;
        color: #ffcdd2 !important;
        box-shadow: 0 4px 15px rgba(192, 57, 43, 0.2);
    }

    .threat-critical h1, .threat-critical h3, .threat-critical p {
        color: #ffcdd2 !important;
    }

    .threat-moderate {
        background: rgba(39, 174, 96, 0.15);
        border-left: 5px solid #27ae60;
        padding: 25px;
        border-radius: 4px;
        color: #b2dfdb !important;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.2);
    }

    .threat-moderate h1, .threat-moderate h3, .threat-moderate p {
        color: #b2dfdb !important;
    }

    /* Info/Warning Boxes - Dark Theme Adapted */
    .stAlert {
        background: #0f3460;
        border: 1px solid #1a1a2e;
        color: #e0e0e0 !important;
    }
    .stAlert p {
        color: #e0e0e0 !important;
    }
    
    /* Divider */
    hr {
        border-color: #0f3460 !important;
    }

    /* Professional Container for sections */
    .professional-container {
        background: #0f3460;
        border: 1px solid #1a1a2e;
        border-radius: 4px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
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
            <h4 style="color: #a8b2d1; margin:0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Core Algorithm</h4>
            <h2 style="margin: 15px 0; color: #00f3ff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;">XGBoost</h2>
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
            <h4 style="color: #a8b2d1; margin:0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Forecast Horizon</h4>
            <h2 style="margin: 15px 0; color: #00f3ff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;">2027</h2>
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
# PROJECT OVERVIEW (FIXED CONTENT)
# =====================================
with overview:
    st.title("Project Overview & Research Context")
    
    # Content is now placed directly without empty containers
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
    
    st.warning("Parameter Significance: Each parameter is weighted by the model based on its historical correlation with threat escalation. Economic instability and patch delays often show high correlation with increased attack surfaces.")
