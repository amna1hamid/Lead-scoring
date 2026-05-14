import streamlit as st
import pandas as pd
import csv
import os

from datetime import datetime
from model import train_model


# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Customer Conversion Predictor",
    layout="centered"
)


# ==========================================
# LOAD MODEL
# ==========================================
model, accuracy = train_model()


# ==========================================
# SAVE LEAD FUNCTION
# ==========================================
def save_lead(
    name,
    platform,
    product,
    score,
    category
):

    file_name = "leads_storage.csv"

    # Check if file exists
    file_exists = os.path.isfile(file_name)

    with open(
        file_name,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Write headers once
        if not file_exists:

            writer.writerow([
                "Customer Name",
                "Platform",
                "Product",
                "Score",
                "Category",
                "Date"
            ])

        # Save lead
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


# ==========================================
# APP TITLE
# ==========================================
st.title(
    "AI Customer Conversion Predictor"
)


# ==========================================
# MODEL INFO
# ==========================================
with st.expander("Model Information"):

    st.metric(
        "Model Accuracy",
        f"{accuracy:.2f}"
    )


# ==========================================
# USER INPUTS
# ==========================================
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


# ==========================================
# PREDICTION BUTTON
# ==========================================
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


        # ==========================================
        # MODEL PREDICTION
        # ==========================================
        prediction = model.predict(
            new_lead
        )[0]

        probability = (
            model.predict_proba(
                new_lead
            )[0][1] * 100
        )


        # ==========================================
        # LEAD CATEGORY
        # ==========================================
        if probability >= 80:

            category = "Very Hot 🔥"

        elif probability >= 60:

            category = "Hot Lead 🔥"

        elif probability >= 40:

            category = "Warm Lead 🟡"

        else:

            category = "Cold Lead 🔵"


        # ==========================================
        # SAVE LEAD
        # ==========================================
        save_lead(
            customer_name,
            platform,
            product_interest,
            probability,
            category
        )


        # ==========================================
        # RESULT SECTION
        # ==========================================
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


        # ==========================================
        # BUSINESS RECOMMENDATION
        # ==========================================
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


# ==========================================
# SAVED LEADS DASHBOARD
# ==========================================
st.subheader(
    "Saved Leads Dashboard"
)

try:

    # Load CSV
    leads_df = pd.read_csv(
        "leads_storage.csv"
    )


    # ==========================================
    # BUSINESS INSIGHTS
    # ==========================================
    total_leads = len(
        leads_df
    )

    hot_leads = len(
        leads_df[
            leads_df["Category"] == "Hot Lead 🔥"
        ]
    )

    very_hot_leads = len(
        leads_df[
            leads_df["Category"] == "Very Hot 🔥"
        ]
    )

    warm_leads = len(
        leads_df[
            leads_df["Category"] == "Warm Lead 🟡"
        ]
    )

    cold_leads = len(
        leads_df[
            leads_df["Category"] == "Cold Lead 🔵"
        ]
    )


    # ==========================================
    # METRICS SECTION
    # ==========================================
    st.subheader(
        "Business Insights"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Leads",
        total_leads
    )

    col2.metric(
        "Very Hot",
        very_hot_leads
    )

    col3.metric(
        "Hot Leads",
        hot_leads
    )

    col4.metric(
        "Warm Leads",
        warm_leads
    )

    col5.metric(
        "Cold Leads",
        cold_leads
    )


    # ==========================================
    # LEAD CATEGORY DISTRIBUTION
    # ==========================================
    st.subheader(
        "Lead Category Distribution"
    )

    category_counts = (
        leads_df["Category"]
        .value_counts()
    )

    st.bar_chart(
        category_counts
    )


    # ==========================================
    # PLATFORM PERFORMANCE
    # ==========================================
    st.subheader(
        "Platform Performance"
    )

    platform_counts = (
        leads_df["Platform"]
        .value_counts()
    )

    st.bar_chart(
        platform_counts
    )


    # ==========================================
    # SHOW DATAFRAME
    # ==========================================
    st.subheader(
        "Saved Leads Data"
    )

    st.dataframe(
        leads_df,
        use_container_width=True
    )


    # ==========================================
    # DOWNLOAD CSV BUTTON
    # ==========================================
    with open(
        "leads_storage.csv",
        "rb"
    ) as file:

        st.download_button(
            label="Download Leads CSV",
            data=file,
            file_name="leads_storage.csv",
            mime="text/csv"
        )


except:

    st.warning(
        "No leads saved yet."
    )
