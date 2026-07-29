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
# PROFESSIONAL CYBERSECURITY STYLE (RESEARCHED PALETTE)
# =====================================
st.markdown("""
<style>
    /* 
       COLOR PALETTE RESEARCH:
       - Background: Deep Slate (#0f172a) to Dark Charcoal (#1e293b) - Professional, deep, non-fatiguing.
       - Primary Accent: Electric Indigo (#6366f1) - Modern tech feel, distinct from generic blue.
       - Secondary Accent: Teal/Cyan (#06b6d4) - High contrast for data, represents "live" status.
       - Danger: Crimson (#ef4444) and Orange (#f97316) - Standard, clear alert colors.
       - Text: White (#ffffff) and Light Gray (#cbd5e1) - Maximum readability.
    */

    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #cbd5e1;
    }

    /* Typography: Hybrid Approach */
    /* Headers: Clean Sans-Serif for modern UI feel */
    h1, h2, h3, h4, h5, h6, [data-testid="stMetricLabel"], [data-testid="stTab"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    /* Body: Times New Roman for Academic/Research integrity as requested */
    p, li, div, span, label, a, button, .stMarkdown, .stAlert {
        font-family: 'Times New Roman', Times, serif !important;
        color: #cbd5e1 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    h1 {
        border-bottom: 2px solid #6366f1;
        padding-bottom: 15px;
        margin-bottom: 20px;
        font-size: 2.5rem !important;
        text-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }

    h2, h3 {
        color: #06b6d4 !important; /* Teal for subheaders to differentiate */
        margin-top: 20px;
    }

    /* Navigation Tabs - Modern Glass Style */
    .stTabs [data-testid="stTab"] {
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        margin: 0 5px;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #ffffff !important;
        border: none;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        font-weight: 700;
    }

    /* Metric Cards - Glassmorphism with Teal Accent */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
        transition: transform 0.2s;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(6, 182, 212, 0.5);
    }

    [data-testid="stMetricValue"] {
        color: #06b6d4 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 800;
        font-size: 2.5rem !important;
        text-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Tables - Clean Dark Grid */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        background: rgba(30, 41, 59, 0.5);
        color: #e2e8f0;
    }

    /* Alert Boxes - Professional, Non-Cartoonish */
    .threat-high {
        background: rgba(249, 115, 22, 0.1);
        border-left: 5px solid #f97316;
        padding: 30px;
        border-radius: 8px;
        color: #fb923c !important;
        box-shadow: 0 4px 20px rgba(249, 115, 22, 0.2);
    }

    .threat-high h1, .threat-high h3, .threat-high p {
        color: #fb923c !important;
    }

    .threat-critical {
        background: rgba(239, 68, 68, 0.1);
        border-left: 5px solid #ef4444;
        padding: 30px;
        border-radius: 8px;
        color: #f87171 !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);
    }

    .threat-critical h1, .threat-critical h3, .threat-critical p {
        color: #f87171 !important;
    }

    .threat-moderate {
        background: rgba(52, 211, 153, 0.1);
        border-left: 5px solid #34d399;
        padding: 30px;
        border-radius: 8px;
        color: #6ee7b7 !important;
        box-shadow: 0 4px 20px rgba(52, 211, 153, 0.2);
    }

    .threat-moderate h1, .threat-moderate h3, .threat-moderate p {
        color: #6ee7b7 !important;
    }

    /* Info/Warning Boxes - Adapted to Dark Theme */
    .stAlert {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #e2e8f0 !important;
        border-radius: 8px;
    }
    .stAlert p {
        color: #e2e8f0 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(148, 163, 184, 0.1) !important;
    }

    /* Professional Container for sections - Glassmorphism */
    .professional-container {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
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
            <h4 style="color: #94a3b8; margin:0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px;">Core Algorithm</h4>
            <h2 style="margin: 15px 0; color: #6366f1; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;">XGBoost</h2>
            <p style="color: #64748b; font-size: 0.8rem;">Advanced Gradient Boosting</p>
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
            <h4 style="color: #94a3b8; margin:0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px;">Forecast Horizon</h4>
            <h2 style="margin: 15px 0; color: #6366f1; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;">2027</h2>
            <p style="color: #64748b; font-size: 0.8rem;">Predictive Analysis</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Threat Display
    st.header("2027 Threat Projection")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1 style="margin:0;">HIGH RISK DETECTED</h1>
            <h3 style="color: #f97316;">Predicted Threat Level: HIGH</h3>
            <p>The predictive model indicates a significant escalation in cyber threats targeting government digital infrastructure. Immediate proactive measures and resource allocation are recommended.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1 style="margin:0;">CRITICAL ALERT</h1>
            <h3 style="color: #ef4444;">Predicted Threat Level: CRITICAL</h3>
            <p>Critical infrastructure vulnerability detected. The model forecasts an unprecedented surge in attack vectors. Emergency protocols should be reviewed immediately.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1 style="margin:0;">STABLE STATUS</h1>
            <h3 style="color: #34d399;">Predicted Threat Level: MODERATE</h3>
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
