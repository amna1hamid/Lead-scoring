def categorize_lead(score):
    if score >= 70:
        return "High Value"
    elif score >= 40:
        return "Medium Value"
    else:
        return "Low Value"


def explain_lead(data):
    reasons = []

    if data["income"] > 50000:
        reasons.append("High income")
    if data["visits"] > 5:
        reasons.append("Frequent visits")
    if data["time_spent"] > 10:
        reasons.append("High engagement")

    return ", ".join(reasons)

import streamlit as st

st.title("AI Lead Scoring System")

income = st.number_input("Enter Income")
visits = st.number_input("Website Visits")
time_spent = st.number_input("Time Spent on Site")

if st.button("Predict"):

    # Simple scoring logic (replace with your model later)
    score = (income * 0.3 + visits * 5 + time_spent * 2) / 10

    category = categorize_lead(score)
    reason = explain_lead({
        "income": income,
        "visits": visits,
        "time_spent": time_spent
    })

    st.write(f"### Score: {score:.2f}")
    st.write(f"### Category: {category}")
    st.write(f"### Reason: {reason}")