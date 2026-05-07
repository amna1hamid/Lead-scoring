import pandas as pd
from sklearn.linear_model import LogisticRegression

# Load data
data = pd.read_csv("leads_data.csv")

# Features and target
X = data[["purchase_amount", "visits", "time_spent"]]
y = data["converted"]

# Train model
model = LogisticRegression()
model.fit(X, y)

print("Model trained successfully")


new_data = pd.DataFrame({
    "purchase_amount": [200],
    "visits": [5],
    "time_spent": [10]
})

prediction = model.predict(new_data)

print(prediction)


import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv("leads_data.csv")

# Features and target
X = data[["purchase_amount", "visits", "time_spent"]]
y = data["converted"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = LogisticRegression()
model.fit(X, y)

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("AI Customer Conversion Predictor")

purchase_amount = st.number_input("Purchase Amount")
visits = st.number_input("Website Visits")
time_minutes = st.number_input("Time Spent on Site (minutes)")

# Convert minutes → seconds
time_spent = time_minutes * 60

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Conversion"):

    # Prepare input
    new_lead = [[purchase_amount, visits, time_spent]]

    # Prediction
    prediction = model.predict(new_lead)[0]

    # Probability
    probability = model.predict_proba(new_lead)[0][1] * 100

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader("Prediction Result")

    st.write(f"Conversion Probability: {probability:.2f}%")

    if prediction == 1:
        st.success("This customer is likely to convert.")
    else:
        st.error("This customer is unlikely to convert.")

    # -----------------------------
    # BUSINESS INSIGHTS
    # -----------------------------
    reasons = []

    if purchase_amount > 15000:
        reasons.append("High purchase activity")

    if visits >= 4:
        reasons.append("Strong website engagement")

    if time_spent > 300:
        reasons.append("Spent significant time on site")

    if len(reasons) > 0:
        st.write("Reasons:")
        for r in reasons:
            st.write("-", r)
