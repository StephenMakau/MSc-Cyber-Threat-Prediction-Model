import streamlit as st

from cyber_threat_model import predict_2027



st.set_page_config(

page_title="Cyber Threat Prediction",

layout="wide"

)



st.title(
"MSc Cybersecurity Project"
)


st.subheader(
"Mount Kenya University"
)


st.write(
"Author: Stephen Musau Makau"
)


prediction = predict_2027()



st.metric(

"Predicted Cyber Threat Level - 2027",

prediction

)
