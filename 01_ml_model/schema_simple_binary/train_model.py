import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("water_quality.csv")

# Input features
X = data[["pH", "Turbidity", "TDS", "Temperature"]]

# Target
y = data["Label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")