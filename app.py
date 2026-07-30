import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# HOME - PRIORITY: OUTCOME FIRST
# =====================================
with home:
    st.title("🛡️ CYBER THREAT INTELLIGENCE")
    st.subheader("SYSTEM v2.0.7 | Mount Kenya University")
    st.markdown("**Operator:** Stephen Musau Makau | **Clearance:** MSc Cybersecurity")
    
    mode_indicator = "🌙 DARK" if st.session_state.dark_mode else "☀️ LIGHT"
    view_indicator = "📱 MOBILE" if st.session_state.mobile_view else "💻 DESKTOP"
    st.caption(f"⏱️ SYS.TIME: {datetime.now(ZoneInfo('Africa/Nairobi')).strftime('%d/%m/%Y | %H:%M:%S')} EAT | STATUS: ONLINE | MODE: {mode_indicator} | VIEW: {view_indicator}")
    
    st.divider()

    # 1. EXECUTION: Get Prediction & Accuracy Immediately
    try:
        prediction = predict_2027()
        accuracy = get_model_accuracy() * 100
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        prediction = "Unknown"
        accuracy = 0.0

    # 2. OUTCOME: Display Pulsing Threat Projection FIRST (Top Priority)
    st.header("🚨 THREAT PROJECTION // 2027")
    
    # Define styles based on prediction
    if prediction == "High":
        color_hex = "#fbbf24"
        color_rgb = "251, 188, 4"
        bg_color = "rgba(251, 188, 4, 0.15)"
        border_color = "rgba(251, 188, 4, 1)"
        text_color = "#fbbf24" if st.session_state.dark_mode else "#92400e"
        animation_name = "pulse-orange"
        title = "⚠️ HIGH RISK DETECTED"
        subtitle = "THREAT_LEVEL: HIGH"
        message = "Predictive algorithms indicate significant escalation in cyber threats. Immediate countermeasures required."
    elif prediction == "Critical":
        color_hex = "#ef4444"
        color_rgb = "239, 68, 68"
        bg_color = "rgba(239, 68, 68, 0.15)"
        border_color = "rgba(239, 68, 68, 1)"
        text_color = "#fca5a5" if st.session_state.dark_mode else "#991b1b"
        animation_name = "pulse-red"
        title = "🛑 CRITICAL ALERT"
        subtitle = "THREAT_LEVEL: CRITICAL"
        message = "Maximum threat level detected. System predicts unprecedented attack surge. Emergency protocols activated."
    else:
        color_hex = "#10b981"
        color_rgb = "16, 185, 129"
        bg_color = "rgba(16, 185, 129, 0.15)"
        border_color = "rgba(16, 185, 129, 1)"
        text_color = "#6ee7b7" if st.session_state.dark_mode else "#065f46"
        animation_name = "pulse-green"
        title = "✅ STABLE STATUS"
        subtitle = "THREAT_LEVEL: MODERATE"
        message = "Threat parameters within acceptable ranges. Standard monitoring protocols sufficient."

    # Render Pulsing Alert
    st.markdown(f"""
    <div class="pulse-container">
        <div class="pulse-box" style="
            background: {bg_color};
            border: 2px solid {border_color};
            color: {text_color};
            animation-name: {animation_name};
        ">
            <h1 style="color: {text_color} !important; -webkit-text-fill-color: {text_color}; margin: 0; font-size: 2.5rem;">{title}</h1>
            <h3 style="color: {text_color} !important; -webkit-text-fill-color: {text_color}; margin: 10px 0; font-size: 1.5rem;">{subtitle}</h3>
            <p style="color: {text_color} !important; -webkit-text-fill-color: {text_color}; font-size: 1.1rem;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add interpretation warning/success based on prediction
    if prediction == "High":
        st.warning("⚠️ **Interpretation**: Historical data shows that when attack volumes exceed 4,000 (DDoS), 18,000 (Malware), and economic pressure indicators are elevated, threat levels typically spike to HIGH. Review defensive protocols immediately.")
    elif prediction == "Critical":
        st.error("🛑 **Interpretation**: The convergence of high CVE counts (95), low patch compliance (9 days delay), and economic instability historically correlates with CRITICAL threat periods. Immediate executive action required.")
    else:
        st.success("✅ **Interpretation**: Current projections indicate manageable threat levels. Attack volumes remain within historical norms and economic indicators suggest stable conditions. Maintain standard operations.")

    # 3. GRAPH: Threat Trend Projection (Historical + Future)
    st.divider()
    st.header("📈 TH TREND ANALYSIS & PROJECTION")
    
    # Get historical data
    historical_df = get_historical_data()
    
    # Create a mapping for threat levels to numeric values for plotting
    threat_mapping = {'Medium': 1, 'High': 2, 'Critical': 3}
    reverse_threat_mapping = {1: 'Medium', 2: 'High', 3: 'Critical'}
    
    # Convert historical threat levels to numeric
    historical_df['Threat_Level_Num'] = historical_df['Threat_Level'].map(threat_mapping)
    
    # Create future projection point
    future_point = get_future_projection_point()
    future_threat_level = predict_2027()
    future_threat_num = threat_mapping.get(future_threat_level, 1)
    
    # Create a dataframe for the full timeline including projection
    full_timeline = pd.DataFrame({
        'Year': list(historical_df['Year']) + [2027],
        'Threat_Level_Num': list(historical_df['Threat_Level_Num']) + [future_threat_num],
        'Type': ['Historical'] * len(historical_df) + ['Projection']
    })
    
    # Create the plot
    fig = go.Figure()

    # Add historical data line
    fig.add_trace(go.Scatter(
        x=historical_df['Year'],
        y=historical_df['Threat_Level_Num'],
        mode='lines+markers',
        name='Historical Threat Level',
        line=dict(color='#06b6d4', width=3),
        marker=dict(size=8)
    ))

    # Add projection line (dashed)
    fig.add_trace(go.Scatter(
        x=[historical_df['Year'].max(), 2027],
        y=[historical_df['Threat_Level_Num'].iloc[-1], future_threat_num],
        mode='lines+markers',
        name='AI Projection (2027)',
        line=dict(color='#ef4444', width=3, dash='dot'),
        marker=dict(size=10, symbol='star')
    ))

    # Update layout
    fig.update_layout(
        title='Cyber Threat Level Trend (Historical vs Projected)',
        xaxis_title='Year',
        yaxis_title='Threat Level',
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3],
            ticktext=['Moderate', 'High', 'Critical']
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)' if st.session_state.dark_mode else 'rgba(255,255,255,0)',
        paper_bgcolor='rgba(0,0,0,0)' if st.session_state.dark_mode else 'rgba(255,255,255,0)',
        font=dict(color='#e2e8f0' if st.session_state.dark_mode else '#1e293b'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)' if st.session_state.dark_mode else 'rgba(255,255,255,0)',
            font=dict(color='#e2e8f0' if st.session_state.dark_mode else '#1e293b')
        )
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("📊 **Chart Explanation**: The solid blue line represents actual historical threat levels observed from 2020-2025. The dotted red line represents the AI-projected trajectory based on current parameters. The star marker indicates the predicted threat level for 2027.")

    st.divider()

    # 4. CONTEXT: System Metrics & Algorithm Info (Secondary Priority)
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
        st.caption("💡 **XGBoost** (eXtreme Gradient Boosting) is an advanced ML algorithm that combines multiple decision trees to make predictions. It was selected for its superior accuracy in handling cybersecurity data.")

    with c2:
        st.metric(
            "🎯 MODEL ACCURACY",
            f"{accuracy:.2f}%",
            help="Training validation score"
        )
        st.caption("💡 This percentage indicates how often the model correctly
