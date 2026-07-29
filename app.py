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


    # =====================================
    # PROJECT DESCRIPTION
    # =====================================


    st.markdown(

    """

    <div style="
    background:white;
    padding:20px;
    border-radius:15px;
    border-left:8px solid #003366;
    margin-top:15px;
    ">


    <h3 style="color:#003366;">
    Project Overview
    </h3>


    <p style="color:#333333; font-size:16px;">

    This project develops a machine learning-based cyber threat
    prediction model designed to forecast future cybersecurity risk
    trends affecting Kenyan government digital services.


    The system evaluates historical cyber threat indicators,
    vulnerability intelligence, technology-related factors, and
    economic variables to identify patterns that contribute to
    increased cyber risk levels.


    Using supervised machine learning classification algorithms,
    including XGBoost, Random Forest, and Logistic Regression,
    the model analyses previous threat behaviour and generates a
    projected cyber threat classification for the year 2027.

    </p>


    </div>

    """,

    unsafe_allow_html=True

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
