import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo

from cyber_threat_model import (
    predict_2027,
    get_model_accuracy
)



# ===============================
# PAGE SETTINGS
# ===============================


st.set_page_config(

    page_title="Cyber Threat Prediction Report",

    layout="wide"

)



# ===============================
# CUSTOM DESIGN
# ===============================


st.markdown(
"""
<style>

body {

background-color:#000000;

}


h1 {

color:#E50914;

font-size:45px;

}


h2 {

color:#ffffff;

}


.stMetric {

background:#111111;

border:1px solid #E50914;

padding:20px;

border-radius:15px;

}


</style>

""",

unsafe_allow_html=True

)



# ===============================
# HEADER
# ===============================


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



# ===============================
# PREDICTION
# ===============================


prediction = predict_2027()


accuracy = get_model_accuracy()*100



col1,col2,col3 = st.columns(3)



with col1:

    st.metric(

        "Forecast Year",

        "2027"

    )


with col2:

    st.metric(

        "Algorithm",

        "XGBoost"

    )


with col3:

    st.metric(

        "Accuracy",

        f"{accuracy:.2f}%"

    )



st.divider()



# ===============================
# THREAT RESULT
# ===============================


st.subheader(

"2027 Cyber Threat Forecast"

)



if prediction == "Critical":

    color="#E50914"

elif prediction=="High":

    color="#ff0000"

else:

    color="#00ff00"



st.markdown(

f"""

<div style="

background:#111111;

padding:40px;

border-radius:20px;

border:3px solid {color};

text-align:center;

">


<h1 style="color:{color};">

{prediction} RISK

</h1>


<p style="color:white;">

AI Generated Cyber Threat Forecast

</p>


</div>

""",

unsafe_allow_html=True

)
