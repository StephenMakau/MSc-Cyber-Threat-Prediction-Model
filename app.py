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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# SESSION MODE
# =====================================================

if "theme" not in st.session_state:
    st.session_state.theme = "Light"


# =====================================================
# STYLE
# =====================================================

if st.session_state.theme == "Light":

    background = "#D9F3F0"
    text_color = "#003366"
    card_background = "#FFFFFF"
    border_color = "#9AD9D5"

else:

    background = "#0B1628"
    text_color = "#FFFFFF"
    card_background = "#172A46"
    border_color = "#355C8A"



st.markdown(f"""

<style>

.stApp {{

background:{background};

}}


.block-container {{

max-width:1400px;

padding-top:1rem;

}}



h1,h2,h3 {{

color:{text_color};

font-weight:800;

}}



p,label {{

color:{text_color};

}}



[data-testid="stMetric"] {{

background:{card_background};

padding:18px;

border-radius:15px;

border:2px solid {border_color};

box-shadow:0 5px 15px rgba(0,0,0,0.1);

}}



[data-testid="stMetricLabel"] {{

color:{text_color} !important;

font-weight:bold;

}}



[data-testid="stMetricValue"] {{

color:#D35400 !important;

font-weight:900;

}}



button[data-baseweb="tab"] {{

color:{text_color};

font-weight:bold;

}}



button[data-baseweb="tab"][aria-selected="true"] {{

background:#7ACFC7;

border-radius:8px;

}}



.forecast-card {{

background:#008B8B;

padding:35px;

border-radius:20px;

text-align:center;

border:2px solid white;

}}



.forecast-title {{

font-size:clamp(2rem,5vw,3rem);

font-weight:900;

color:white;

}}



.forecast-sub {{

font-size:clamp(1rem,2vw,1.4rem);

color:white;

}}



thead tr th {{

background:#003366 !important;

color:white !important;

}}



tbody tr td {{

background:{card_background} !important;

color:{text_color} !important;

}}



@media(max-width:768px){{

.block-container{{

padding-left:1rem;

padding-right:1rem;

}}

}}


</style>

""",
unsafe_allow_html=True
)



# =====================================================
# TABS
# =====================================================

home, dataset, models, parameters, mode = st.tabs(
[
"HOME",
"DATASET",
"MODELS",
"PARAMETERS",
"MODE"
]
)



# =====================================================
# HOME
# =====================================================

with home:


    st.title(
        "MSc Cybersecurity Project"
    )


    st.subheader(
        "Mount Kenya University"
    )


    st.write(
        "Machine Learning-Based Cyber Threat Trend Prediction for Kenyan Government Digital Services"
    )


    st.write(
        "Author: Stephen Musau Makau"
    )


    st.caption(

        datetime.now(
            ZoneInfo("Africa/Nairobi")
        ).strftime(
            "%d %B %Y | %H:%M:%S EAT"
        )

    )


    st.divider()


    prediction = predict_2027()

    accuracy = get_model_accuracy()*100



    c1,c2,c3 = st.columns(3)


    with c1:

        st.metric(
            "Algorithm",
            "XGBoost"
        )


    with c2:

        st.metric(
            "Accuracy",
            f"{accuracy:.2f}%"
        )


    with c3:

        st.metric(
            "Forecast Year",
            "2027"
        )


    st.divider()


    st.header(
        "2027 Cyber Threat Forecast"
    )


    if prediction == "High":

        st.markdown(

        """

        <div class="forecast-card">

        <div class="forecast-title">

        HIGH RISK

        </div>


        <div class="forecast-sub">

        Predicted Threat Level: High

        </div>

        </div>

        """,

        unsafe_allow_html=True

        )


    elif prediction == "Critical":

        st.error(
            "CRITICAL RISK"
        )

    else:

        st.success(
            "MODERATE RISK"
        )





# =====================================================
# DATASET
# =====================================================

with dataset:


    st.title(
        "Cyber Threat Dataset"
    )


    st.dataframe(

        get_dataset(),

        use_container_width=True,

        hide_index=True

    )





# =====================================================
# MODELS
# =====================================================

with models:


    st.title(
        "Machine Learning Algorithms"
    )


    results=get_results()


    table=[]


    for name,value in results.items():

        table.append({

        "Algorithm":name,

        "Accuracy":f"{value*100:.2f}%"

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


    st.title(
        "Prediction Parameters Evaluated"
    )


    st.write(

    """
    The following cybersecurity,
    technological and economic variables
    contribute to the 2027 threat prediction.
    """

    )


    st.dataframe(

        get_parameters(),

        use_container_width=True,

        hide_index=True

    )





# =====================================================
# MODE SWITCH
# =====================================================

with mode:


    st.title(
        "Display Mode"
    )


    selected = st.radio(

        "Select interface theme",

        [
            "Light",
            "Dark"
        ],

        index=0 if st.session_state.theme=="Light" else 1

    )


    if selected != st.session_state.theme:

        st.session_state.theme = selected

        st.rerun()
