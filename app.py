import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo


from cyber_threat_model import (

    predict_2027,

    get_model_accuracy

)



# =====================================================
# PAGE SETTINGS
# =====================================================


st.set_page_config(

    page_title="Cyber Threat Prediction Report",

    page_icon="🛡️",

    layout="wide"

)



# =====================================================
# FUTURISTIC THEME
# =====================================================


st.markdown(

"""

<style>


body {

background:#020617;

}


.stApp {

background:

linear-gradient(

135deg,

#020617,

#0b1f3a,

#001122

);

color:white;

}



h1 {

color:white;

font-size:45px;

letter-spacing:3px;

}



h2 {

color:#ffffff;

}



.card {

background:

rgba(255,255,255,0.08);

border-radius:20px;

padding:25px;

border:

1px solid rgba(255,255,255,0.2);

box-shadow:

0 0 25px rgba(0,0,0,0.5);

}



</style>


""",

unsafe_allow_html=True

)



# =====================================================
# HEADER
# =====================================================


time = datetime.now(

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

f"Prediction Report Generated: {time}"

)



st.divider()



# =====================================================
# MODEL SUMMARY
# =====================================================


prediction = predict_2027()

accuracy = get_model_accuracy()*100



a,b,c = st.columns(3)



with a:

    st.metric(

        "Algorithm",

        "XGBoost"

    )


with b:

    st.metric(

        "Accuracy",

        f"{accuracy:.2f}%"

    )


with c:

    st.metric(

        "Forecast Horizon",

        "2027"

    )



st.divider()



# =====================================================
# THREAT FORECAST
# =====================================================



if prediction == "Critical":

    colour="#ff1744"

    status="CRITICAL RISK"



elif prediction=="High":

    colour="#ffb300"

    status="HIGH RISK"



else:

    colour="#00e676"

    status="MODERATE RISK"





st.markdown(

f"""

<div style="

background:rgba(0,0,0,0.35);

padding:45px;

border-radius:25px;

border:2px solid {colour};

text-align:center;

box-shadow:0 0 30px {colour};

">


<h2>

2027 CYBER THREAT FORECAST

</h2>


<h1 style="color:{colour};">

{status}

</h1>


<p style="color:white;font-size:20px;">

Predicted Threat Classification:
<br>

<b>{prediction}</b>

</p>


</div>


""",

unsafe_allow_html=True

)



st.divider()



# =====================================================
# REPORT INFORMATION
# =====================================================


left,right = st.columns(2)



with left:

    st.markdown(

    """

    <div class="card">

    <h3>Research Dataset</h3>

    Cyber Threat Indicators<br>

    Economic Variables<br>

    Vulnerability Intelligence

    </div>

    """,

    unsafe_allow_html=True

    )



with right:

    st.markdown(

    """

    <div class="card">

    <h3>Model Type</h3>

    Supervised Machine Learning Classification

    <br><br>

    Algorithm:

    XGBoost Classifier

    </div>

    """,

    unsafe_allow_html=True

    )
