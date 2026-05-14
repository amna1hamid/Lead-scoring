import streamlit as st
import pandas as pd
import csv
import os

from datetime import datetime
from model import train_model


# =========================
# LOAD MODEL
# =========================
model, accuracy = train_model()


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Customer Conversion Predictor",
    layout="centered"
)


# =========================
# SAVE LEAD FUNCTION
# =========================
def save_lead(
    name,
    platform,
    product,
    score,
    category
):

    file_name = "leads_storage.csv"

    # Check if file already exists
    file_exists = os.path.isfile(file_name)

    with open(
        file_name,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Write headers only once
        if not file_exists:

            writer.writerow([
                "Customer Name",
                "Platform",
                "Product",
                "Score",
                "Category",
                "Date"
            ])

        # Save lead data
        writer.writerow([
            name,
            platform,
            product,
            round(score, 2),
            category,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ])


# =========================
# TITLE
# =========================
st.title("AI Customer Conversion Predictor")


# =========================
# MODEL INFO
# =========================
with st.expander("Model Information"):

    st.metric(
        "Model Accuracy",
        f"{accuracy:.2f}"
    )


# =========================
# USER INPUTS
# =========================
customer_name = st.text_input(
    "Customer Name"
)

platform = st.selectbox(
    "Platform",
    [
        "Instagram",
        "WhatsApp",
        "Facebook"
    ]
)

product_interest = st.text_input(
    "Interested Product"
)

purchase_amount = st.number_input(
    "Purchase Amount ($)",
    min_value=0.0,
    max_value=100000.0,
    value=5000.0
)

visits = st.number_input(
    "Website Visits (Last 7 Days)",
    min_value=0,
    max_value=100,
    value=3
)

time_minutes = st.number_input(
    "Average Session Duration (Minutes)",
    min_value=0.0,
    max_value=500.0,
    value=10.0
)


# Convert minutes to seconds
time_spent = time_minutes * 60


# =========================
# PREDICTION BUTTON
# =========================
if st.button("Predict Conversion"):

    # Validation
    if customer_name.strip() == "":
        st.warning(
            "Please enter customer name."
        )

    elif product_interest.strip() == "":
        st.warning(
            "Please enter interested product."
        )

    else:

        # Create dataframe
        new_lead = pd.DataFrame({

            "purchase_amount": [
                purchase_amount
            ],

            "visits": [
                visits
            ],

            "time_spent": [
                time_spent
            ]

        })

        # Predict conversion
        prediction = model.predict(
            new_lead
        )[0]

        # Predict probability
        probability = (
            model.predict_proba(
                new_lead
            )[0][1] * 100
        )

        # =========================
        # LEAD CATEGORY
        # =========================
        if probability >= 80:

            category = "Very Hot 🔥"

        elif probability >= 60:

            category = "Hot Lead 🔥"

        elif probability >= 40:

            category = "Warm Lead 🟡"

        else:

            category = "Cold Lead 🔵"


        # =========================
        # SAVE LEAD
        # =========================
        save_lead(
            customer_name,
            platform,
            product_interest,
            probability,
            category
        )


        # =========================
        # DISPLAY RESULT
        # =========================
        st.subheader(
            "Prediction Result"
        )

        st.metric(
            "Conversion Probability",
            f"{probability:.2f}%"
        )

        st.success(
            f"Lead Category: {category}"
        )


        # =========================
        # BUSINESS INSIGHT
        # =========================
        st.subheader(
            "Business Recommendation"
        )

        if probability >= 80:

            st.info(
                "High-intent customer. "
                "Prioritize sales call immediately."
            )

        elif probability >= 60:

            st.info(
                "Strong lead. "
                "Send personalized follow-up."
            )

        elif probability >= 40:

            st.info(
                "Moderate interest detected. "
                "Use nurturing campaign."
            )

        else:

            st.info(
                "Low conversion chance. "
                "Retarget with offers or ads."
            )


# =========================
# SAVED LEADS DASHBOARD
# =========================
st.subheader("Saved Leads Dashboard")

try:

    leads_df = pd.read_csv(
        "leads_storage.csv"
    )

    st.dataframe(
        leads_df,
        use_container_width=True
    )
# Total leads
    total_leads = len(leads_df)

# Hot leads
    hot_leads = len(
    leads_df[
        leads_df["Category"] == "Hot Lead 🔥"
    ]
)

# Warm leads
    warm_leads = len(
    leads_df[
        leads_df["Category"] == "Warm Lead ⚠️"
    ]
)

# Cold leads
    cold_leads = len(
    leads_df[
        leads_df["Category"] == "Cold Lead ❄️"
    ]
)

st.subheader("Business Insights")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Leads",
    total_leads
)

col2.metric(
    "Hot Leads",
    hot_leads
)

col3.metric(
    "Warm Leads",
    warm_leads
)

col4.metric(
    "Cold Leads",
    cold_leads
)
except:

    st.warning(
        "No leads saved yet."
    )
   
