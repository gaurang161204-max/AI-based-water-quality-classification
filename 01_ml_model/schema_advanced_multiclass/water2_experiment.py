import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

print("==========================================")
print("   AI-BASED WATER QUALITY CLASSIFICATION")
print("==========================================")

# ------------------------------------------------
# TRAINING DATA
# 0 = Normal
# 1 = Abnormal
# ------------------------------------------------

training_data = {
    "pH": [7.2, 7.0, 7.4, 6.9, 7.1,
           6.8, 5.8, 8.9, 6.2, 9.1],

    "Turbidity": [2.5, 3.2, 4.0, 2.8, 4.5,
                  8.5, 15.0, 12.0, 10.5, 18.0],

    "TDS": [350, 420, 450, 380, 490,
            750, 1100, 900, 850, 1300],

    "Temperature": [25, 26, 27, 24, 26,
                    28, 30, 29, 28, 31],

    "Quality": [0, 0, 0, 0, 0,
                1, 1, 1, 1, 1]
}

df = pd.DataFrame(training_data)

# ------------------------------------------------
# INPUT FEATURES
# ------------------------------------------------

X = df[["pH", "Turbidity", "TDS", "Temperature"]]

# OUTPUT / LABEL
y = df["Quality"]

# ------------------------------------------------
# TRAIN RANDOM FOREST
# ------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

print("\nModel trained successfully!")


# ------------------------------------------------
# TAKE RAW SENSOR INPUT
# ------------------------------------------------

print("\n========== ENTER RAW DATA ==========")

ph = float(input("Enter pH: "))
turbidity = float(input("Enter Turbidity (NTU): "))
tds = float(input("Enter TDS (ppm): "))
temperature = float(input("Enter Temperature (°C): "))


# ------------------------------------------------
# DISPLAY RAW INPUT
# ------------------------------------------------

print("\n========== RAW INPUT DATA ==========")

print("pH          :", ph)
print("Turbidity   :", turbidity, "NTU")
print("TDS         :", tds, "ppm")
print("Temperature :", temperature, "°C")


# ------------------------------------------------
# CREATE INPUT FOR MODEL
# ------------------------------------------------

new_data = pd.DataFrame([{
    "pH": ph,
    "Turbidity": turbidity,
    "TDS": tds,
    "Temperature": temperature
}])


# ------------------------------------------------
# RANDOM FOREST PREDICTION
# ------------------------------------------------

prediction = model.predict(new_data)[0]

probability = model.predict_proba(new_data)[0]


# ------------------------------------------------
# CONVERT OUTPUT
# ------------------------------------------------

if prediction == 0:
    result = "NORMAL"
else:
    result = "ABNORMAL"


# ------------------------------------------------
# DISPLAY OUTPUT
# ------------------------------------------------

print("\n========== AI OUTPUT ==========")

print("Water Quality :", result)

print("Normal Probability   :", round(probability[0] * 100, 2), "%")
print("Abnormal Probability :", round(probability[1] * 100, 2), "%")


# ------------------------------------------------
# GRAPH
# ------------------------------------------------

parameters = ["pH", "Turbidity", "TDS", "Temperature"]
values = [ph, turbidity, tds, temperature]

plt.figure(figsize=(8, 5))

plt.bar(parameters, values)

plt.xlabel("Water Quality Parameters")
plt.ylabel("Sensor Value")
plt.title("Raw Water Quality Input Data")

plt.grid(axis="y")

plt.show()