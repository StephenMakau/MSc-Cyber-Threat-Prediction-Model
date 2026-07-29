import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo


from cyber_threat_model import (

    predict_2027,

    get_model_accuracy

)



# ==========================================
# PAGE CONFIGURATION
# ==========================================


st.set_page_config(

    page_title="Cyber Threat Prediction Report",

    page_icon="🛡️",

    layout="wide"

)



# ==========================================
# COMPUTER PRIDE STYLE THEME
# ==========================================


st.markdown(

"""

<style>


.stApp {

background:#eef7ff;

}



.block-container {

padding-top:1rem;

}



h1 {

color:#003366;

font-weight:800;

}



h2 {

color:#003366;

}



h3 {

color:#003366;

}



[data-testid="stMetric"] {

background:white;

border-radius:12px;

padding:20px;

border:1px solid #b7d7f0;

box-shadow:0 4px 12px rgba(0,0,0,0.12);

}



[data-testid="stMetricLabel"] {

color:#003366 !important;

font-weight:bold;

}



[data-testid="stMetricValue"] {

color:#d35400 !important;

font-size:32px;

font-weight:800;

}



</style>

""",

unsafe_allow_html=True

)



# ==========================================
# HEADER
# ==========================================


current_time=datetime.now(

ZoneInfo("Africa/Nairobi")

).strftime(

"%d %B %Y | %H:%M:%S EAT"

)



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

f"Prediction Report Generated: {current_time}"

)



st.divider()



# ==========================================
# DASHBOARD CARDS
# ==========================================


prediction=predict_2027()

accuracy=get_model_accuracy()*100



col1,col2,col3=st.columns(3)



with col1:

    st.metric(

        "Machine Learning Model",

        "XGBoost"

    )



with col2:

    st.metric(

        "Prediction Accuracy",

        f"{accuracy:.2f}%"

    )



with col3:

    st.metric(

        "Forecast Year",

        "2027"

    )



st.divider()



# ==========================================
# MAIN REPORT SECTION
# ==========================================


st.header(

"2027 Cyber Threat Forecast"

)



if prediction=="Critical":


    st.error(

    f"""

    ## CRITICAL RISK


    Predicted Threat Level:

    **{prediction}**

    """

    )


elif prediction=="High":


    st.warning(

    f"""

    ## HIGH RISK


    Predicted Threat Level:

    **{prediction}**

    """

    )


else:


    st.success(

    f"""

    ## MODERATE RISK


    Predicted Threat Level:

    **{prediction}**

    """

    )



st.divider()



# ==========================================
# REPORT INFORMATION
# ==========================================


a,b=st.columns(2)



with a:


    st.info(

    """

    ### Research Dataset


    • Cyber Threat Indicators


    • Economic Variables


    • Vulnerability Intelligence


    """

    )



with b:


    st.success(

    """

    ### Model Information


    Supervised Machine Learning Classification


    Algorithm:

    XGBoost Classifier


    """

    )



st.divider()



st.caption(

"Cyber Threat Prediction Reporting System | MSc Cybersecurity Project | Mount Kenya University"

)
