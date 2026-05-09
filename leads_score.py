import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="AI Customer Conversion Predictor",
    layout="centered"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
data = pd.read_csv("leads_data.csv")

# Features and target
X = data[["purchase_amount", "visits", "time_spent"]]
y = data["converted"]

# -----------------------------------
# TRAIN / TEST SPLIT
# -----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------------
# MODEL PIPELINE
# -----------------------------------
model = make_pipeline(
    StandardScaler(),
    LogisticRegression()
)

# Train model
model.fit(X_train, y_train)

# Model accuracy
accuracy = model.score(X_test, y_test)

# -----------------------------------
# STREAMLIT UI
# -----------------------------------
st.title("AI Customer Conversion Predictor")

st.metric("Model Accuracy", f"{accuracy:.2f}")


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

# Convert minutes to seconds
time_spent = time_minutes * 60

# -----------------------------------
# PREDICTION
# -----------------------------------
if st.button("Predict Conversion"):

    # Create DataFrame input
    new_lead = pd.DataFrame({
        "purchase_amount": [purchase_amount],
        "visits": [visits],
        "time_spent": [time_spent]
    })

    # Prediction
    prediction = model.predict(new_lead)[0]

    # Probability
    probability = model.predict_proba(new_lead)[0][1] * 100

    # -----------------------------------
    # RESULTS
    # -----------------------------------
    st.subheader("Prediction Result")

    st.write(f"Conversion Probability: {probability:.2f}%")

    # Progress bar
    st.progress(int(probability))

    # Better interpretation
    if probability >= 70:
        lead_type = "Hot Lead 🔥"

    elif probability >= 40:
        lead_type = "Warm Lead ⚠️"

    else:
        lead_type = "Cold Lead ❄️"

    st.subheader(f"Lead Category: {lead_type}")

    # -----------------------------------
    # BUSINESS INSIGHTS
    # -----------------------------------
    reasons = []

    if purchase_amount > 15000:
        reasons.append("High purchase activity")

    if visits >= 5:
        reasons.append("Strong website engagement")

    if time_spent > 600:
        reasons.append("Spent significant time on site")

    if len(reasons) > 0:
        st.subheader("Reasons")

        for r in reasons:
            st.write("-", r)

    # -----------------------------------
    # FEATURE IMPORTANCE
    # -----------------------------------
    st.subheader("Feature Importance")

    logistic_model = model.named_steps["logisticregression"]

    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": logistic_model.coef_[0]
    })

    importance_df["Absolute"] = importance_df["Importance"].abs()

    importance_df = importance_df.sort_values(
        by="Absolute",
        ascending=False
    )

    st.write(
        importance_df[["Feature", "Importance"]]
    )

    st.bar_chart(
        importance_df.set_index("Feature")["Importance"]
    )

    top_feature = importance_df.iloc[0]["Feature"]

    st.info(
        f"The most influential factor for conversion is: {top_feature}"

