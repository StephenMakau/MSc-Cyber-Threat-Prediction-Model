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

layout="wide"

)



# =====================================
# THEME SELECTION
# =====================================


if "theme" not in st.session_state:

    st.session_state.theme = "Light Mode"



# =====================================
# TOP NAVIGATION
# =====================================


home, dataset, models, parameters, theme = st.tabs(

[
"🏠 HOME",
"📊 DATASET",
"🤖 MODELS",
"⚙ PARAMETERS",
"🎨 THEME"
]

)



# =====================================
# THEME SETTINGS
# =====================================


with theme:


    st.header("System Appearance")


    selected_theme = st.selectbox(

        "Choose Display Mode",

        [

        "Light Mode",

        "Dark Mode"

        ]

    )


    st.session_state.theme = selected_theme





# =====================================
# APPLY THEME
# =====================================


if st.session_state.theme == "Dark Mode":


    background="#07111f"

    card="#101d33"

    text="#ffffff"

    heading="#ffb300"


else:


    background="#eaf6ff"

    card="#ffffff"

    text="#003366"

    heading="#003366"





st.markdown(

f"""

<style>


.stApp {{

background:{background};

}}



h1,h2,h3 {{

color:{heading};

}}



p {{

color:{text};

}}



[data-testid="stMetric"] {{

background:{card};

padding:18px;

border-radius:15px;

border:2px solid #ff9800;

box-shadow:0px 5px 15px rgba(0,0,0,0.15);

}}



[data-testid="stMetricLabel"] {{

color:{text}!important;

font-weight:bold;

}}



[data-testid="stMetricValue"] {{

color:#ff9800!important;

font-weight:900;

font-size:32px;

}}



</style>


""",

unsafe_allow_html=True

)




# =====================================
# HOME TAB
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

    "Report Generated: " +

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



    if prediction=="High":


        st.markdown(

        """

        <div style="

        background:#F57C00;

        padding:35px;

        border-radius:20px;

        text-align:center;

        box-shadow:0 0 25px #F57C00;

        ">


        <h1 style="color:white;">

        HIGH RISK

        </h1>


        <h2 style="color:white;">

        Predicted Level: High

        </h2>


        </div>


        """,

        unsafe_allow_html=True

        )



    elif prediction=="Critical":


        st.markdown(

        """

        <div style="

        background:#b71c1c;

        padding:35px;

        border-radius:20px;

        text-align:center;

        ">


        <h1 style="color:white;">

        CRITICAL RISK

        </h1>


        </div>

        """,

        unsafe_allow_html=True

        )


    else:


        st.success(

        f"MODERATE RISK - {prediction}"

        )




# =====================================
# DATASET TAB
# =====================================


with dataset:


    st.header(

    "Cyber Threat Dataset"

    )


    st.dataframe(

    get_dataset(),

    use_container_width=True

    )





# =====================================
# MODELS TAB
# =====================================


with models:


    st.header(

    "Machine Learning Algorithms"

    )



    results=get_results()



    table=[]



    for name,value in results.items():


        table.append(

        {

        "Algorithm":name,

        "Accuracy":f"{value*100:.2f}%"

        }

        )



    st.table(table)




# =====================================
# PARAMETERS TAB
# =====================================


with parameters:


    st.header(

    "Prediction Parameters Evaluated"

    )


    st.write(

    """

    Variables contributing to the final 2027 cyber threat prediction.

    """

    )



    st.dataframe(

    get_parameters(),

    use_container_width=True

    )
