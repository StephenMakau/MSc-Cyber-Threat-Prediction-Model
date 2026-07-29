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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# COMPACT FUTURISTIC DARK THEME
# =====================================
st.markdown("""
<style>
    /* COMPACT LAYOUT - Reduced spacing everywhere */
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0b1120 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Compact Headers */
    h1 {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-bottom: 2px solid rgba(6, 182, 212, 0.3);
        padding-bottom: 8px !important;
        margin-bottom: 15px !important;
        margin-top: 0 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }

    h2 {
        font-family: 'Inter', sans-serif !important;
        color: #06b6d4 !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        font-size: 1.4rem !important;
        border-left: 3px solid #06b6d4;
        padding-left: 12px;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
        line-height: 1.3 !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        color: #8b5cf6 !important;
        margin-top: 15px !important;
        margin-bottom: 8px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
    }

    /* Compact Body Text */
    p, li, div, span, label, .stMarkdown, .stAlert {
        font-family: Calibri, 'Segoe UI', sans-serif !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        margin-bottom: 8px !important;
    }
    
    li {
        margin-bottom: 4px !important;
    }

    /* Navigation Tabs - Compact & Close Together */
    .stTabs [data-testid="stTab"] {
        color: #94a3b8;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        font-size: 0.85rem;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 0;
        padding: 8px 16px !important;
        margin: 0 -1px 10px 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        height: 40px !important;
    }

    .stTabs [data-testid="stTab"]:first-child {
        border-radius: 6px 0 0 6px;
    }

    .stTabs [data-testid="stTab"]:last-child {
        border-radius: 0 6px 6px 0;
        margin-right: 0;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.1);
        border-color: #06b6d4;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
        z-index: 1;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        color: #ffffff !important;
        border: 1px solid #06b6d4;
        font-weight: 700;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.5);
        z-index: 2;
    }

    /* Compact Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 10px;
        padding: 15px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #06b6d4;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #3b82f6);
    }

    [data-testid="stMetricValue"] {
        color: #06b6d4 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700;
        font-size: 2rem !important;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
        margin-bottom: 5px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0 !important;
    }

    /* Compact Tables */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 8px;
        background: rgba(15, 23, 42, 0.8);
        color: #f8fafc;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }
    
    .stDataFrame td, .stDataFrame th {
        color: #e2e8f0 !important;
        border-bottom: 1px solid rgba(6, 182, 212, 0.1) !important;
        padding: 8px !important;
        font-size: 0.9rem !important;
    }
    
    .stDataFrame th {
        background: rgba(6, 182, 212, 0.1) !important;
        color: #06b6d4 !important;
        font-weight: 600 !important;
    }

    /* Compact Alert Boxes */
    .threat-high, .threat-critical, .threat-moderate {
        padding: 20px !important;
        border-radius: 8px;
        margin-bottom: 15px !important;
    }

    .threat-high {
        background: rgba(251, 188, 4, 0.1);
        border: 1px solid rgba(251, 188, 4, 0.5);
        border-left: 4px solid #fbbf24;
        color: #fcd34d !important;
        box-shadow: 0 0 15px rgba(251, 188, 4, 0.2);
    }

    .threat-high h1 {
        color: #fbbf24 !important;
        -webkit-text-fill-color: #fbbf24;
        font-size: 1.6rem !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 10px rgba(251, 188, 4, 0.5);
        line-height: 1.2 !important;
    }
    
    .threat-high h3 {
        color: #f59e0b !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
    }
    
    .threat-high p {
        color: #fde68a !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
    }

    .threat-critical {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.5);
        border-left: 4px solid #ef4444;
        color: #fca5a5 !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
    }

    .threat-critical h1 {
        color: #ef4444 !important;
        -webkit-text-fill-color: #ef4444;
        font-size: 1.6rem !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
        line-height: 1.2 !important;
    }
    
    .threat-critical h3 {
        color: #f87171 !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
    }
    
    .threat-critical p {
        color: #fecaca !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
    }

    .threat-moderate {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.5);
        border-left: 4px solid #10b981;
        color: #6ee7b7 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }

    .threat-moderate h1 {
        color: #34d399 !important;
        -webkit-text-fill-color: #34d399;
        font-size: 1.6rem !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        line-height: 1.2 !important;
    }
    
    .threat-moderate h3 {
        color: #10b981 !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
    }
    
    .threat-moderate p {
        color: #a7f3d0 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
    }

    /* Compact Info Boxes */
    .stAlert {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: #06b6d4 !important;
        border-radius: 8px;
        font-family: Calibri, sans-serif !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        padding: 12px !important;
        margin-bottom: 15px !important;
    }
    
    .stAlert p {
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
    }
    
    /* Compact Caption */
    .stCaption {
        color: #64748b !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        margin-bottom: 10px !important;
    }
    
    /* Compact Divider */
    hr {
        border-color: rgba(6, 182, 212, 0.2) !important;
        margin: 20px 0 !important;
    }

    /* Compact Tech Container */
    .tech-container {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 10px;
        padding: 20px !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .tech-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #3b82f6);
    }
    
    /* Strong text */
    strong, b {
        color: #06b6d4 !important;
        font-weight: 700;
    }
    
    /* Reduce default Streamlit spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    
    /* Compact columns */
    .row-widget.stHorizontal {
        gap: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION WITH ICONS - CLOSE TOGETHER
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
    st.title("🛡️ CYBER THREAT INTELLIGENCE")
    st.caption(f"SYS.TIME: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d/%m/%Y | %H:%M:%S')} EAT | STATUS: ONLINE | OPERATOR: Stephen Musau Makau")
    
    # Prediction Engine
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    # Metrics Row
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("CORE ALGORITHM", "XGBoost", help="ML.Engine.GradientBoost")

    with c2:
        st.metric("MODEL ACCURACY", f"{accuracy:.2f}%", help="Training validation")

    with c3:
        st.metric("TARGET YEAR", "2027", help="Forecast.Horizon")

    # Threat Display
    st.markdown("### 🚨 THREAT PROJECTION // 2027")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1>⚠️ HIGH RISK DETECTED</h1>
            <h3>THREAT_LEVEL: HIGH</h3>
            <p>Predictive algorithms indicate significant escalation in cyber threats. Immediate countermeasures required.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1>🛑 CRITICAL ALERT</h1>
            <h3>THREAT_LEVEL: CRITICAL</h3>
            <p>Maximum threat level detected. Emergency protocols activated. Raise all defensive systems.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1>✅ STABLE STATUS</h1>
            <h3>THREAT_LEVEL: MODERATE</h3>
            <p>Threat parameters within acceptable ranges. Standard monitoring protocols sufficient.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# PROJECT OVERVIEW
# =====================================
with overview:
    st.title("📄 SYSTEM OVERVIEW")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 MISSION")
        st.write("Advanced predictive intelligence for Kenyan Government Digital Services. ML algorithms forecast threat evolution.")
        
        st.subheader("⚠️ THREAT LANDSCAPE")
        st.write("Digital transformation correlates with exponential threat growth. Conventional defenses inadequate.")
    
    with col2:
        st.subheader("🔬 ARCHITECTURE")
        st.markdown("""
        - **Attack Vectors:** DDoS, Malware, Phishing
        - **Vulnerability Metrics:** CVE Criticality
        - **Network Intelligence:** Traffic Anomalies
        - **Economic Indicators:** Inflation/GDP correlation
        """)
        
        st.subheader("🌍 IMPACT")
        st.markdown("""
        - Critical Infrastructure Protection
        - Resource Optimization
        - Policy Intelligence
        """)

    st.info("🔒 SECURITY PROTOCOL: All data synthetic/anonymized.")

# =====================================
# DATASET
# =====================================
with dataset:
    st.title("📊 DATA MATRIX")
    st.dataframe(get_dataset(), use_container_width=True, height=400)

# =====================================
# MODELS
# =====================================
with models:
    st.title("🤖 AI CORE PERFORMANCE")
    
    results = get_results()
    table_data = []
    for name, value in results.items():
        table_data.append({
            "Algorithm": name,
            "Accuracy": f"{value*100:.2f}%",
            "Status": "ACTIVE" if name == "XGBoost" else "STANDBY"
        })
    
    st.table(table_data)
    st.warning("⚠️ XGBoost selected for production deployment.")

# =====================================
# PARAMETERS
# =====================================
with parameters:
    st.title("⚙️ SYSTEM PARAMETERS")
    st.dataframe(get_parameters(), use_container_width=True, height=350)
    st.warning("⚠️ Economic volatility shows highest correlation with threat escalation.")
