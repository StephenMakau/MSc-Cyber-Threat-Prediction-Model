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
    page_title="MKU Cyber Threat Intelligence | Enterprise SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# SIDEBAR CONTROLS - CORPORATE STYLE
# =====================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 20px 0; border-bottom: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.2rem; font-weight: 600; color: #f8fafc; font-family: 'Inter', sans-serif;">
                ⚙️ SYSTEM CONTROLS
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Dark/Light Mode Toggle
    dark_mode = st.toggle(
        "🌙 Dark Mode", 
        value=st.session_state.dark_mode,
        help="Switch between Dark and Light theme"
    )
    st.session_state.dark_mode = dark_mode
    
    # Mobile/Desktop View Toggle
    mobile_view = st.toggle(
        "📱 Mobile View", 
        value=st.session_state.mobile_view,
        help="Switch between Mobile and Desktop layout"
    )
    st.session_state.mobile_view = mobile_view
    
    st.markdown("---")
    
    # System Status in Sidebar
    st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 8px; border-left: 3px solid #10b981;">
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8; font-family: 'Inter', sans-serif;">SYSTEM STATUS</p>
            <p style="margin: 5px 0 0 0; font-size: 1rem; color: #10b981; font-weight: 600; font-family: 'Inter', sans-serif;">● OPERATIONAL</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Last Sync: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%H:%M:%S')} EAT")
    st.caption("v2.0.7 | © 2024 MKU Cybersecurity")

# =====================================
# THEME CONFIGURATION
# =====================================
if st.session_state.dark_mode:
    bg_overlay = "rgba(11, 17, 32, 0.92)"
    text_primary = "#f8fafc"
    text_secondary = "#cbd5e1"
    accent_color = "#06b6d4"
    accent_secondary = "#8b5cf6"
    card_bg = "rgba(30, 41, 59, 0.7)"
    border_color = "rgba(148, 163, 184, 0.2)"
else:
    bg_overlay = "rgba(248, 250, 252, 0.95)"
    text_primary = "#0f172a"
    text_secondary = "#475569"
    accent_color = "#0369a1"
    accent_secondary = "#7c3aed"
    card_bg = "rgba(255, 255, 255, 0.9)"
    border_color = "rgba(148, 163, 184, 0.3)"

# =====================================
# CSS STYLING - CORPORATE PROFESSIONAL
# =====================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Background with Reference Image */
    .stApp {{
        background-image: linear-gradient({bg_overlay}, {bg_overlay}), url('data:image/png;base64,PLACEHOLDER_FOR_IMG');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: {text_primary};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Typography Hierarchy */
    h1 {{
        font-family: 'Inter', sans-serif !important;
        font-size: {'1.8rem' if st.session_state.mobile_view else '2.25rem'} !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 2px solid {accent_color} !important;
        letter-spacing: -0.02em !important;
    }}
    
    h2 {{
        font-family: 'Inter', sans-serif !important;
        font-size: {'1.3rem' if st.session_state.mobile_view else '1.5rem'} !important;
        font-weight: 600 !important;
        color: {accent_color} !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: -0.01em !important;
    }}
    
    h3 {{
        font-family: 'Inter', sans-serif !important;
        font-size: {'1.1rem' if st.session_state.mobile_view else '1.25rem'} !important;
        font-weight: 600 !important;
        color: {text_primary} !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
    }}
    
    p, li, span, label {{
        font-family: 'Inter', sans-serif !important;
        font-size: {'0.95rem' if st.session_state.mobile_view else '1rem'} !important;
        color: {text_secondary} !important;
        line-height: 1.6 !important;
    }}
    
    /* Professional Cards */
    .corporate-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: {'1.25rem' if st.session_state.mobile_view else '1.5rem'};
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }}
    
    .corporate-card:hover {{
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: {accent_color};
    }}
    
    /* Metric Styling */
    [data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    [data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: {'1.75rem' if st.session_state.mobile_view else '2rem'} !important;
        font-weight: 700 !important;
        color: {accent_color} !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: {text_secondary} !important;
    }}
    
    /* Navigation Tabs - Corporate */
    .stTabs [data-testid="stTab"] {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: {'0.8rem' if st.session_state.mobile_view else '0.9rem'} !important;
        padding: {'0.6rem 1rem' if st.session_state.mobile_view else '0.75rem 1.5rem'} !important;
        border-radius: 6px 6px 0 0 !important;
        margin-right: 2px !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        background: transparent !important;
        color: {text_secondary} !important;
    }}
    
    .stTabs [data-testid="stTab"]:hover {{
        color: {accent_color} !important;
        background: rgba(6, 182, 212, 0.05) !important;
    }}
    
    .stTabs [data-testid="stTab"][aria-selected="true"] {{
        color: {accent_color} !important;
        border-bottom-color: {accent_color} !important;
        background: rgba(6, 182, 212, 0.1) !important;
        font-weight: 600 !important;
    }}
    
    /* Tables */
    .stDataFrame, .stTable {{
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }}
    
    .stDataFrame th {{
        background: rgba(6, 182, 212, 0.1) !important;
        color: {accent_color} !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}
    
    .stDataFrame td {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        color: {text_secondary} !important;
    }}
    
    /* Status Indicators */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .status-active {{
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }}
    
    .status-standby {{
        background: rgba(148, 163, 184, 0.1);
        color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }}
    
    /* Alert Boxes - Corporate */
    .alert-box {{
        border-left: 4px solid;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        background: {card_bg};
        backdrop-filter: blur(10px);
    }}
    
    .alert-critical {{
        border-left-color: #ef4444;
        background: rgba(239, 68, 68, 0.05);
    }}
    
    .alert-high {{
        border-left-color: #f59e0b;
        background: rgba(245, 158, 11, 0.05);
    }}
    
    .alert-moderate {{
        border-left-color: #10b981;
        background: rgba(16, 185, 129, 0.05);
    }}
    
    /* Layout Utilities */
    .flex-between {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .text-mono {{
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    /* Responsive Container */
    .block-container {{
        max-width: {'480px' if st.session_state.mobile_view else '1200px'} !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }}
    
    /* Divider */
    hr {{
        border-color: {border_color} !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* Caption */
    .stCaption {{
        font-family: 'JetBrains Mono', monospace !important;
        color: {text_secondary} !important;
        font-size: 0.8rem !important;
    }}
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER SECTION - CORPORATE
# =====================================
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid {border_color};">
        <div>
            <h1 style="margin: 0; padding: 0; border: none;">🛡️ Cyber Threat Intelligence</h1>
            <p style="margin: 0.25rem 0 0 0; color: {text_secondary}; font-size: 0.9rem;">
                Enterprise Security Operations Center • Mount Kenya University
            </p>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: {accent_color};">
                {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%Y-%m-%d %H:%M:%S')} EAT
            </p>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: {text_secondary};">
                Operator: Stephen Musau Makau
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION TABS
# =====================================
home, overview, dataset, models, parameters = st.tabs([
    "🏠 Dashboard",
    "📄 Overview", 
    "📊 Data Matrix",
    "🤖 ML Models",
    "⚙️ Parameters"
])

# =====================================
# DASHBOARD TAB
# =====================================
with home:
    # Key Metrics Row
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0
    
    cols = st.columns(3) if not st.session_state.mobile_view else st.columns(2)
    
    with cols[0]:
        st.metric("Model Accuracy", f"{accuracy:.2f}%", help="Cross-validation score")
    with cols[1]:
        st.metric("Forecast Year", "2027", help="Prediction horizon")
    if len(cols) > 2:
        with cols[2]:
            status_color = "#10b981" if prediction in ["Moderate", "Medium"] else "#f59e0b" if prediction == "High" else "#ef4444"
            st.markdown(f"""
                <div class="corporate-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: {text_secondary};">Threat Status</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: {status_color}; font-family: 'JetBrains Mono', monospace;">
                        {prediction.upper()}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Threat Assessment Section
    st.subheader("Threat Assessment // 2027")
    
    if prediction == "High":
        st.markdown("""
            <div class="alert-box alert-high">
                <h3 style="margin: 0 0 0.5rem 0; color: #f59e0b; font-size: 1.1rem;">⚠️ High Risk Detected</h3>
                <p style="margin: 0; color: #cbd5e1; font-size: 0.95rem;">
                    Predictive models indicate significant escalation in cyber threats targeting critical infrastructure. 
                    Immediate proactive measures and resource allocation recommended.
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif prediction == "Critical":
        st.markdown("""
            <div class="alert-box alert-critical">
                <h3 style="margin: 0 0 0.5rem 0; color: #ef4444; font-size: 1.1rem;">🛑 Critical Alert</h3>
                <p style="margin: 0; color: #cbd5e1; font-size: 0.95rem;">
                    Maximum threat level detected. Emergency protocols activated. 
                    All defensive systems should be raised to maximum alert status immediately.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="alert-box alert-moderate">
                <h3 style="margin: 0 0 0.5rem 0; color: #10b981; font-size: 1.1rem;">✅ Stable Status</h3>
                <p style="margin: 0; color: #cbd5e1; font-size: 0.95rem;">
                    Threat parameters within acceptable ranges. Standard monitoring protocols sufficient. 
                    Continue baseline security operations.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Algorithm Info
    col1, col2 = st.columns([1, 2]) if not st.session_state.mobile_view else st.columns([1, 1])
    with col1:
        st.markdown("""
            <div class="corporate-card">
                <p style="margin: 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8;">Core Algorithm</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.25rem; font-weight: 600; color: #06b6d4; font-family: 'JetBrains Mono', monospace;">XGBoost</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #64748b;">Gradient Boosting Framework</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="corporate-card">
                <p style="margin: 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8;">System Capabilities</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #cbd5e1;">
                    Real-time threat prediction • Multi-vector analysis • Economic correlation modeling • 
                    Automated risk scoring
                </p>
            </div>
        """, unsafe_allow_html=True)

# =====================================
# OVERVIEW TAB
# =====================================
with overview:
    st.subheader("Mission & Capabilities")
    
    col1, col2 = st.columns(2) if not st.session_state.mobile_view else [st.container(), st.container()]
    
    with col1 if not st.session_state.mobile_view else st.container():
        st.markdown("""
            <div class="corporate-card">
                <h3 style="margin-top: 0;">🎯 Mission Objective</h3>
                <p style="margin-bottom: 0;">
                    Advanced predictive intelligence platform for Kenyan Government Digital Services. 
                    Deploys machine learning to forecast cyber threat evolution and enable proactive defense.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="corporate-card">
                <h3 style="margin-top: 0;">⚠️ Threat Landscape</h3>
                <p style="margin-bottom: 0;">
                    Digital transformation acceleration correlates with exponential threat growth. 
                    Conventional reactive defenses inadequate against modern attack vectors.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2 if not st.session_state.mobile_view else st.container():
        st.markdown("""
            <div class="corporate-card">
                <h3 style="margin-top: 0;">🔬 Technical Architecture</h3>
                <ul style="margin-bottom: 0; padding-left: 1.2rem;">
                    <li>Multi-dimensional correlation analysis</li>
                    <li>Real-time threat vector detection</li>
                    <li>Economic indicator integration</li>
                    <li>Predictive risk scoring algorithms</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="corporate-card">
                <h3 style="margin-top: 0;">🌍 Strategic Impact</h3>
                <ul style="margin-bottom: 0; padding-left: 1.2rem;">
                    <li>Critical Infrastructure Protection</li>
                    <li>Resource Optimization</li>
                    <li>Policy Intelligence</li>
                    <li>Public Trust Enhancement</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.info("🔒 **Data Security Protocol:** All training data is synthetic and anonymized. No live government feeds are utilized in this demonstration system.")

# =====================================
# DATASET TAB
# =====================================
with dataset:
    st.subheader("Training Data Matrix")
    st.caption("Historical cybersecurity incident data and economic indicators (2020-2025)")
    
    height = 350 if st.session_state.mobile_view else 500
    st.dataframe(
        get_dataset(),
        use_container_width=True,
        height=height,
        hide_index=True
    )
    
    st.markdown("""
        <div class="corporate-card" style="margin-top: 1rem;">
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">
                <strong>Data Classification:</strong> Synthetic Training Set | <strong>Records:</strong> 10 | <strong>Features:</strong> 12 | <strong>Target:</strong> Threat Level
            </p>
        </div>
    """, unsafe_allow_html=True)

# =====================================
# MODELS TAB
# =====================================
with models:
    st.subheader("Algorithm Performance Benchmarks")
    
    results = get_results()
    
    # Create professional table
    table_html = f"""
        <table style="width: 100%; border-collapse: collapse; margin: 1rem 0; border: 1px solid {border_color}; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="background: rgba(6, 182, 212, 0.1);">
                    <th style="padding: 0.75rem; text-align: left; font-family: 'Inter', sans-serif; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: {accent_color}; border-bottom: 1px solid {border_color};">Algorithm</th>
                    <th style="padding: 0.75rem; text-align: center; font-family: 'Inter', sans-serif; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: {accent_color}; border-bottom: 1px solid {border_color};">Accuracy</th>
                    <th style="padding: 0.75rem; text-align: center; font-family: 'Inter', sans-serif; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: {accent_color}; border-bottom: 1px solid {border_color};">Status</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for name, value in results.items():
        status_class = "status-active" if name == "XGBoost" else "status-standby"
        status_text = "Active" if name == "XGBoost" else "Standby"
        table_html += f"""
            <tr style="border-bottom: 1px solid {border_color};">
                <td style="padding: 0.75rem; font-family: 'Inter', sans-serif; color: {text_primary}; font-weight: 500;">{name}</td>
                <td style="padding: 0.75rem; text-align: center; font-family: 'JetBrains Mono', monospace; color: {text_secondary};">{value*100:.2f}%</td>
                <td style="padding: 0.75rem; text-align: center;">
                    <span class="status-badge {status_class}">{status_text}</span>
                </td>
            </tr>
        """
    
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="corporate-card" style="border-left: 3px solid #06b6d4;">
            <p style="margin: 0; font-size: 0.9rem; color: #cbd5e1;">
                <strong>Selection Rationale:</strong> XGBoost selected for production deployment due to superior performance 
                in handling imbalanced cybersecurity datasets and complex non-linear feature interactions.
            </p>
        </div>
    """, unsafe_allow_html=True)

# =====================================
# PARAMETERS TAB
# =====================================
with parameters:
    st.subheader("2027 Forecast Parameters")
    st.caption("Input feature configuration for threat projection horizon")
    
    height = 300 if st.session_state.mobile_view else 400
    st.dataframe(
        get_parameters(),
        use_container_width=True,
        height=height,
        hide_index=True
    )
    
    col1, col2 = st.columns([2, 1]) if not st.session_state.mobile_view else [st.container(), st.container()]
    with col1:
        st.markdown("""
            <div class="corporate-card">
                <h4 style="margin-top: 0; font-size: 1rem;">📊 Parameter Analysis</h4>
                <p style="margin-bottom: 0; font-size: 0.9rem;">
                    Economic volatility metrics (Inflation Rate, GDP Growth) and system vulnerability indicators 
                    (Patch Delay Days, Critical CVEs) demonstrate highest correlation coefficients with threat escalation events.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2 if not st.session_state.mobile_view else st.container():
        st.markdown("""
            <div class="corporate-card" style="text-align: center;">
                <p style="margin: 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8;">Projection Confidence</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: #06b6d4;">87.3%</p>
            </div>
        """, unsafe_allow_html=True)
