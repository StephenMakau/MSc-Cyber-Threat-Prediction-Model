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
# STYLE
# ===============================


st.markdown("""

<style>

.stApp {

background:#d9efff;

}


h1 {

color:#06283D;

}


h2 {

color:#0B3954;

}


h3 {

color:#06283D;

}


[data-testid="stMetric"] {

background:white;

border-radius:15px;

padding:15px;

border:2px solid #0B3954;

}


[data-testid="stMetricLabel"] {

color:#06283D !important;

font-size:18px;

font-weight:bold;

}


[data-testid="stMetricValue"] {

color:#E65100 !important;

font-size:30px;

font-weight:bold;

}


.block-container {

padding-top:1rem;

padding-bottom:1rem;

}


</style>

""",
unsafe_allow_html=True)



# ===============================
# HEADER
# ===============================


time=datetime.now(

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



# ===============================
# RESULTS
# ===============================


prediction=predict_2027()

accuracy=get_model_accuracy()*100



col1,col2,col3=st.columns(3)



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



# ===============================
# THREAT CARD
# ===============================


if prediction=="Critical":

    colour="#C62828"

    label="CRITICAL RISK"


elif prediction=="High":

    colour="#EF6C00"

    label="HIGH RISK"


else:

    colour="#2E7D32"

    label="MODERATE RISK"



st.markdown(

f"""

## 2027 CYBER THREAT FORECAST


<div style="

background:white;

padding:25px;

border-radius:15px;

border-left:10px solid {colour};

">


<h1 style="color:{colour};">

{label}

</h1>


<h3 style="color:#06283D;">

Predicted Threat Level: {prediction}

</h3>


</div>

""",

unsafe_allow_html=True

)



# ===============================
# FOOTER INFORMATION
# ===============================


left,right=st.columns(2)



with left:

    st.info(

    """
    Dataset:
    
    Cyber Threat Indicators
    
    Economic Variables
    
    Vulnerability Intelligence
    """

    )



with right:

    st.success(

    """
    Model:

    Supervised Machine Learning

    Algorithm:

    XGBoost Classifier
    """

    )
