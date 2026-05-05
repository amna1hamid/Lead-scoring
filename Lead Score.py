def categorize_lead(score):
    if score >= 70:
        return "High Value"
    elif score >= 40:
        return "Medium Value"
    else:
        return "Low Value"


def explain_lead(data):
    reasons = []

    if data["purchase_amount"] > 50000:
        reasons.append("High Purchase Activity")
    if data["visits"] > 5:
        reasons.append("Frequent visits")
    if data["time_spent"] > 10:
        reasons.append("High engagement")

    return ", ".join(reasons)

import streamlit as st

st.title("AI Lead Scoring System")

purchase_amount = st.number_input("purchase amount")
visits = st.number_input("Website Visits")
time_spent = st.number_input("Time Spent on Site (in seconds)")

if st.button("Predict"):

    # Simple scoring logic (replace with your model later)
    score = (purchase_amount * 0.4 + visits * 5 + time_spent * 0.1) / 10

    category = categorize_lead(score)
    reason = explain_lead({
        "purchase_amount": purchase_amount,
        "visits": visits,
        "time_spent": time_spent
    })

    st.write(f"### Score: {score:.2f}")
    st.write(f"### Category: {category}")
    st.write(f"### Reason: {reason}")

minutes=time_spent/60
st.write(f"Time_spent: {minutes:.2f} minutes")