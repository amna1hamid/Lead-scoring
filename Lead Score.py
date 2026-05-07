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
