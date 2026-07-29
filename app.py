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



# =====================================================
# PAGE CONFIGURATION
# =====================================================


st.set_page_config(

    page_title="Cyber Threat Prediction System",

    page_icon="🛡️",

    layout="wide"

)



# =====================================================
# FUTURISTIC BLUE THEME
# =====================================================


st.markdown("""

<style>


/* Entire background */

.stApp{

background:

linear-gradient(

135deg,

#062B5C,

#0B4F8A,

#1565C0

);

}



/* Main container */

.block-container{

padding-top:20px;

}



/* Headings */

h1,h2,h3{

color:white !important;

font-weight:800;

}



p{

color:white;

font-size:16px;

}



/* Captions */

.stCaption{

color:#eeeeee !important;

}



/* Metric cards */

[data-testid="stMetric"]{

background:white;

padding:20px;

border-radius:15px;

border:3px solid #FF9800;

box-shadow:

0px 5px 20px rgba(0,0,0,0.30);

}



/* Metric titles */

[data-testid="stMetricLabel"]{

color:#003366 !important;

font-weight:bold;

font-size:16px;

}



/* Metric values */

[data-testid="stMetricValue"]{

color:#E65100 !important;

font-weight:900;

font-size:32px;

}



/* Tabs */

.stTabs [data-baseweb="tab-list"]{

gap:12px;

}



.stTabs [data-baseweb="tab"]{

background:#003366;

color:white;

padding:12px 25px;

border-radius:10px;

font-weight:bold;

}



.stTabs [aria-selected="true"]{

background:#FF9800 !important;

color:white !important;

}



/* Data tables */

[data-testid="stDataFrame"]{

background:white;

border-radius:15px;

}



/* Info boxes */

.stAlert{

border-radius:15px;

}



</style>


""",

unsafe_allow_html=True

)



# =====================================================
# TOP NAVIGATION TABS
# =====================================================


home, dataset, models, parameters = st.tabs(

[

"🏠 HOME",

"📊 DATASET",

"🤖 MODELS",

"⚙ PARAMETERS"

]

)



# =====================================================
# HOME PAGE
# =====================================================


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

        "Prediction Report Generated: " +

        datetime.now(

            ZoneInfo("Africa/Nairobi")

        ).strftime(

            "%d %B %Y | %H:%M:%S EAT"

        )

    )



    st.divider()



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



    st.header(

        "2027 Cyber Threat Forecast"

    )



    # ==============================
    # RISK DISPLAY
    # ==============================


    if prediction == "High":


        st.markdown(

        """

        <div style="

        background:#F57C00;

        padding:35px;

        border-radius:20px;

        text-align:center;

        box-shadow:0px 5px 20px rgba(0,0,0,0.35);

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


        <h2 style="color:white;">

        Immediate Attention Required

        </h2>


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





# =====================================================
# DATASET TAB
# =====================================================


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





# =====================================================
# MODELS TAB
# =====================================================


with models:


    st.title(

        "Machine Learning Algorithms Evaluated"

    )



    results = get_results()



    model_table=[]



    for model, score in results.items():


        model_table.append(

        {

        "Algorithm":model,

        "Accuracy":f"{score*100:.2f}%"

        }

        )



    st.table(

        model_table

    )



    st.info(

        """

        Models evaluated:


        • Logistic Regression


        • Random Forest


        • XGBoost Classifier


        Final selected model:

        XGBoost


        """

    )





# =====================================================
# PARAMETERS TAB
# =====================================================


with parameters:


    st.title(

        "Prediction Parameters Evaluated"

    )


    st.write(

        """

        The following cybersecurity, technological,

        and economic variables contribute to the

        final 2027 prediction.

        """

    )


    st.dataframe(

        get_parameters(),

        use_container_width=True

    )
