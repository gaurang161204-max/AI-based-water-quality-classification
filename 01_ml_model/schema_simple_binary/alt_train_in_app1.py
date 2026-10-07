import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =====================================================
# 1. LOAD CSV
# =====================================================

data = pd.read_csv("water_quality.csv")

print("\nCSV loaded successfully!")
print("Columns:", data.columns.tolist())


# =====================================================
# 2. INPUT FEATURES
# =====================================================

X = data[
    [
        "ph",
        "turbidity",
        "temperature",
        "tds"
    ]
]


# =====================================================
# 3. TARGET
# =====================================================

y = data["label"]


# =====================================================
# 4. SPLIT DATA
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =====================================================
# 5. RANDOM FOREST
# =====================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# =====================================================
# 6. TRAIN
# =====================================================

model.fit(X_train, y_train)


# =====================================================
# 7. TEST
# =====================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)


# =====================================================
# 8. RESULTS
# =====================================================

print("\n====================================")
print("AI WATER QUALITY CLASSIFICATION")
print("====================================")

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# =====================================================
# 9. SAVE MODEL
# =====================================================

joblib.dump(model, "model.pkl")

print("\n====================================")
print("SUCCESS")
print("====================================")
print("model.pkl created successfully!")