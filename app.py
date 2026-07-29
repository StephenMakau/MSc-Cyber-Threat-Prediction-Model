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
    page_icon="🛡️",  # This sets the browser tab icon to a shield
    layout="wide"
)

# =====================================
# PROFESSIONAL LIGHT THEME WITH SVG ICONS
# =====================================
st.markdown("""
<style>
    /* 
       COLOR PALETTE: Modern Enterprise Security (Light Mode)
       - Background: Light Slate/Blue-Grey Gradient (#f0f4f8 to #ffffff)
       - Primary: Deep Navy (#1e3a8a)
       - Accent: Electric Blue (#2563eb)
       - Text: Dark Slate (#1e293b)
    */

    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);
        color: #1e293b;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: #1e3a8a !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    h1 {
        border-bottom: 2px solid #2563eb;
        padding-bottom: 15px;
        margin-bottom: 20px;
        font-size: 2.5rem !important;
        color: #1e3a8a !important;
    }

    h2, h3 {
        color: #2563eb !important;
        margin-top: 20px;
    }

    p, li, div, span, label, a, button, .stMarkdown, .stAlert {
        font-family: 'Times New Roman', Times, serif !important;
        color: #334155 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Navigation Tabs - Clean Professional Style */
    .stTabs [data-testid="stTab"] {
        color: #64748b;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.9rem;
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 10px 20px;
        margin: 0 5px;
        transition: all 0.3s ease;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #2563eb;
        background: #f1f5f9;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: #2563eb;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        font-weight: 700;
    }

    /* Metric Cards - White with Shadow and Border */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid #2563eb;
    }

    [data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 800;
        font-size: 2.5rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Tables - Clean Light Grid */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background: #ffffff;
        color: #1e293b;
    }

    /* Alert Boxes - Professional Security Alerts */
    .threat-high {
        background: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 30px;
        border-radius: 8px;
        color: #9a3412 !important;
        box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.1);
    }

    .threat-high h1, .threat-high h3, .threat-high p {
        color: #9a3412 !important;
    }

    .threat-critical {
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 30px;
        border-radius: 8px;
        color: #b91c1c !important;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1);
    }

    .threat-critical h1, .threat-critical h3, .threat-critical p {
        color: #b91c1c !important;
    }

    .threat-moderate {
        background: #ecfdf5;
        border-left: 5px solid #10b981;
        padding: 30px;
        border-radius: 8px;
        color: #047857 !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1);
    }

    .threat-moderate h1, .threat-moderate h3, .threat-moderate p {
        color: #047857 !important;
    }

    /* Info/Warning Boxes - Light Theme Adapted */
    .stAlert {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #1e293b !important;
        border-radius: 8px;
    }
    .stAlert p {
        color: #1e293b !important;
    }
    
    /* Divider */
    hr {
        border-color: #e2e8f0 !important;
    }

    /* Professional Container for sections */
    .professional-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Icon Styling */
    .icon-svg {
        width: 24px;
        height: 24px;
        vertical-align: middle;
        margin-right: 8px;
        fill: currentColor;
    }
    .header-icon {
        width: 32px;
        height: 32px;
        vertical-align: middle;
        margin-right: 12px;
        fill: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# ICON DEFINITIONS (SVG)
# =====================================
ICON_HOME = '<svg class="header-icon" viewBox="0 0 24 24"><path d="="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>'
ICON_OVERVIEW = '<svg class="header-icon" viewBox="0 0 24 24"><path d="="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.83L17.17 9H13z"/></svg>'
ICON_DATASET = '<svg class="header-icon" viewBox="0 0 24 24"><path d="="M20 3H4c-1.1 0-2.0.9-2.0 2.0v14c0 1.1.9 2.0 2.0 2.0h16c1.1 0 2.0-.9 2.0-2.0V5c0-1.1-.9-2.0-2.0-2.0zm0 16H4V5h16v14z"/><path d="="M12 7c-1.1 0-2.0.9-2.0 2.0s.9 2.0 2.0 2.0 2.0-.9 2.0-2.0-.9-2.0-2.0-2.0zm0 10c-2.67 0-8.0 1.34-8.0 4.0v2.0h16v-2.0c0-2.66-5.33-4.0-8.0-4.0z"/></svg>'
ICON_MODELS = '<svg class="header-icon" viewBox="0 0 24 24"><path d="="M21 2H3c-1.1 0-2.0.9-2.0 2.0v14c0 1.1.9 2.0 2.0 2.0h16c1.1 0 2.0-.9 2.0-2.0V4c0-1.1-.9-2.0-2.0-2.0zm0 16H3V4h16v14zm-10-10h2v2h-2zm0 4h2v6h-2z"/></svg>'
ICON_PARAMS = '<svg class="header-icon" viewBox="0 0 24 24"><path d="="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 00.12-.61l-1.92-3.32a.488.488 0 00-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 00-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.17.47-.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58a.48.48 0 00-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0.43-.17.47-.41l.36-2.54c.59-.24 1.13-.57 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.17-.47.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>'
ICON_WARNING = '<svg style="width:20px;height:20px;vertical-align:middle;margin-right:8px;fill:currentcolor;" viewBox="0 0 24 24"><path d="="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>'

# =====================================
# NAVIGATION
# =====================================
home, overview, dataset, models, parameters = st.tabs(
    [
        f"{ICON_HOME} HOME",
        f"{ICON_OVERVIEW} PROJECT OVERVIEW",
        f"{ICON_DATASET} DATASET",
        f"{ICON_MODELS} AI MODELS",
        f"{ICON_PARAMS} PARAMETERS"
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
            <h4 style="color: #64748b; margin:0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px;">Core Algorithm</h4>
            <h2 style="margin: 15px 0; color: #2563eb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;">XGBoost</h2>
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
            <h4 style="color: #64748b; margin:0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px;">Forecast Horizon</h4>
            <h2 style="margin: 15px 0; color: #2563eb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;">2027</h2>
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
            <h3 style="color: #10b981;">Predicted Threat Level: MODERATE</h3>
            <p>Threat levels are within manageable parameters. Continue standard monitoring and maintenance protocols.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# PROJECT OVERVIEW
# =====================================
with overview:
    st.title("Project Overview & Research Context")
    
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
    
    st.warning(f"{ICON_WARNING} Note: XGBoost was selected as the primary model due to superior performance in handling imbalanced cybersecurity datasets and complex non-linear relationships.")

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
    
    st.warning(f"{ICON_WARNING} Parameter Significance: Each parameter is weighted by the model based on its historical correlation with threat escalation. Economic instability and patch delays often show high correlation with increased attack surfaces.")
