import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import base64

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
# BACKGROUND IMAGE WITH DARK OVERLAY
# =====================================
# Get image and convert to base64 for CSS background
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# For uploaded image reference - using the provided image ID
# In production, replace with actual image path or use st.image with use_column_width
try:
    # Attempt to use the uploaded image if available locally
    img_base64 = get_img_as_base64("img-1785342036164-vgwr5ws7n.png")
    img_url = f"data:image/png;base64,{img_base64}"
except:
    # Fallback: use a dark gradient if image not found
    img_url = "none"

st.markdown(f"""
<style>
    /* 
       BACKGROUND: Cybersecurity Shield Image with Dark Overlay
       Colors optimized for orange/gold circuit board background
    */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Background with Image and Heavy Dark Overlay for Readability */
    .stApp {{
        background-image: 
            linear-gradient(rgba(10, 10, 15, 0.88), rgba(20, 15, 10, 0.92)),
            url('{img_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: #ffffff;
    }}

    /* Typography - Maximum Visibility with Glow Effects */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: -0.02em;
        text-shadow: 
            0 0 10px rgba(0, 0, 0, 1),
            0 0 20px rgba(251, 191, 36, 0.6),
            0 2px 4px rgba(0, 0, 0, 0.9);
    }}

    h1 {{
        background: linear-gradient(90deg, #fbbf24, #f97316, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-bottom: 2px solid rgba(251, 191, 36, 0.6);
        padding-bottom: 8px !important;
        margin-bottom: 15px !important;
        margin-top: 0 !important;
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        text-shadow: none !important;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.8));
    }}

    h2 {{
        color: #fbbf24 !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        font-size: 1.5rem !important;
        border-left: 3px solid #f97316;
        padding-left: 12px;
        text-shadow: 
            0 0 10px rgba(0, 0, 0, 1),
            0 0 15px rgba(251, 191, 36, 0.5);
    }}
    
    h3 {{
        color: #22d3ee !important;
        margin-top: 15px !important;
        margin-bottom: 8px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        text-shadow: 
            0 0 10px rgba(0, 0, 0, 1),
            0 0 10px rgba(34, 211, 238, 0.5);
    }}

    /* Body Text - Bright White with Heavy Shadow for Readability */
    p, li, div, span, label, .stMarkdown, .stAlert {{
        font-family: Calibri, 'Segoe UI', sans-serif !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
        text-shadow: 
            0 0 8px rgba(0, 0, 0, 0.9),
            0 0 15px rgba(0, 0, 0, 0.7),
            0 1px 2px rgba(0, 0, 0, 1);
    }}
    
    li {{
        margin-bottom: 4px !important;
        color: #f1f5f9 !important;
    }}

    /* Navigation Tabs - Orange/Gold Theme matching image */
    .stTabs [data-testid="stTab"] {{
        color: #fed7aa;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        font-size: 0.85rem;
        background: rgba(20, 10, 5, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(251, 191, 36, 0.4);
        border-radius: 0;
        padding: 8px 16px !important;
        margin: 0 -1px 10px 0;
        transition: all 0.3s ease;
        position: relative;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }}

    .stTabs [data-testid="stTab"]:first-child {{
        border-radius: 6px 0 0 6px;
    }}

    .stTabs [data-testid="stTab"]:last-child {{
        border-radius: 0 6px 6px 0;
        margin-right: 0;
    }}

    .stTabs [data-testid="stTab"]:hover {{
        color: #ffffff;
        background: rgba(249, 115, 22, 0.3);
        border-color: #fbbf24;
        box-shadow: 0 0 15px rgba(251, 191, 36, 0.5);
        z-index: 1;
    }}

    .stTabs [data-testid="stTab"][aria-selected="true"] {{
        background: linear-gradient(135deg, #f97316, #fbbf24);
        color: #000000 !important;
        border: 1px solid #fbbf24;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(251, 191, 36, 0.7);
        z-index: 2;
        text-shadow: none;
    }}

    /* Metric Cards - Dark with Orange Glow */
    [data-testid="stMetric"] {{
        background: rgba(10, 10, 15, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(251, 191, 36, 0.5);
        border-radius: 10px;
        padding: 15px !important;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.8),
            0 0 15px rgba(251, 191, 36, 0.2);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    [data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        border-color: #fbbf24;
        box-shadow: 
            0 0 25px rgba(251, 191, 36, 0.4),
            0 4px 20px rgba(0, 0, 0, 0.8);
    }}
    
    [data-testid="stMetric"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #f97316, #fbbf24, #22d3ee);
    }}

    [data-testid="stMetricValue"] {{
        color: #fbbf24 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700;
        font-size: 2rem !important;
        text-shadow: 
            0 0 10px rgba(251, 191, 36, 0.8),
            0 0 20px rgba(251, 191, 36, 0.4);
        margin-bottom: 5px !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: #fed7aa !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.9);
    }}

    /* Tables - Dark with Orange Borders */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {{
        border: 1px solid rgba(251, 191, 36, 0.4);
        border-radius: 8px;
        background: rgba(10, 10, 15, 0.95);
        color: #ffffff;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
    }}
    
    .stDataFrame td, .stDataFrame th {{
        color: #f1f5f9 !important;
        border-bottom: 1px solid rgba(251, 191, 36, 0.2) !important;
        padding: 8px !important;
        font-size: 0.9rem !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }}
    
    .stDataFrame th {{
        background: rgba(249, 115, 22, 0.25) !important;
        color: #fbbf24 !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.9);
    }}

    /* Alert Boxes - Matching Orange Theme */
    .threat-high, .threat-critical, .threat-moderate {{
        padding: 20px !important;
        border-radius: 8px;
        margin-bottom: 15px !important;
        backdrop-filter: blur(10px);
        border: 1px solid;
    }}

    .threat-high {{
        background: rgba(180, 83, 9, 0.2);
        border-color: rgba(251, 191, 36, 0.6);
        border-left: 4px solid #fbbf24;
        color: #fef3c7 !important;
        box-shadow: 
            0 0 20px rgba(251, 191, 36, 0.3),
            inset 0 0 20px rgba(251, 191, 36, 0.05);
    }}

    .threat-high h1 {{
        color: #fbbf24 !important;
        -webkit-text-fill-color: #fbbf24;
        font-size: 1.6rem !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 15px rgba(251, 191, 36, 0.9);
        line-height: 1.2 !important;
    }}
    
    .threat-high h3 {{
        color: #f59e0b !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
        text-shadow: 0 0 10px rgba(0,0,0,0.9);
    }}
    
    .threat-high p {{
        color: #ffedd5 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.9);
    }}

    .threat-critical {{
        background: rgba(220, 38, 38, 0.2);
        border-color: rgba(239, 68, 68, 0.6);
        border-left: 4px solid #ef4444;
        color: #fee2e2 !important;
        box-shadow: 
            0 0 20px rgba(239, 68, 68, 0.3),
            inset 0 0 20px rgba(239, 68, 68, 0.05);
    }}

    .threat-critical h1 {{
        color: #ef4444 !important;
        -webkit-text-fill-color: #ef4444;
        font-size: 1.6rem !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 15px rgba(239, 68, 68, 0.9);
        line-height: 1.2 !important;
    }}
    
    .threat-critical h3 {{
        color: #f87171 !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
        text-shadow: 0 0 10px rgba(0,0,0,0.9);
    }}
    
    .threat-critical p {{
        color: #fecaca !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.9);
    }}

    .threat-moderate {{
        background: rgba(5, 150, 105, 0.2);
        border-color: rgba(16, 185, 129, 0.6);
        border-left: 4px solid #10b981;
        color: #d1fae5 !important;
        box-shadow: 
            0 0 20px rgba(16, 185, 129, 0.3),
            inset 0 0 20px rgba(16, 185, 129, 0.05);
    }}

    .threat-moderate h1 {{
        color: #34d399 !important;
        -webkit-text-fill-color: #34d399;
        font-size: 1.6rem !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 15px rgba(52, 211, 153, 0.9);
        line-height: 1.2 !important;
    }}
    
    .threat-moderate h3 {{
        color: #10b981 !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
        text-shadow: 0 0 10px rgba(0,0,0,0.9);
    }}
    
    .threat-moderate p {{
        color: #a7f3d0 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.9);
    }}

    /* Info/Warning Boxes */
    .stAlert {{
        background: rgba(10, 10, 15, 0.95);
        border: 1px solid rgba(251, 191, 36, 0.4);
        color: #fbbf24 !important;
        border-radius: 8px;
        font-family: Calibri, sans-serif !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.8);
        padding: 12px !important;
        margin-bottom: 15px !important;
    }}
    
    .stAlert p {{
        color: #ffffff !important;
        font-size: 0.95rem !important;
        margin-bottom: 0 !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.9);
    }}
    
    /* Caption - Bright Cyan */
    .stCaption {{
        color: #22d3ee !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        margin-bottom: 10px !important;
        text-shadow: 
            0 0 10px rgba(0,0,0,1),
            0 0 10px rgba(34, 211, 238, 0.5);
    }}
    
    /* Divider */
    hr {{
        border-color: rgba(251, 191, 36, 0.3) !important;
        margin: 20px 0 !important;
    }}

    /* Tech Container - Dark with Orange Border */
    .tech-container {{
        background: rgba(10, 10, 15, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(251, 191, 36, 0.4);
        border-radius: 10px;
        padding: 20px !important;
        margin: 10px 0 !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.8),
            0 0 15px rgba(251, 191, 36, 0.1);
        position: relative;
        overflow: hidden;
    }}
    
    .tech-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #f97316, #fbbf24, #22d3ee);
    }}
    
    /* Strong text - Cyan */
    strong, b {{
        color: #22d3ee !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
    }}
    
    /* Reduce default Streamlit spacing */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }}
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
    st.title("🛡️ CYBER THREAT INTELLIGENCE")
    st.caption(f"SYS.TIME: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d/%m/%Y | %H:%M:%S')} EAT | STATUS: ONLINE | OPERATOR: Stephen Musau Makau")
    
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("CORE ALGORITHM", "XGBoost")
    with c2:
        st.metric("MODEL ACCURACY", f"{accuracy:.2f}%")
    with c3:
        st.metric("TARGET YEAR", "2027")

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
            <p>Maximum threat level detected. Emergency protocols activated.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="threat-moderate">
            <h1>✅ STABLE STATUS</h1>
            <h3>THREAT_LEVEL: MODERATE</h3>
            <p>Threat parameters within acceptable ranges. Standard monitoring sufficient.</p>
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
        st.write("Advanced predictive intelligence for Kenyan Government Digital Services.")
        st.subheader("⚠️ THREAT LANDSCAPE")
        st.write("Digital transformation correlates with exponential threat growth.")
    with col2:
        st.subheader("🔬 ARCHITECTURE")
        st.markdown("""
        - **Attack Vectors:** DDoS, Malware, Phishing
        - **Vulnerability Metrics:** CVE Criticality
        - **Network Intelligence:** Traffic Anomalies
        - **Economic Indicators:** Inflation/GDP correlation
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
        table_data.append({"Algorithm": name, "Accuracy": f"{value*100:.2f}%", "Status": "ACTIVE" if name == "XGBoost" else "STANDBY"})
    st.table(table_data)
    st.warning("⚠️ XGBoost selected for production deployment.")

# =====================================
# PARAMETERS
# =====================================
with parameters:
    st.title("⚙️ SYSTEM PARAMETERS")
    st.dataframe(get_parameters(), use_container_width=True, height=350)
    st.warning("⚠️ Economic volatility shows highest correlation with threat escalation.")
