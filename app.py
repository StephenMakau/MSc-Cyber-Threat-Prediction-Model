import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from cyber_threat_model import (
    predict_2027,
    get_model_accuracy,
    get_results,
    get_dataset,
    get_parameters
)

# =====================================
# SESSION STATE INITIALIZATION
# =====================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
    
if 'mobile_view' not in st.session_state:
    st.session_state.mobile_view = False

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="MKU Cyber Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# SIDEBAR CONTROLS
# =====================================
with st.sidebar:
    st.title("⚙️ SYSTEM CONTROLS")
    st.markdown("---")
    
    dark_mode = st.toggle(
        "🌙 Dark Mode / ☀️ Light Mode", 
        value=st.session_state.dark_mode,
        help="Switch between Dark and Light theme"
    )
    st.session_state.dark_mode = dark_mode
    
    mobile_view = st.toggle(
        "📱 Mobile View / 💻 Desktop View", 
        value=st.session_state.mobile_view,
        help="Switch between Mobile and Desktop layout"
    )
    st.session_state.mobile_view = mobile_view
    
    st.markdown("---")
    st.caption(f"System Time: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%H:%M:%S')}")
    st.caption("MKU Cybersecurity v2.0.7")

# =====================================
# THEME CSS
# =====================================
if st.session_state.dark_mode:
    theme_css = """
    <style>
        .stApp { background: linear-gradient(135deg, #0b1120 0%, #1e293b 50%, #0f172a 100%); color: #f8fafc; }
        h1, h2, h3, h4, h5, h6 { color: #f8fafc !important; text-shadow: 0 0 20px rgba(6, 182, 212, 0.3); }
        h1 { background: linear-gradient(90deg, #06b6d4, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; border-bottom: 2px solid rgba(6, 182, 212, 0.3); }
        h2 { color: #06b6d4 !important; border-left: 4px solid #06b6d4; }
        h3 { color: #8b5cf6 !important; }
        p, li, div, span, label, .stMarkdown, .stAlert { color: #e2e8f0 !important; }
        .stTabs [data-testid="stTab"] { color: #94a3b8; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(6, 182, 212, 0.2); }
        .stTabs [data-testid="stTab"]:hover { color: #06b6d4; background: rgba(6, 182, 212, 0.1); }
        .stTabs [data-testid="stTab"][aria-selected="true"] { background: linear-gradient(135deg, #06b6d4, #3b82f6); color: #ffffff !important; }
        [data-testid="stMetric"] { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(6, 182, 212, 0.3); }
        [data-testid="stMetricValue"] { color: #06b6d4 !important; }
        [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
        div[data-testid="stDataFrame"], div[data-testid="stTable"] { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(6, 182, 212, 0.2); }
        .threat-high { background: rgba(251, 188, 4, 0.1); border: 1px solid rgba(251, 188, 4, 0.5); color: #fcd34d !important; }
        .threat-critical { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.5); color: #fca5a5 !important; }
        .threat-moderate { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.5); color: #6ee7b7 !important; }
        .stAlert { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(6, 182, 212, 0.3); color: #06b6d4 !important; }
        .tech-container { background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(6, 182, 212, 0.2); }
        strong, b { color: #06b6d4 !important; }
    </style>
    """
else:
    theme_css = """
    <style>
        .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%); color: #1e293b; }
        h1, h2, h3, h4, h5, h6 { color: #1e293b !important; text-shadow: none; }
        h1 { background: linear-gradient(90deg, #0369a1, #7c3aed, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; border-bottom: 2px solid rgba(37, 99, 235, 0.3); }
        h2 { color: #0369a1 !important; border-left: 4px solid #0369a1; }
        h3 { color: #7c3aed !important; }
        p, li, div, span, label, .stMarkdown, .stAlert { color: #334155 !important; }
        .stTabs [data-testid="stTab"] { color: #64748b; background: rgba(255, 255, 255, 0.8); border: 1px solid rgba(37, 99, 235, 0.2); }
        .stTabs [data-testid="stTab"]:hover { color: #0369a1; background: rgba(37, 99, 235, 0.1); }
        .stTabs [data-testid="stTab"][aria-selected="true"] { background: linear-gradient(135deg, #0369a1, #2563eb); color: #ffffff !important; }
        [data-testid="stMetric"] { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(37, 99, 235, 0.3); box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        [data-testid="stMetricValue"] { color: #0369a1 !important; }
        [data-testid="stMetricLabel"] { color: #64748b !important; }
        div[data-testid="stDataFrame"], div[data-testid="stTable"] { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(37, 99, 235, 0.2); }
        .threat-high { background: rgba(251, 191, 36, 0.15); border: 1px solid rgba(251, 191, 36, 0.6); color: #92400e !important; }
        .threat-high h1 { -webkit-text-fill-color: #92400e; color: #92400e !important; }
        .threat-critical { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.6); color: #991b1b !important; }
        .threat-critical h1 { -webkit-text-fill-color: #991b1b; color: #991b1b !important; }
        .threat-moderate { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.6); color: #065f46 !important; }
        .threat-moderate h1 { -webkit-text-fill-color: #065f46; color: #065f46 !important; }
        .stAlert { background: rgba(219, 234, 254, 0.8); border: 1px solid rgba(37, 99, 235, 0.3); color: #1e40af !important; }
        .tech-container { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(37, 99, 235, 0.2); }
        strong, b { color: #0369a1 !important; }
        hr { border-color: rgba(37, 99, 235, 0.2) !important; }
    </style>
    """

if st.session_state.mobile_view:
    mobile_css = """
    <style>
        .block-container { max-width: 480px !important; padding-left: 1rem !important; padding-right: 1rem !important; }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.4rem !important; }
        h3 { font-size: 1.2rem !important; }
        .stTabs [data-testid="stTab"] { padding: 8px 12px !important; font-size: 0.8rem !important; }
        [data-testid="stMetric"] { padding: 15px !important; }
        [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    </style>
    """
else:
    mobile_css = """
    <style>
        .block-container { max-width: 95% !important; }
    </style>
    """

st.markdown(theme_css + mobile_css, unsafe_allow_html=True)

# =====================================
# DATA PREPARATION FOR THREAT GRAPH
# =====================================
def get_threat_data():
    """Prepare threat data for visualization"""
    data = {
        "Year": [2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2025],
        "Month": [3, 9, 2, 10, 3, 8, 2, 11, 5, 7],
        "Threat_Level": ["Medium", "Medium", "Medium", "High", "High", "High", "Critical", "High", "Medium", "Medium"],
        "DDoS_Attacks": [500, 700, 900, 1200, 1800, 2400, 3200, 2800, 2100, 1900],
        "Malware_Attacks": [4000, 5000, 6500, 7500, 9000, 12000, 15000, 13000, 11000, 9500],
        "Phishing_Attacks": [600, 800, 1000, 1300, 1700, 2200, 3000, 2600, 1800, 1500],
        "Web_Attacks": [1000, 1200, 1600, 2000, 2500, 3200, 4000, 3500, 3000, 2800]
    }
    df = pd.DataFrame(data)
    
    # Convert Threat_Level to numeric for plotting
    threat_mapping = {"Medium": 1, "High": 2, "Critical": 3}
    df["Threat_Numeric"] = df["Threat_Level"].map(threat_mapping)
    
    # Create date column for better x-axis
    df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(day=1))
    
    return df

# =====================================
# NAVIGATION
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
# HOME
# =====================================
with home:
    st.title("🛡️ CYBER THREAT INTELLIGENCE")
    st.subheader("SYSTEM v2.0.7 | Mount Kenya University")
    st.markdown("**Operator:** Stephen Musau Makau | **Clearance:** MSc Cybersecurity")
    
    mode_indicator = "🌙 DARK" if st.session_state.dark_mode else "☀️ LIGHT"
    view_indicator = "📱 MOBILE" if st.session_state.mobile_view else "💻 DESKTOP"
    st.caption(f"⏱️ SYS.TIME: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d/%m/%Y | %H:%M:%S')} EAT | STATUS: ONLINE | MODE: {mode_indicator} | VIEW: {view_indicator}")
    
    st.divider()

    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    st.markdown("### 📡 THREAT ASSESSMENT MODULE")
    
    if st.session_state.mobile_view:
        c1, c2 = st.columns(2)
        c3 = st.container()
    else:
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
        st.metric("🎯 MODEL ACCURACY", f"{accuracy:.2f}%", help="Training validation score")

    with c3:
        st.markdown("""
        <div class="tech-container" style="text-align: center;">
            <h4 style="color: #94a3b8; margin:15px 0 0 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; font-family: Inter, sans-serif;">Target Year</h4>
            <h2 style="margin: 20px 0; color: #8b5cf6; font-family: JetBrains Mono, monospace !important; font-size: 2.6rem; font-weight: 700; text-shadow: 0 0 15px rgba(139,92,246,0.5);">2027</h2>
            <p style="color: #64748b; font-size: 0.95rem; font-family: Calibri, sans-serif; margin-bottom: 15px;">Forecast.Horizon</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.header("🚨 THREAT PROJECTION // 2027")
    
    if prediction == "High":
        st.markdown("""
        <div class="threat-high">
            <h1>⚠️ HIGH RISK DETECTED</h1>
            <h3>THREAT_LEVEL: HIGH</h3>
            <p>Predictive algorithms indicate significant escalation in cyber threats targeting critical infrastructure. Immediate countermeasures required.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
        <div class="threat-critical">
            <h1>🛑 CRITICAL ALERT</h1>
            <h3>THREAT_LEVEL: CRITICAL</h3>
            <p>Maximum threat level detected. System predicts unprecedented attack surge. Emergency protocols activated.</p>
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
# PROJECT OVERVIEW WITH THREAT GRAPH
# =====================================
with overview:
    st.title("📄 SYSTEM OVERVIEW")
    
    # THREAT LANDSCAPE WITH GRAPH
    st.subheader("⚠️ THREAT LANDSCAPE")
    st.write("Historical threat evolution analysis showing escalation patterns from 2020-2025.")
    
    # Get data and create plot
    threat_df = get_threat_data()
    
    # Create the plot based on theme
    if st.session_state.dark_mode:
        plot_bg = "rgba(30, 41, 59, 0.7)"
        paper_bg = "rgba(15, 23, 42, 0.8)"
        font_color = "#e2e8f0"
        grid_color = "rgba(148, 163, 184, 0.2)"
        line_colors = ["#06b6d4", "#f97316", "#8b5cf6", "#10b981"]
    else:
        plot_bg = "rgba(255, 255, 255, 0.9)"
        paper_bg = "rgba(241, 245, 249, 0.9)"
        font_color = "#334155"
        grid_color = "rgba(100, 116, 139, 0.2)"
        line_colors = ["#0369a1", "#ea580c", "#7c3aed", "#059669"]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add Threat Level as stepped line
    fig.add_trace(
        go.Scatter(
            x=threat_df["Date"],
            y=threat_df["Threat_Numeric"],
            name="Threat Level",
            line=dict(color="#ef4444" if st.session_state.dark_mode else "#dc2626", width=4),
            mode="lines+markers",
            marker=dict(size=10, symbol="diamond"),
            text=threat_df["Threat_Level"],
            hovertemplate="%{x}<br>Threat: %{text}<extra></extra>"
        ),
        secondary_y=False
    )
    
    # Add attack vectors
    fig.add_trace(
        go.Scatter(
            x=threat_df["Date"],
            y=threat_df["DDoS_Attacks"],
            name="DDoS Attacks",
            line=dict(color=line_colors[0], width=2),
            mode="lines"
        ),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
            x=threat_df["Date"],
            y=threat_df["Malware_Attacks"],
            name="Malware Attacks",
            line=dict(color=line_colors[1], width=2),
            mode="lines"
        ),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
            x=threat_df["Date"],
            y=threat_df["Phishing_Attacks"],
            name="Phishing Attacks",
            line=dict(color=line_colors[2], width=2),
            mode="lines"
        ),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
            x=threat_df["Date"],
            y=threat_df["Web_Attacks"],
            name="Web Attacks",
            line=dict(color=line_colors[3], width=2),
            mode="lines"
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="CYBER THREAT EVOLUTION CURVE (2020-2025)",
            font=dict(size=16, color=font_color, family="Inter, sans-serif"),
            x=0.5
        ),
        plot_bgcolor=plot_bg,
        paper_bgcolor=paper_bg,
        font=dict(color=font_color, family="Calibri, sans-serif"),
        legend=dict(
            bgcolor="rgba(0,0,0,0.3)" if st.session_state.dark_mode else "rgba(255,255,255,0.7)",
            bordercolor="rgba(6, 182, 212, 0.3)" if st.session_state.dark_mode else "rgba(37, 99, 235, 0.3)",
            borderwidth=1,
            font=dict(color=font_color)
        ),
        hovermode="x unified",
        height=500 if not st.session_state.mobile_view else 400,
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
    fig.update_xaxes(
        title_text="Timeline",
        gridcolor=grid_color,
        zerolinecolor=grid_color,
        tickfont=dict(color=font_color),
        title_font=dict(color=font_color)
    )
    
    fig.update_yaxes(
        title_text="Threat Level (1=Medium, 2=High, 3=Critical)",
        secondary_y=False,
        gridcolor=grid_color,
        tickfont=dict(color=font_color),
        title_font=dict(color=font_color),
        tickvals=[1, 2, 3],
        ticktext=["Medium", "High", "Critical"]
    )
    
    fig.update_yaxes(
        title_text="Attack Volume (Count)",
        secondary_y=True,
        tickfont=dict(color=font_color),
        title_font=dict(color=font_color)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("Digital transformation acceleration correlates with exponential threat growth. Conventional reactive defenses inadequate against modern attack vectors.")
    
    # Rest of the overview content
    if st.session_state.mobile_view:
        st.subheader("🎯 MISSION OBJECTIVE")
        st.write("Advanced predictive intelligence platform for Kenyan Government Digital Services.")
        st.subheader("🔬 SYSTEM ARCHITECTURE")
        st.markdown("""
        - **Attack Vectors:** DDoS, Malware, Phishing
        - **Vulnerability Metrics:** CVE Criticality
        - **Network Intelligence:** Traffic Anomalies
        - **Economic Indicators:** Inflation/GDP correlation
        """)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 MISSION OBJECTIVE")
            st.write("Advanced predictive intelligence platform for Kenyan Government Digital Services. Deploys machine learning algorithms to forecast cyber threat evolution.")
            st.subheader("⚠️ KEY INSIGHTS")
            st.markdown("""
            - **2023 Peak:** Critical threat level reached
            - **Attack Surge:** 300% increase in DDoS attacks
            - **Malware Growth:** Exponential trajectory from 2020-2023
            """)
        with col2:
            st.subheader("🔬 SYSTEM ARCHITECTURE")
            st.markdown("""
            - **🎯 Attack Vectors:** DDoS, Malware, Phishing, Web Exploits
            - **🔒 Vulnerability Metrics:** CVE Criticality, Patch Latency
            - **📡 Network Intelligence:** Traffic Anomaly Detection
            - **📈 Economic Indicators:** Inflation/GDP correlation
            """)
            st.subheader("🌍 OPERATIONAL IMPACT")
            st.markdown("""
            - **🏛️ Critical Infrastructure Protection**
            - **💰 Resource Optimization**
            - **📋 Policy Intelligence**
            """)

    st.info("🔒 **SECURITY PROTOCOL:** All data synthetic/anonymized. No live government feeds.")

# =====================================
# DATASET
# =====================================
with dataset:
    st.title("📊 DATA MATRIX")
    st.markdown("Accessing classified training datasets...")
    
    height = 400 if st.session_state.mobile_view else 600
    st.dataframe(get_dataset(), use_container_width=True, height=height)

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
    st.markdown("Feature configuration for 2027 threat projection horizon.")
    
    height = 300 if st.session_state.mobile_view else 400
    st.dataframe(get_parameters(), use_container_width=True, height=height)
    st.warning("⚠️ **ANALYSIS:** Economic volatility and patch latency show highest correlation with threat escalation.")
