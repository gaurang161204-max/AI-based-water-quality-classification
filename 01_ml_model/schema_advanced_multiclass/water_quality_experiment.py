import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import RandomForestClassifier

print("======================================")
print(" AI-BASED WATER QUALITY CLASSIFICATION")
print("======================================")

# Sample training data
data = {
    "pH": [6.8, 7.0, 7.2, 7.5, 6.9, 8.5, 5.2, 9.1],
    "Turbidity": [1.2, 2.0, 1.5, 2.5, 3.0, 8.0, 10.0, 7.5],
    "Temperature": [24, 25, 26, 25, 24, 31, 32, 30],
    "TDS": [250, 300, 280, 320, 350, 700, 800, 650],
    "Quality": [
        "Normal",
        "Normal",
        "Normal",
        "Normal",
        "Normal",
        "Abnormal",
        "Abnormal",
        "Abnormal"
    ]
}

# Convert data into a table
df = pd.DataFrame(data)

# Features used by the AI model
X = df[["pH", "Turbidity", "Temperature", "TDS"]]

# Target/output
y = df["Quality"]

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X, y)

print("\nEnter current water sensor values:")

# Take raw input from user
ph = float(input("pH: "))
turbidity = float(input("Turbidity (NTU): "))
temperature = float(input("Temperature (°C): "))
tds = float(input("TDS (ppm): "))

# Prepare the input for prediction
new_water = np.array([
    [ph, turbidity, temperature, tds]
])

# Predict water quality
prediction = model.predict(new_water)[0]

print("\n======================================")
print("Water Quality Result:", prediction)
print("======================================")
print("Water Quality Result:", prediction)
print("======================================")
# Display water quality parameters
parameters = ["pH", "Turbidity", "Temperature", "TDS"]
values = [ph, turbidity, temperature, tds]

plt.figure(figsize=(8, 5))
plt.plot(parameters, values)

plt.title("Water Quality Parameters")
plt.xlabel("Water Quality Parameter")
plt.ylabel("Measured Value")

plt.grid(axis="y")
plt.show()
