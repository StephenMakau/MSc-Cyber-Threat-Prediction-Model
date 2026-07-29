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


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Cyber Threat Prediction System",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# =====================================================
# THEME CONTROL
# =====================================================

if "theme" not in st.session_state:
    st.session_state.theme = "Light"



if st.session_state.theme == "Light":

    background = "#DDF6F3"
    text_color = "#003366"
    card_background = "#FFFFFF"
    border_color = "#8ED8D2"
    table_text = "#000000"

else:

    background = "#101820"
    text_color = "#FFFFFF"
    card_background = "#1C2B3A"
    border_color = "#456A89"
    table_text = "#FFFFFF"



# =====================================================
# CSS
# =====================================================

st.markdown(f"""

<style>


.stApp {{

background:{background};

}}



.block-container {{

max-width:1400px;

padding-top:1rem;

padding-bottom:2rem;

}}



h1,h2,h3 {{

color:{text_color};

font-weight:800;

}}



p,span,label {{

color:{text_color};

}}



[data-testid="stMetric"] {{

background:{card_background};

padding:18px;

border-radius:15px;

border:2px solid {border_color};

box-shadow:0px 5px 15px rgba(0,0,0,0.12);

}}



[data-testid="stMetricLabel"] {{

color:{text_color} !important;

font-weight:bold;

}}



[data-testid="stMetricValue"] {{

color:#C75B12 !important;

font-weight:900;

}}



button[data-baseweb="tab"] {{

font-size:15px;

font-weight:700;

color:{text_color};

}}



button[data-baseweb="tab"][aria-selected="true"] {{

background:#8ED8D2;

border-radius:10px;

color:#003366 !important;

}}



thead tr th {{

background:#003366 !important;

color:white !important;

}}



tbody tr td {{

background:{card_background} !important;

color:{table_text} !important;

}}



.forecast-card {{

background:#007C83;

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



@media(max-width:768px){{


.block-container {{

padding-left:1rem;

padding-right:1rem;

}}


[data-testid="stMetric"] {{

padding:12px;

}}


}}



</style>

""",
unsafe_allow_html=True
)



# =====================================================
# NAVIGATION
# =====================================================

home, dataset, models, parameters, mode = st.tabs(

[
"🏠 Dashboard",
"📊 Dataset Analysis",
"🤖 ML Models",
"⚙ Prediction Parameters",
"🌓 Theme Settings"
]

)



# =====================================================
# DASHBOARD
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



    col1,col2,col3 = st.columns(3)



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


    results = get_results()


    model_table = []


    for name,value in results.items():


        model_table.append(

        {

        "Algorithm":name,

        "Accuracy":f"{value*100:.2f}%"

        }

        )


    st.dataframe(

        model_table,

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
# THEME SETTINGS
# =====================================================

with mode:


    st.title(
        "Theme Settings"
    )


    selected_theme = st.radio(

        "Select Display Mode",

        [
            "Light",
            "Dark"
        ],

        index=0 if st.session_state.theme=="Light" else 1

    )



    if selected_theme != st.session_state.theme:

        st.session_state.theme = selected_theme

        st.rerun()
