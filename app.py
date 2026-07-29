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

st.set_page_config(
    page_title="Cyber Threat Prediction System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# RESPONSIVE CSS
# =====================================================

st.markdown("""
<style>

/* MAIN */
.stApp{
    background:#eef7ff;
}

/* Hide Streamlit menu/footer */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Center content */
.block-container{
    max-width:1400px;
    padding-top:1rem;
    padding-bottom:2rem;
}

/* Responsive titles */

h1{
    color:#003366;
    font-weight:800;
    font-size:clamp(1.8rem,4vw,3rem);
}

h2{
    color:#003366;
    font-size:clamp(1.3rem,3vw,2rem);
}

h3{
    color:#003366;
}

/* Metric Cards */

[data-testid="stMetric"]{

    background:white;

    border-radius:18px;

    border:2px solid #b8d9f5;

    padding:18px;

    box-shadow:0 4px 10px rgba(0,0,0,.08);

}

[data-testid="stMetricValue"]{

    color:#d35400 !important;

    font-weight:900;

}

/* Forecast Card */

.forecast-card{

    background:#F57C00;

    color:white;

    padding:35px;

    border-radius:20px;

    text-align:center;

    box-shadow:0 8px 20px rgba(0,0,0,.15);

}

.forecast-title{

    font-size:clamp(2rem,5vw,3rem);

    font-weight:900;

}

.forecast-sub{

    font-size:clamp(1rem,2vw,1.5rem);

}

/* Tables */

thead tr th{

    background:#003366 !important;

    color:white !important;

}

/* Mobile */

@media (max-width:768px){

.block-container{

padding-left:1rem;

padding-right:1rem;

}

[data-testid="stMetric"]{

padding:12px;

}

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================

home, dataset, models, parameters = st.tabs(
    [
        "🏠 HOME",
        "📊 DATASET",
        "🤖 MODELS",
        "⚙ PARAMETERS"
    ]
)

# =====================================================
# HOME
# =====================================================

with home:

    st.title("MSc Cybersecurity Project")
    st.subheader("Mount Kenya University")

    st.write(
        "Machine Learning-Based Cyber Threat Trend Prediction "
        "for Kenyan Government Digital Services"
    )

    st.write("**Author:** Stephen Musau Makau")

    st.caption(
        datetime.now(
            ZoneInfo("Africa/Nairobi")
        ).strftime("%d %B %Y | %H:%M:%S EAT")
    )

    st.divider()

    prediction = predict_2027()
    accuracy = get_model_accuracy() * 100

    # Responsive metrics
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        st.metric(
            "Algorithm",
            "XGBoost"
        )

    with col2:
        st.metric(
            "Accuracy",
            f"{accuracy:.2f}%"
        )

    with col3:
        st.metric(
            "Forecast Year",
            "2027"
        )

    st.divider()

    st.header("2027 Cyber Threat Forecast")

    if prediction == "High":

        st.markdown(f"""

        <div class="forecast-card">

        <div class="forecast-title">
        HIGH RISK
        </div>

        <div class="forecast-sub">
        Predicted Threat Level: <b>{prediction}</b>
        </div>

        </div>

        """, unsafe_allow_html=True)

    elif prediction == "Critical":

        st.error("🚨 CRITICAL RISK")

    else:

        st.success("✅ MODERATE RISK")

# =====================================================
# DATASET
# =====================================================

with dataset:

    st.title("Cyber Threat Dataset")

    st.dataframe(
        get_dataset(),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# MODELS
# =====================================================

with models:

    st.title("Machine Learning Algorithms")

    results = get_results()

    table = []

    for algorithm, score in results.items():

        table.append({

            "Algorithm": algorithm,

            "Accuracy": f"{score*100:.2f}%"

        })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# PARAMETERS
# =====================================================

with parameters:

    st.title("Prediction Parameters Evaluated")

    st.write(
        """
        The following cybersecurity,
        technological, and economic
        variables contribute to the
        final prediction for 2027.
        """
    )

    st.dataframe(
        get_parameters(),
        use_container_width=True,
        hide_index=True
    )
