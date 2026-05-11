import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression


def train_model():

    # Load dataset
    data = pd.read_csv("leads_data.csv")

    # Features
    X = data[
        ["purchase_amount", "visits", "time_spent"]
    ]

    # Target
    y = data["converted"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Create pipeline
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression()
    )

    # Train model
    model.fit(X_train, y_train)

    # Accuracy
    accuracy = model.score(X_test, y_test)

    # Return model and accuracy
    return model, accuracy