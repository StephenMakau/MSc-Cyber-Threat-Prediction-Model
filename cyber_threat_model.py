import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from lightgbm import LGBMClassifier
data = {

"Year":[
2020,2020,2021,2021,
2022,2022,2023,2023,
2024,2025
],

"Month":[
3,9,2,10,3,8,2,11,5,7
],

"DDoS_Attacks":[
500,700,900,1200,1800,
2400,3200,2800,2100,1900
],

"Malware_Attacks":[
4000,5000,6500,7500,
9000,12000,15000,
13000,11000,9500
],

"Phishing_Attacks":[
600,800,1000,1300,
1700,2200,3000,
2600,1800,1500
],

"Web_Attacks":[
1000,1200,1600,2000,
2500,3200,4000,
3500,3000,2800
],

"Critical_CVEs":[
20,25,30,35,
45,55,70,65,50,45
],

"Patch_Delay_Days":[
20,18,17,15,
14,12,10,11,13,15
],

"Traffic_Volume":[
200000,250000,300000,
350000,450000,600000,
800000,750000,
700000,650000
],

"Inflation_Rate":[
5.4,5.6,6.1,6.4,
7.9,8.5,9.2,7.8,
5.7,4.5
],

"GDP_Growth":[
5.3,5.0,7.5,5.9,
5.4,5.2,4.8,5.6,
5.0,5.5
],

"Economic_Environment":[
"Stable",
"Stable",
"Improving",
"Stable",
"High_Cost",
"High_Cost",
"High_Cost",
"Pressure",
"Improving",
"Stable"
],

"Threat_Level":[
"Medium",
"Medium",
"Medium",
"High",
"High",
"High",
"Critical",
"High",
"Medium",
"Medium"
]

}


df = pd.DataFrame(data)
encoder = LabelEncoder()


df["Economic_Environment"] = encoder.fit_transform(
    df["Economic_Environment"]
)


df["Threat_Level"] = encoder.fit_transform(
    df["Threat_Level"]
)


X = df.drop(
    "Threat_Level",
    axis=1
)


y = df["Threat_Level"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)


xgb_model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)


xgb_model.fit(
    X_train,
    y_train
)


xgb_prediction = xgb_model.predict(
    X_test
)
xgb_prediction = xgb_model.predict(
    X_test
)


model_accuracy = accuracy_score(
    y_test,
    xgb_prediction
)


print(
    "Model Accuracy:",
    model_accuracy
)

xgb_model.fit(
    X_train,
    y_train
)
def predict_2027():


    future_2027 = pd.DataFrame({

        "Year":[2027],

        "Month":[8],

        "DDoS_Attacks":[4200],

        "Malware_Attacks":[18500],

        "Phishing_Attacks":[4100],

        "Web_Attacks":[5200],

        "Critical_CVEs":[95],

        "Patch_Delay_Days":[9],

        "Traffic_Volume":[1100000],

        "Inflation_Rate":[6.8],

        "GDP_Growth":[5.2],

        "Economic_Environment":[2]

    })


    prediction = xgb_model.predict(
        future_2027
    )


    result = encoder.inverse_transform(
        prediction
    )


    return result[0]
