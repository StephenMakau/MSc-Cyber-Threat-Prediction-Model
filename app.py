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


# =====================================
# STYLE
# =====================================

st.markdown("""

<style>

.stApp{

background:#002366;

color:white;

}


.block-container{

max-width:1400px;

padding-top:1rem;

}


/* Titles */

h1,h2,h3{

color:white;

font-weight:800;

}


/* Text */

p, label{

color:white;

}


/* Cards */

[data-testid="stMetric"]{

background:white;

padding:18px;

border-radius:15px;

border:2px solid #9bbce0;

box-shadow:0 5px 15px rgba(0,0,0,0.2);

}


[data-testid="stMetricLabel"]{

color:#003366 !important;

font-weight:bold;

}


[data-testid="stMetricValue"]{

color:#d35400 !important;

font-weight:900;

}


/* Tabs */

button[data-baseweb="tab"]{

color:white;

font-weight:bold;

}


button[data-baseweb="tab"][aria-selected="true"]{

background:#4169e1;

border-radius:8px;

}


/* Tables */

thead tr th{

background:#001845 !important;

color:white !important;

}


tbody tr td{

background:white !important;

color:#000 !important;

}



/* Forecast */

.forecast-card{

background:#4169e1;

padding:35px;

border-radius:20px;

text-align:center;

border:2px solid white;

}


.forecast-title{

font-size:clamp(2rem,5vw,3rem);

font-weight:900;

color:white;

}


.forecast-sub{

font-size:clamp(1rem,2vw,1.4rem);

color:white;

}



@media(max-width:768px){

.block-container{

padding-left:1rem;

padding-right:1rem;

}


[data-testid="stMetric"]{

padding:12px;

}


}

</style>

""",
unsafe_allow_html=True
)



# =====================================
# NAVIGATION
# =====================================


home, dataset, models, parameters = st.tabs(
[
"HOME",
"DATASET",
"MODELS",
"PARAMETERS"
]
)



# =====================================
# HOME
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





# =====================================
# DATASET
# =====================================

with dataset:


    st.title(
        "Cyber Threat Dataset"
    )


    st.dataframe(

        get_dataset(),

        use_container_width=True,

        hide_index=True

    )





# =====================================
# MODELS
# =====================================

with models:


    st.title(
        "Machine Learning Algorithms"
    )


    results = get_results()


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





# =====================================
# PARAMETERS
# =====================================

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
