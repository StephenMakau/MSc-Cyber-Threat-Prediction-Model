import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo

from cyber_threat_model import (
    predict_2027,
    get_model_accuracy
)



# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(

    page_title="Cyber Threat Prediction Report",

    page_icon="🛡️",

    layout="wide"

)



# =====================================
# FUTURISTIC THEME
# =====================================

st.markdown(

"""

<style>

.stApp {

background:

linear-gradient(

135deg,

#d8efff,

#b9dcf5

);

}


h1 {

color:#06283D;

font-size:42px;

font-weight:800;

}


h2 {

color:#06283D;

}


h3 {

color:#0B3954;

}


[data-testid="stMetric"] {

background:white;

border-radius:15px;

padding:15px;

border:2px solid #0B3954;

box-shadow:0px 4px 15px rgba(0,0,0,0.15);

}


[data-testid="stMetricLabel"] {

color:#06283D !important;

font-size:17px;

font-weight:bold;

}


[data-testid="stMetricValue"] {

color:#E65100 !important;

font-size:30px;

font-weight:900;

}


.stAlert {

font-size:18px;

}


</style>

""",

unsafe_allow_html=True

)



# =====================================
# HEADER
# =====================================


report_time = datetime.now(

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
    f"Prediction Report Generated: {report_time}"
)



st.divider()



# =====================================
# MODEL RESULTS
# =====================================


prediction = predict_2027()


accuracy = get_model_accuracy() * 100



col1, col2, col3 = st.columns(3)



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



# =====================================
# THREAT FORECAST
# =====================================


st.subheader(

    "2027 CYBER THREAT FORECAST"

)



if prediction == "Critical":


    st.error(

        f"""

        ### 🔴 CRITICAL RISK


        Predicted Threat Level:

        **{prediction}**

        """

    )


elif prediction == "High":


    st.warning(

        f"""

        ### 🟠 HIGH RISK


        Predicted Threat Level:

        **{prediction}**

        """

    )


else:


    st.success(

        f"""

        ### 🟢 MODERATE RISK


        Predicted Threat Level:

        **{prediction}**

        """

    )



st.divider()



# =====================================
# REPORT INFORMATION
# =====================================


left, right = st.columns(2)



with left:


    st.info(

        """

        **Research Dataset**


        • Cyber Threat Indicators

        • Economic Variables

        • Vulnerability Intelligence


        """

    )



with right:


    st.success(

        """

        **Model Information**


        Machine Learning Classification


        Algorithm:

        XGBoost Classifier


        """

    )
