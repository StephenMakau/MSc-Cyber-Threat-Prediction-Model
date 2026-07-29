import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo


from cyber_threat_model import (

predict_2027,

get_model_accuracy,

get_results,

get_dataset

)



st.set_page_config(

page_title="Cyber Threat Prediction System",

layout="wide"

)



# ===============================
# THEME
# ===============================


st.markdown("""

<style>

.stApp{

background:#e8f4ff;

}


h1,h2,h3{

color:#003366;

}


button{

font-weight:bold;

}


[data-testid="stMetric"]{

background:white;

padding:15px;

border-radius:15px;

border:1px solid #b0cce5;

}


</style>

""",unsafe_allow_html=True)



# ===============================
# TOP NAVIGATION
# ===============================


home, dataset, models = st.tabs(

[

"🏠 HOME",

"📊 DATASET",

"🤖 MODELS"

]

)



# ===============================
# HOME PAGE
# ===============================


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

    "Report Generated: " +

    datetime.now(
    ZoneInfo("Africa/Nairobi")
    ).strftime("%d %B %Y | %H:%M:%S EAT")

    )


    st.divider()



    prediction=predict_2027()

    accuracy=get_model_accuracy()*100



    c1,c2,c3=st.columns(3)



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
        "Forecast",
        "2027"
        )


    st.divider()



    st.header(
    "Cyber Threat Forecast"
    )



    if prediction=="Critical":

        st.error(
        f"CRITICAL RISK\n\nPredicted Level: {prediction}"
        )


    elif prediction=="High":

        st.warning(
        f"HIGH RISK\n\nPredicted Level: {prediction}"
        )


    else:

        st.success(
        f"MODERATE RISK\n\nPredicted Level: {prediction}"
        )




# ===============================
# DATASET PAGE
# ===============================


with dataset:


    st.title(
    "Cyber Threat Dataset"
    )


    st.write(
    "Historical cybersecurity indicators used for model training."
    )


    st.dataframe(

    get_dataset(),

    use_container_width=True

    )



# ===============================
# MODELS PAGE
# ===============================


with models:


    st.title(
    "Machine Learning Models"
    )


    results=get_results()


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
    Algorithms evaluated:

    • Logistic Regression

    • Random Forest

    • XGBoost


    Final selected model:

    XGBoost Classifier

    """

    )
