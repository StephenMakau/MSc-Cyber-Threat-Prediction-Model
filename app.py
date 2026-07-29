st.markdown("""
<style>

/* ================================
   FUTURISTIC BLACK SOC DASHBOARD
   ================================ */


@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');


/* MAIN BACKGROUND */

.stApp {

    background:
    radial-gradient(circle at top,
    #1a1a1a,
    #000000 60%);

    color:white;

}


/* GLOBAL TEXT */

html, body, p, span, div, label {

    color:#f5f5f5 !important;

    font-family:
    'Inter',
    sans-serif !important;

}



/* HEADINGS */


h1 {

    color:#ffffff !important;

    font-weight:800 !important;

    letter-spacing:2px;

    text-shadow:
    0 0 15px rgba(255,255,255,0.3);

}



h2 {

    color:#ffb300 !important;

    font-weight:700 !important;

}



h3 {

    color:#00e676 !important;

}



/* ================================
   TABS
================================ */


.stTabs [data-testid="stTab"] {


    background:#111111;

    color:#ffffff !important;

    border:

    1px solid #333333;


    padding:

    12px 25px;


    font-weight:700;


    border-radius:8px 8px 0 0;


}



.stTabs [data-testid="stTab"]:hover {


    background:#222222;

    color:#ffb300 !important;

    border-color:#ffb300;


}



.stTabs [aria-selected="true"] {


    background:

    linear-gradient(

    135deg,

    #ff0000,

    #990000

    );


    color:white !important;


    border:

    2px solid #ff0000;


    box-shadow:

    0 0 20px rgba(255,0,0,.5);


}



/* ================================
   METRIC CARDS
================================ */


[data-testid="stMetric"] {


    background:

    rgba(255,255,255,0.05);


    border:

    1px solid #444;


    border-radius:15px;


    padding:25px;


    box-shadow:

    0 0 25px rgba(255,255,255,.05);


}



[data-testid="stMetricLabel"] {


    color:#cccccc !important;

    font-size:15px !important;

    font-weight:700;


}



[data-testid="stMetricValue"] {


    color:#00e676 !important;

    font-size:40px !important;

    font-weight:900;


}



/* ================================
   CARDS
================================ */


.tech-container {


    background:

    linear-gradient(

    145deg,

    #111111,

    #050505

    );


    border:

    1px solid #333;


    border-radius:20px;


    padding:25px;


}



/* ================================
   HIGH RISK BOX
================================ */


.threat-high {


    background:

    linear-gradient(

    135deg,

    #ff8c00,

    #cc5500

    );


    color:white !important;


    padding:30px;


    border-radius:20px;


    border:

    2px solid #ffb300;


    box-shadow:

    0 0 30px rgba(255,179,0,.6);


}



.threat-high h1,

.threat-high h3,

.threat-high p {


    color:white !important;


}




/* ================================
   CRITICAL BOX
================================ */


.threat-critical {


    background:

    linear-gradient(

    135deg,

    #b00000,

    #300000

    );


    padding:30px;


    border-radius:20px;


    border:

    2px solid red;


}



.threat-critical h1,

.threat-critical h3,

.threat-critical p {


    color:white !important;

}



/* ================================
   MODERATE BOX
================================ */


.threat-moderate {


    background:

    linear-gradient(

    135deg,

    #006400,

    #002200

    );


    padding:30px;


    border-radius:20px;


    border:

    2px solid #00e676;


}



.threat-moderate h1,

.threat-moderate h3,

.threat-moderate p {


    color:white !important;


}



/* ================================
   TABLES
================================ */


[data-testid="stDataFrame"] {


    background:#111111 !important;


}



thead tr th {


    background:#222222 !important;

    color:#ffb300 !important;

}



tbody tr td {


    color:white !important;


}



/* ================================
   ALERTS
================================ */


.stAlert {


    background:#111111 !important;


    border:

    1px solid #555;


}



.stAlert p {


    color:white !important;


}



/* DIVIDERS */


hr {


    border-color:#333333 !important;


}



/* SCROLL BAR */


::-webkit-scrollbar {


    width:10px;


}


::-webkit-scrollbar-track {


    background:#000;


}


::-webkit-scrollbar-thumb {


    background:#ff0000;

    border-radius:10px;


}



</style>
""", unsafe_allow_html=True)
