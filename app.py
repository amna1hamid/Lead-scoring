import csv

from datetime import datetime

import streamlit as st

import pandas as pd

from model import train_model



# Load trained model
model, accuracy = train_model()


# Page config
st.set_page_config(
    page_title="AI Customer Conversion Predictor",
    layout="centered"
)


# Title
st.title("AI Customer Conversion Predictor")


# Accuracy display
st.metric(
    "Model Accuracy",
    f"{accuracy:.2f}"
)
customer_name = st.text_input(
    "Customer Name"
)

platform = st.selectbox(
    "Platform",
    ["Instagram", "WhatsApp", "Facebook"]
)

product_interest = st.text_input(
    "Interested Product"
)


# Inputs
purchase_amount = st.number_input(
    "Purchase Amount",
    min_value=0.0,
    value=5000.0
)

visits = st.number_input(
    "Website Visits",
    min_value=0,
    value=3
)

time_minutes = st.number_input(
    "Time Spent on Site (minutes)",
    min_value=0.0,
    value=10.0
)


# Convert to seconds
time_spent = time_minutes * 60


# Prediction button
if st.button("Predict Conversion"):

    # Create input dataframe
    new_lead = pd.DataFrame({

        "purchase_amount": [purchase_amount],

        "visits": [visits],

        "time_spent": [time_spent]

    })

    # Prediction
    prediction = model.predict(new_lead)[0]

    # Probability
    probability = (
        model.predict_proba(new_lead)[0][1] * 100
    )

    # Display result
    st.subheader("Prediction Result")

    st.write(
        f"Conversion Probability: {probability:.2f}%"
    )

def save_lead(
    name,
    platform,
    product,
    score,
    category
):

    with open(
        "leads_storage.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            name,
            platform,
            product,
            score,
            category,
            datetime.now()
        ])
