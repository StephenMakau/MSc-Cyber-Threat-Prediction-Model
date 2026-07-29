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



# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="MKU Cyber Threat Intelligence",

    page_icon="🛡️",

    layout="wide",

    initial_sidebar_state="collapsed"

)



# ==========================================
# FUTURISTIC BLACK SECURITY THEME
# ==========================================


st.markdown("""
<style>


.stApp {

    background:#000000;

    color:white;

}


/* GLOBAL TEXT */


p, span, div, label {

    color:white !important;

    font-family:
    Arial,
    sans-serif;

}



h1 {

    color:white !important;

    font-weight:900;

    letter-spacing:2px;

}



h2 {

    color:#ffb300 !important;

}



h3 {

    color:#00e676 !important;

}




/* ===============================
   TABS
================================ */


.stTabs [data-testid="stTab"] {


    background:#111111;

    color:white !important;

    border:

    1px solid #444;


    padding:

    12px 25px;


    font-weight:bold;


}



.stTabs [aria-selected="true"] {


    background:#b00000 !important;

    color:white !important;

    border:

    2px solid red;


}



/* ===============================
METRIC BOXES
================================ */


[data-testid="stMetric"] {


    background:#111111;


    border:

    1px solid #444;


    border-radius:15px;


    padding:20px;


}



[data-testid="stMetricLabel"] {


    color:#ffffff !important;


}



[data-testid="stMetricValue"] {


    color:#00e676 !important;

    font-size:40px !important;

    font-weight:bold;


}



/* ===============================
CARDS
================================ */


.tech-container {


    background:#111111;


    border:

    1px solid #333;


    border-radius:20px;


    padding:25px;


}



/* ===============================
HIGH RISK
================================ */


.threat-high {


    background:#ff8c00;


    padding:30px;


    border-radius:20px;


    border:

    3px solid #ffb300;


}



.threat-high * {


    color:white !important;


}



/* ===============================
CRITICAL
================================ */


.threat-critical {


    background:#990000;


    padding:30px;


    border-radius:20px;


}



.threat-critical * {


    color:white !important;


}




/* ===============================
MODERATE
================================ */


.threat-moderate {


    background:#006400;


    padding:30px;


    border-radius:20px;


}



.threat-moderate * {


    color:white !important;


}



/* ===============================
TABLES
================================ */


[data-testid="stDataFrame"] {


    background:#111111;


}



thead tr th {


    background:#222222 !important;

    color:#ffb300 !important;


}



tbody tr td {


    color:white !important;


}



</style>

""", unsafe_allow_html=True)




# ==========================================
# SYSTEM TIME
# ==========================================


current_time = datetime.now(

    ZoneInfo("Africa/Nairobi")

).strftime(

    "%d %B %Y | %H:%M:%S EAT"

)




# ==========================================
# NAVIGATION TABS
# ==========================================


home, overview, dataset, models, parameters = st.tabs(

    [

        "🏠 HOME",

        "📄 PROJECT OVERVIEW",

        "📊 DATASET",

        "🤖 AI MODELS",

        "⚙️ PARAMETERS"

    ]

)




# ==========================================
# HOME PAGE
# ==========================================


with home:


    st.title(
        "🛡️ CYBER THREAT INTELLIGENCE SYSTEM"
    )


    st.subheader(
        "MSc Cybersecurity Project | Mount Kenya University"
    )


    st.write(

        "Author: Stephen Musau Makau"

    )


    st.caption(

        f"System Report Generated: {current_time}"

    )


    st.info(

        """
        This project applies machine learning techniques
        to predict future cyber threat trends affecting
        Kenyan Government Digital Services using threat
        indicators, vulnerability intelligence and economic
        variables.
        """

    )


    try:

        prediction = predict_2027()

        accuracy = get_model_accuracy()*100


    except Exception as e:

        st.error(e)

        prediction="ERROR"

        accuracy=0



    st.divider()


    st.header(
        "📡 THREAT FORECAST 2027"
    )



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



    if prediction=="High":


        st.markdown(

        f"""

        <div class="threat-high">

        <h1>HIGH RISK</h1>

        <h3>Predicted Level: {prediction}</h3>

        </div>

        """,

        unsafe_allow_html=True

        )


    elif prediction=="Critical":


        st.markdown(

        f"""

        <div class="threat-critical">

        <h1>CRITICAL RISK</h1>

        <h3>Predicted Level: {prediction}</h3>

        </div>

        """,

        unsafe_allow_html=True

        )


    else:


        st.markdown(

        f"""

        <div class="threat-moderate">

        <h1>MODERATE RISK</h1>

        <h3>Predicted Level: {prediction}</h3>

        </div>

        """,

        unsafe_allow_html=True

        )





# ==========================================
# PROJECT OVERVIEW
# ==========================================


with overview:


    st.title(
        "📄 PROJECT OVERVIEW"
    )


    st.write(

    """

    The Cyber Threat Prediction Model uses supervised
    machine learning algorithms to analyse historical
    cyber threat indicators and forecast future risk levels.

    Evaluated variables include:

    - Malware attacks
    - DDoS attacks
    - Phishing attacks
    - Web attacks
    - Critical vulnerabilities
    - Patch delays
    - Network traffic
    - Economic indicators

    """

    )




# ==========================================
# DATASET TAB
# ==========================================


with dataset:


    st.title(
        "📊 DATASET INFORMATION"
    )


    st.dataframe(

        get_dataset(),

        use_container_width=True

    )




# ==========================================
# MODELS TAB
# ==========================================


with models:


    st.title(
        "🤖 MACHINE LEARNING MODELS"
    )


    results=get_results()


    model_table=[]


    for model,value in results.items():


        model_table.append(

            {

            "Algorithm":model,

            "Accuracy":f"{value*100:.2f}%",

            "Deployment":

            "ACTIVE"

            if model=="XGBoost"

            else

            "TESTED"

            }

        )


    st.table(model_table)




# ==========================================
# PARAMETERS TAB
# ==========================================


with parameters:


    st.title(

        "⚙️ FORECAST PARAMETERS"

    )


    st.dataframe(

        get_parameters(),

        use_container_width=True

    )
