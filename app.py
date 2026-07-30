import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import plotly.graph_objects as go
import pandas as pd

# Import from the model file
from cyber_threat_model import (
    predict_2027,
    get_model_accuracy,
    get_results,
    get_dataset,
    get_parameters,
    get_historical_data,
    get_future_projection_point
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
        .stAlert { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(6, 182, 212, 0.3); color: #06b6d4 !important; }
        .tech-container { background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(6, 182, 212, 0.2); }
        strong, b { color: #06b6d4 !important; }
        .explanation-box { background: rgba(6, 182, 212, 0.1); border-left: 3px solid #06b6d4; padding: 15px; border-radius: 5px; margin: 10px 0; }
        
        /* Pulsing Alert Styles */
        .pulse-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            margin: 20px 0;
        }
        .pulse-box {
            position: relative;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.7);
            animation: pulse-red 2s infinite;
            max-width: 800px;
            margin: 0 auto;
            border: 2px solid;
        }
        @keyframes pulse-red {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(239, 68, 68, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
            }
        }
        @keyframes pulse-orange {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(251, 188, 4, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(251, 188, 4, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(251, 188, 4, 0);
            }
        }
        @keyframes pulse-green {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(16, 185, 129, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }
        }
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
        .stAlert { background: rgba(219, 234, 254, 0.8); border: 1px solid rgba(37, 99, 235, 0.3); color: #1e40af !important; }
        .tech-container { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(37, 99, 235, 0.2); }
        strong, b { color: #0369a1 !important; }
        hr { border-color: rgba(37, 99, 235, 0.2) !important; }
        .explanation-box { background: rgba(37, 99, 235, 0.1); border-left: 3px solid #0369a1; padding: 15px; border-radius: 5px; margin: 10px 0; }

        /* Pulsing Alert Styles - Light Mode */
        .pulse-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            margin: 20px 0;
        }
        .pulse-box {
            position: relative;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.1);
            animation: pulse-red 2s infinite;
            max-width: 800px;
            margin: 0 auto;
            border: 2px solid;
            color: #000;
        }
        @keyframes pulse-red {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(220, 38, 38, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(220, 38, 38, 0);
            }
        }
        @keyframes pulse-orange {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(217, 119, 6, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(217, 119, 6, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(217, 119, 6, 0);
            }
        }
        @keyframes pulse-green {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 20px rgba(22, 163, 74, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(22, 163, 74, 0);
            }
        }
    </style>
    """

if st.session_state.mobile_view:
    mobile_css = """
    <style>
        .block-container { max-width: 480px !important; padding-left: 1rem !important; padding-right: 1rem !important; }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.4rem !important; }
        h3 { font-size: 1.2rem !important; }
        .stTabs [data-testid="stTab"] { padding: 8px 12px !important; font-size: 0.8rem !
