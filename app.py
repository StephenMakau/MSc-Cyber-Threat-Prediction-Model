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
# FUTURISTIC DARK TECH THEME
# =====================================
st.markdown("""
<style>
    /* 
       FUTURISTIC DARK THEME - SOC Dashboard Style
       - Background: Deep Slate (#0b1120 to #1e293b)
       - Text: High Contrast White (#f8fafc)
       - Accents: Neon Cyan (#06b6d4), Electric Blue (#3b82f6), Purple (#8b5cf6)
    */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Background - Deep Tech Dark */
    .stApp {
        background: linear-gradient(135deg, #0b1120 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Typography - High Contrast */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #f8fafc !important;
        font-weight: 700;
        letter-spacing: -0.02em;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
    }

    h1 {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-bottom: 2px solid rgba(6, 182, 212, 0.3);
        padding-bottom: 20px;
        margin-bottom: 30px;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #06b6d4 !important;
        margin-top: 35px;
        font-size: 2rem !important;
        border-left: 4px solid #06b6d4;
        padding-left: 20px;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }
    
    h3 {
        color: #8b5cf6 !important;
        margin-top: 25px;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }

    /* Body Text: Calibri with High Contrast */
    p, li, div, span, label, .stMarkdown, .stAlert {
        font-family: Calibri, 'Segoe UI', sans-serif !important;
        color: #e2e8f0 !important;
        font-size: 1.2rem;
        line-height: 1.8;
        font-weight: 400;
    }
    
    p {
        margin-bottom: 1.2rem !important;
        color: #cbd5e1 !important;
    }
    
    li {
        margin-bottom: 0.8rem !important;
        color: #cbd5e1 !important;
        font-family: Calibri, sans-serif !important;
    }

    /* Navigation Tabs - CLOSE TOGETHER (NO GAP) */
    .stTabs [data-testid="stTab"] {
        color: #94a3b8;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        font-size: 1rem;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 0;
        padding: 12px 24px;
        margin: 0 -1px 15px 0;  /* Negative margin to overlap borders */
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
    }

    .stTabs [data-testid="stTab"]:first-child {
        border-radius: 8px 0 0 8px;
    }

    .stTabs [data-testid="stTab"]:last-child {
        border-radius: 0 8px 8px 0;
        margin-right: 0;
    }

    .stTabs [data-testid="stTab"]:hover {
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.1);
        border-color: #06b6d4;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
        z-index: 1;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        color: #ffffff !important;
        border: 1px solid #06b6d4;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
        z-index: 2;
    }

    /* Metric Cards - Futuristic Glass */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.1);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #06b6d4;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.3), inset 0 1px 0 rgba(255,255,255,0.1);
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #3b82f6);
    }

    [data-testid="stMetricValue"] {
        color: #06b6d4 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700;
        font-size: 3rem !important;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 10px;
    }

    /* Tables - Dark Tech Style */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.8);
        color: #f8fafc;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .stDataFrame td, .stDataFrame th {
        color: #e2e8f0 !important;
        border-bottom: 1px solid rgba(6, 182, 212, 0.1) !important;
    }
    
    .stDataFrame th {
        background: rgba(6, 182, 212, 0.1) !important;
        color: #06b6d4 !important;
        font-weight: 600 !important;
    }

    /* Alert Boxes - Neon Glow Style */
    .threat-high {
        background: rgba(251, 188, 4, 0.1);
        border: 1px solid rgba(251, 188, 4, 0.5);
        border-left: 6px solid #fbbf24;
        border-radius: 12px;
        padding: 30px;
        color: #fcd34d !important;
        box-shadow: 0 0 30px rgba(251, 188, 4, 0.2), inset 0 1px 0 rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }

    .threat-high h1 {
        color: #fbbf24 !important;
        -webkit-text-fill-color: #fbbf24;
        border-bottom: none;
        font-size: 2.2rem !important;
        margin-bottom: 10px !important;
        text-shadow: 0 0 20px rgba(251, 188, 4, 0.5);
    }
    
    .threat-high h3 {
        color: #f59e0b !important;
        margin-top: 0 !important;
        border-left: none;
        padding-left: 0;
        text-shadow: 0 0 10px rgba(251, 188, 4, 0.3);
    }
    
    .threat-high p {
        color: #fde68a !important;
        font-family: Calibri, sans-serif !important;
    }

    .threat-critical {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.5);
        border-left: 6px solid #ef4444;
        border-radius: 12px;
        padding: 30px;
        color: #fca5a5 !important;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.2), inset 0 1px 0 rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }

    .threat-critical h1 {
        color: #ef4444 !important;
        -webkit-text-fill-color: #ef4444;
        border-bottom: none;
        font-size: 2.2rem !important;
        margin-bottom: 10px !important;
        text-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
    }
    
    .threat-critical h3 {
        color: #f87171 !important;
        margin-top: 0 !important;
        border-left: none;
        padding-left: 0;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    .threat-critical p {
        color: #fecaca !important;
        font-family: Calibri, sans-serif !important;
    }

    .threat-moderate {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.5);
        border-left: 6px solid #10b981;
        border-radius: 12px;
        padding: 30px;
        color: #6ee7b7 !important;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.2), inset 0 1px 0 rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }

    .threat-moderate h1 {
        color: #34d399 !important;
        -webkit-text-fill-color: #34d399;
        border-bottom: none;
        font-size: 2.2rem !important;
        margin-bottom: 10px !important;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    
    .threat-moderate h3 {
        color: #10b981 !important;
        margin-top: 0 !important;
        border-left: none;
        padding-left: 0;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    
    .threat-moderate p {
        color: #a7f3d0 !important;
        font-family: Calibri, sans-serif !important;
    }

    /* Info/Warning Boxes - Tech Style */
    .stAlert {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: #06b6d4 !important;
        border-radius: 12px;
        font-family: Calibri, sans-serif !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stAlert p {
        color: #e2e8f0 !important;
        font-family: Calibri, sans-serif !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: #64748b !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(6, 182, 212, 0.2) !important;
        margin: 35px 0 !important;
    }

    /* Professional Container - Glassmorphism */
    .tech-container {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05);
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
    
    /* Strong text - Neon effect */
    strong, b {
        color: #06b6d4 !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #06b6d4;
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
    st.subheader("SYSTEM v2.0.7 | Mount Kenya University")
    st.markdown("**Operator:** Stephen Musau Makau | **Clearance:** MSc Cybersecurity")
    st.caption(f"⏱️ SYS.TIME: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d/%m/%Y | %H:%M:%S')} EAT | STATUS: ONLINE")
    
    st.divider()

    # Prediction Engine
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    st.markdown("### 📡 THREAT ASSESSMENT MODULE")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="tech-container" style="text-align: center;">
            <h4 style="color: #94a3b8; margin:15px 0 0 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; font-family: Inter, sans-serif;">Core Algorithm</h4>
            <h2 style="margin: 20px 0; color: #06b6d4; font-family: JetBrains Mono, monospace !important; font-size: 2.6rem; font-weight: 700; text-shadow: 0 0 15px rgba(6,182,212,0.5);">XGBoost</h2>
            <p style="color: #64748b; font-size: 0.95rem; font-family: Calibri, sans-serif; margin-bottom: 15px;">ML.Engine.GradientBoost</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.metric(
            "🎯 MODEL ACCURACY",
            f"{accuracy:.2f}%",
            help="Training validation score"
        )

    with c3:
        st.markdown("""
        <div class="tech-container" style="text-align: center;">
            <h4 style="color: #94a3b8; margin:15px 0 0 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; font-family: Inter, sans-serif;">Target Year</h4>
            <h2 style="margin: 20px 0; color: #8b5cf6; font-family: JetBrains Mono, monospace !important; font-size: 2.6rem; font-weight: 700; text-shadow: 0 0 15px rgba(139,92,246,0.5);">2027</h2>
            <p style="color: #64748b; font-size: 0.95rem; font-family: Calibri, sans-serif; margin-bottom: 15px;">Forecast.Horizon</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Threat Display
    st.header("🚨 THREAT PROJECTION // 2027")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1>⚠️ HIGH RISK DETECTED</h1>
            <h3>THREAT_LEVEL: HIGH</h3>
            <p>Predictive algorithms indicate significant escalation in cyber threats targeting critical infrastructure. Immediate countermeasures required. Threat vectors include advanced persistent threats (APTs) and zero-day exploits.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1>🛑 CRITICAL ALERT</h1>
            <h3>THREAT_LEVEL: CRITICAL</h3>
            <p>Maximum threat level detected. System predicts unprecedented attack surge. Emergency protocols activated. All defensive systems should be raised to maximum alert status immediately.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1>✅ STABLE STATUS</h1>
            <h3>THREAT_LEVEL: MODERATE</h3>
            <p>Threat parameters within acceptable ranges. Standard monitoring protocols sufficient. Continue baseline security operations and routine system audits.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# PROJECT OVERVIEW
# =====================================
with overview:
    st.title("📄 SYSTEM OVERVIEW")
    
    st.subheader("🎯 MISSION OBJECTIVE")
    st.write("""
    Advanced predictive intelligence platform for Kenyan Government Digital Services. 
    Deploys machine learning algorithms to forecast cyber threat evolution and enable proactive defense strategies.
    """)

    st.subheader("⚠️ THREAT LANDSCAPE")
    st.write("""
    Digital transformation acceleration correlates with exponential threat growth. 
    Conventional reactive defenses inadequate against modern attack vectors. 
    Critical infrastructure requires predictive capabilities.
    """)

    st.subheader("🔬 SYSTEM ARCHITECTURE")
    st.write("""
    Core engine utilizes **XGBoost Neural Networks** processing multi-dimensional correlation matrices:
    """)
    st.markdown("""
    - **🎯 Attack Vectors:** DDoS, Malware, Phishing, Web Exploits
    - **🔒 Vulnerability Metrics:** CVE Criticality, Patch Latency
    - **📡 Network Intelligence:** Traffic Anomaly Detection
    - **📈 Economic Indicators:** Inflation/GDP correlation algorithms
    
    Predictive synthesis enables pre-emptive resource allocation.
    """)

    st.subheader("🌍 OPERATIONAL IMPACT")
    st.markdown("""
    - **🏛️ Critical Infrastructure Protection**
    - **💰 Resource Optimization**
    - **📋 Policy Intelligence**
    - **🤝 Public Trust Maintenance**
    """)

    st.info("🔒 **SECURITY PROTOCOL:** All data synthetic/anonymized. No live government feeds.")

# =====================================
# DATASET
# =====================================
with dataset:
    st.title("📊 DATA MATRIX")
    st.markdown("Accessing classified training datasets...")
    st.dataframe(
        get_dataset(),
        use_container_width=True,
        height=600
    )

# =====================================
# MODELS
# =====================================
with models:
    st.title("🤖 AI CORE PERFORMANCE")
    st.markdown("Algorithmic benchmarking and selection metrics...")
    
    results = get_results()
    table_data = []
    for name, value in results.items():
        table_data.append({
            "Algorithm": name,
            "Accuracy": f"{value*100:.2f}%",
            "Status": "ACTIVE" if name == "XGBoost" else "STANDBY"
        })
    
    st.table(table_data)
    
    st.warning("⚠️ **SYSTEM NOTE:** XGBoost selected for production deployment. Superior handling of imbalanced threat datasets.")

# =====================================
# PARAMETERS
# =====================================
with parameters:
    st.title("⚙️ SYSTEM PARAMETERS")
    st.markdown("""
    Feature configuration for 2027 threat projection horizon.
    """)
    
    st.dataframe(
        get_parameters(),
        use_container_width=True,
        height=400
    )
    
    st.warning("⚠️ **ANALYSIS:** Economic volatility and patch latency show highest correlation with threat escalation.")
