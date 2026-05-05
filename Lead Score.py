def categorize_lead(score):
    if score >= 70:
        return "High Value"
    elif score >= 40:
        return "Medium Value"
    else:
        return "Low Value"

    if category == "High Value":
        st.success("This lead is likely to convert. Focus sales efforts here.")
    elif category == "Medium Value":
        st.warning("This lead needs nurturing.")
    else:
        st.error("Low priority lead.")


def explain_lead(data):
    reasons = []

    if data["purchase_amount"] > 20000:
        reasons.append("High Purchase Activity")
    if data["visits"] > 5:
        reasons.append("Frequent visits")
    if data["time_spent"] > 300:
        reasons.append("Strong engagement")

    return ", ".join(reasons)

import streamlit as st

st.title("AI Lead Scoring System")

purchase_amount = st.number_input("purchase amount")
visits = st.number_input("Website Visits")
time_minutes = st.number_input("Time Spent on Site (mintues)")
time_spent=time_minutes * 60

if st.button("Predict"):

    # Simple scoring logic (replace with your model later)
    score = min(100,(purchase_amount * 0.01 + visits * 10 + time_spent * 0.05))

    category = categorize_lead(score)
    reason = explain_lead({
        "purchase_amount": purchase_amount,
        "visits": visits,
        "time_spent": time_spent
    })

    st.write(f"### Score: {score:.2f}")
    st.write(f"### Category: {category}")
    st.write(f"### Reason: {reason}")

