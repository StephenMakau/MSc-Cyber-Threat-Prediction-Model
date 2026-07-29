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
# PROFESSIONAL LIGHT THEME WITH CALIBRI
# =====================================
st.markdown("""
<style>
    /* 
       COLOR PALETTE: Modern Enterprise Security (Light Mode)
       - Background: Light Slate/Blue-Grey (#f1f5f9 to #ffffff)
       - Primary: Deep Navy (#1e3a8a)
       - Accent: Electric Blue (#2563eb)
       - Text: Dark Slate (#334155)
       - Font: Calibri for body (as requested)
    */

    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #f1f5f9 0%, #ffffff 100%);
        color: #334155;
    }

    /* Typography: Headers - Clean Sans-Serif */
    h1, h2, h3, h4, h5, h6 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: #1e3a8a !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    h1 {
        border-bottom: 3px solid #2563eb;
        padding-bottom: 15px;
        margin-bottom: 25px;
        font-size: 2.5rem !important;
        color: #1e3a8a !important;
    }

    h2 {
        color: #2563eb !important;
        margin-top: 30px;
        font-size: 1.8rem !important;
    }
    
    h3 {
        color: #3b82f6 !important;
        margin-top: 25px;
        font-size: 1.4rem !important;
    }

    /* Body Text: Calibri as requested */
    p, li, div, span, label, .stMarkdown, .stAlert, .stDataFrame, .stTable {
        font-family: Calibri, 'Segoe UI', Candara, sans-serif !important;
        color: #334155 !important;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    /* Specific paragraph styling */
    p {
        margin-bottom: 1rem !important;
    }
    
    /* List items */
    li {
        margin-bottom: 0.5rem !important;
        font-family: Calibri, 'Segoe UI', Candara, sans-serif !important;
    }

    /* Navigation Tabs - Professional Style with Icons */
    .stTabs [data-testid="stTab"] {
        color: #64748b;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.95rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        margin: 0 4px;
        transition: all 0.3s ease;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #2563eb;
        background: #f1f5f9;
        border-color: #2563eb;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: #2563eb;
        color: #ffffff !important;
        border: 1px solid #2563eb;
        border-bottom: none;
        font-weight: 700;
        box-shadow: 0 -4px 12px rgba(37, 99, 235, 0.2);
    }

    /* Metric Cards - Clean White Style */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border-color: #2563eb;
    }

    [data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 800;
        font-size: 2.8rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Tables - Clean Professional Style */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background: #ffffff;
        color: #334155;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Alert Boxes - Professional Security Alerts */
    .threat-high {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        border-left: 6px solid #f97316;
        border-radius: 8px;
        padding: 30px;
        color: #9a3412 !important;
        box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.1);
    }

    .threat-high h1 {
        color: #c2410c !important;
        border-bottom: none;
        font-size: 2rem !important;
        margin-bottom: 10px !important;
    }
    
    .threat-high h3 {
        color: #ea580c !important;
        margin-top: 0 !important;
    }
    
    .threat-high p {
        color: #7c2d12 !important;
        font-family: Calibri, 'Segoe UI', sans-serif !important;
    }

    .threat-critical {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 6px solid #ef4444;
        border-radius: 8px;
        padding: 30px;
        color: #b91c1c !important;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1);
    }

    .threat-critical h1 {
        color: #dc2626 !important;
        border-bottom: none;
        font-size: 2rem !important;
        margin-bottom: 10px !important;
    }
    
    .threat-critical h3 {
        color: #dc2626 !important;
        margin-top: 0 !important;
    }
    
    .threat-critical p {
        color: #991b1b !important;
        font-family: Calibri, 'Segoe UI', sans-serif !important;
    }

    .threat-moderate {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 6px solid #10b981;
        border-radius: 8px;
        padding: 30px;
        color: #047857 !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1);
    }

    .threat-moderate h1 {
        color: #059669 !important;
        border-bottom: none;
        font-size: 2rem !important;
        margin-bottom: 10px !important;
    }
    
    .threat-moderate h3 {
        color: #059669 !important;
        margin-top: 0 !important;
    }
    
    .threat-moderate p {
        color: #065f46 !important;
        font-family: Calibri, 'Segoe UI', sans-serif !important;
    }

    /* Info/Warning Boxes - Light Theme */
    .stAlert {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #334155 !important;
        border-radius: 8px;
        font-family: Calibri, 'Segoe UI', sans-serif !important;
    }
    
    .stAlert p {
        color: #334155 !important;
        font-family: Calibri, 'Segoe UI', sans-serif !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: #64748b !important;
        font-family: Calibri, 'Segoe UI', sans-serif !important;
        font-size: 0.9rem;
    }
    
    /* Divider */
    hr {
        border-color: #e2e8f0 !important;
        margin: 30px 0 !important;
    }

    /* Professional Container for sections */
    .professional-container {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Strong/Bold text in body */
    strong, b {
        color: #1e3a8a !important;
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
            <h4 style="color: #64748b; margin:0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; font-family: Calibri, sans-serif;">Core Algorithm</h4>
            <h2 style="margin: 15px 0; color: #2563eb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important; font-size: 2.2rem;">XGBoost</h2>
            <p style="color: #64748b; font-size: 0.9rem; font-family: Calibri, sans-serif;">Advanced Gradient Boosting</p>
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
            <h4 style="color: #64748b; margin:0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; font-family: Calibri, sans-serif;">Forecast Horizon</h4>
            <h2 style="margin: 15px 0; color: #2563eb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important; font-size: 2.2rem;">2027</h2>
            <p style="color: #64748b; font-size: 0.9rem; font-family: Calibri, sans-serif;">Predictive Analysis</p>
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
