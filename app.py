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
# PAGE CONFIGURATION
# =====================================


st.set_page_config(

    page_title="Cyber Threat Prediction System",

    page_icon="🛡️",

    layout="wide"

)



# =====================================
# FUTURISTIC CORPORATE THEME
# =====================================


st.markdown("""

<style>


.stApp {

background:#eaf6ff;

}



h1,h2,h3 {

color:#003366;

font-weight:800;

}



[data-testid="stMetric"] {

background:white;

padding:18px;

border-radius:15px;

border:2px solid #b7d7f0;

box-shadow:0px 5px 15px rgba(0,0,0,0.15);

}



[data-testid="stMetricLabel"] {

color:#003366 !important;

font-weight:bold;

font-size:16px;

}



[data-testid="stMetricValue"] {

color:#d35400 !important;

font-size:32px;

font-weight:900;

}



.stTabs [data-baseweb="tab"] {

font-size:17px;

font-weight:bold;

color:#003366;

}



.stTabs [aria-selected="true"] {

background:#003366;

color:white;

}



</style>


""",

unsafe_allow_html=True

)



# =====================================
# TOP TABS
# =====================================


home, dataset, models, parameters = st.tabs(

[

"🏠 HOME",

"📊 DATASET",

"🤖 MODELS",

"⚙ PARAMETERS"

]

)



# =====================================
# HOME PAGE
# =====================================


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


    report_time = datetime.now(

        ZoneInfo("Africa/Nairobi")

    ).strftime(

        "%d %B %Y | %H:%M:%S EAT"

    )


    st.caption(

        f"Prediction Report Generated: {report_time}"

    )



    # =====================================
    # PROJECT DESCRIPTION
    # =====================================


    st.markdown(

    """

    <div style="

    background:white;

    padding:25px;

    border-radius:15px;

    border-left:8px solid #003366;

    margin-top:20px;

    ">


    <h3 style="color:#003366;">
    Project Overview
    </h3>


    <p style="color:#333333;font-size:16px;">

    This project presents a machine learning-based cyber threat
    prediction system designed to analyse historical cybersecurity
    patterns and forecast future threat levels affecting Kenyan
    government digital services.


    The model evaluates cyber threat indicators, vulnerability
    intelligence, technology-related factors, and economic variables
    to identify patterns that contribute to increasing cyber risks.


    Using supervised machine learning algorithms, the system compares
    different classification techniques and applies the XGBoost model
    to generate a projected cyber threat classification for 2027.

    </p>


    </div>


    """,

    unsafe_allow_html=True

    )



    st.divider()



    prediction = predict_2027()


    accuracy = get_model_accuracy() * 100



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

            "Forecast Horizon",

            "2027"

        )



    st.divider()



    st.header(

        "2027 Cyber Threat Forecast"

    )



    # =====================================
    # THREAT DISPLAY
    # =====================================


    if prediction == "High":


        st.markdown(

        """

        <div style="

        background:#F57C00;

        padding:35px;

        border-radius:20px;

        text-align:center;

        box-shadow:0 0 25px rgba(245,124,0,0.5);

        ">


        <h1 style="color:white;">

        HIGH RISK

        </h1>


        <h3 style="color:white;">

        Predicted Level: High

        </h3>


        </div>

        """,

        unsafe_allow_html=True

        )



    elif prediction == "Critical":


        st.markdown(

        """

        <div style="

        background:#C62828;

        padding:35px;

        border-radius:20px;

        text-align:center;

        ">


        <h1 style="color:white;">

        CRITICAL RISK

        </h1>


        <h3 style="color:white;">

        Immediate attention required

        </h3>


        </div>


        """,

        unsafe_allow_html=True

        )



    else:


        st.markdown(

        """

        <div style="

        background:#2E7D32;

        padding:35px;

        border-radius:20px;

        text-align:center;

        ">


        <h1 style="color:white;">

        MODERATE RISK

        </h1>


        </div>


        """,

        unsafe_allow_html=True

        )





# =====================================
# DATASET TAB
# =====================================


with dataset:


    st.title(

        "Cyber Threat Dataset"

    )


    st.write(

        "Historical cybersecurity indicators used for machine learning training."

    )


    st.dataframe(

        get_dataset(),

        use_container_width=True

    )





# =====================================
# MODELS TAB
# =====================================


with models:


    st.title(

        "Machine Learning Algorithms Evaluated"

    )



    results = get_results()



    model_table=[]



    for model,score in results.items():


        model_table.append(

        {

        "Algorithm":model,

        "Accuracy":f"{score*100:.2f}%"

        }

        )



    st.table(model_table)



    st.info(

    """

    The project evaluates multiple supervised learning algorithms:

    • Logistic Regression

    • Random Forest

    • XGBoost


    The final prediction model selected is XGBoost Classifier.

    """

    )





# =====================================
# PARAMETERS TAB
# =====================================


with parameters:


    st.title(

        "Prediction Parameters Evaluated"

    )


    st.write(

    """

    The following cybersecurity, infrastructure, and economic
    variables are analysed by the model to generate the 2027
    cyber threat projection.

    """

    )



    st.dataframe(

        get_parameters(),

        use_container_width=True

    )



    st.divider()



    st.subheader(

        "Evaluation Categories"

    )



    st.markdown(

    """

    **Cyber Attack Indicators**

    - DDoS Attacks

    - Malware Attacks

    - Phishing Attacks

    - Web Attacks


    **Vulnerability Indicators**

    - Critical CVEs

    - Patch Delay Days


    **Technology Indicators**

    - Traffic Volume


    **Economic Indicators**

    - Inflation Rate

    - GDP Growth

    - Economic Environment


    """

    )



st.caption(

"Cyber Threat Prediction Reporting System | MSc Cybersecurity Project | Mount Kenya University"

)
