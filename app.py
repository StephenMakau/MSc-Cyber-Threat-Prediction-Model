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

layout="wide"

)



# =====================================
# STYLE
# =====================================


st.markdown("""

<style>


.stApp{

background:#eaf6ff;

}


h1,h2,h3{

color:#003366;

}



[data-testid="stMetric"]{

background:white;

padding:18px;

border-radius:15px;

border:2px solid #b7d7f0;

}



[data-testid="stMetricValue"]{

color:#d35400 !important;

font-weight:900;

}



</style>


""",

unsafe_allow_html=True

)



# =====================================
# NAVIGATION
# =====================================


home,dataset,models,parameters = st.tabs(

[

"🏠 HOME",

"📊 DATASET",

"🤖 MODELS",

"⚙ PARAMETERS"

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



    prediction=predict_2027()

    accuracy=get_model_accuracy()*100



    c1,c2,c3=st.columns(3)



    c1.metric(
    "Algorithm",
    "XGBoost"
    )


    c2.metric(
    "Accuracy",
    f"{accuracy:.2f}%"
    )


    c3.metric(
    "Forecast Year",
    "2027"
    )



    st.divider()



    st.header(
    "2027 Cyber Threat Forecast"
    )



    if prediction=="High":


        st.markdown(

        """

        <div style="
        background:#F57C00;
        padding:30px;
        border-radius:15px;
        text-align:center;
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



    elif prediction=="Critical":


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

    use_container_width=True

    )



# =====================================
# MODELS
# =====================================


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


    st.table(table)



# =====================================
# PARAMETERS
# =====================================


with parameters:


    st.title(
    "Prediction Parameters Evaluated"
    )


    st.write(

    """
    The following cybersecurity, technological,
    and economic variables contribute to the
    final 2027 threat projection.
    """

    )


    st.dataframe(

    get_parameters(),

    use_container_width=True

    )
