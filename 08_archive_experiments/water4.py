import matplotlib.pyplot as plt

# ==========================================
# AI-BASED WATER QUALITY CLASSIFICATION
# ==========================================

print("==========================================")
print(" AI-BASED WATER QUALITY CLASSIFICATION")
print("==========================================")

# -------- RAW DATA INPUT --------
ph = float(input("Enter pH value: "))
turbidity = float(input("Enter Turbidity (NTU): "))
tds = float(input("Enter TDS (ppm): "))
temperature = float(input("Enter Temperature (°C): "))
conductivity = float(input("Enter Conductivity (µS/cm): "))

# -------- CLASSIFICATION --------
if (6.5 <= ph <= 8.5 and
    turbidity <= 5 and
    tds <= 500 and
    conductivity <= 800):

    quality = "NORMAL"

else:
    quality = "ABNORMAL"

# -------- DISPLAY RESULT --------
print("\n==========================================")
print("             WATER QUALITY RESULT")
print("==========================================")

print("pH           :", ph)
print("Turbidity    :", turbidity, "NTU")
print("TDS          :", tds, "ppm")
print("Temperature  :", temperature, "°C")
print("Conductivity :", conductivity, "µS/cm")

print("------------------------------------------")
print("Classification :", quality)
print("==========================================")

# ==========================================
# GRAPH
# ==========================================

parameters = [
    "pH",
    "Turbidity",
    "TDS",
    "Temperature",
    "Conductivity"
]

values = [
    ph,
    turbidity,
    tds,
    temperature,
    conductivity
]

plt.figure(figsize=(10, 6))

plt.bar(parameters, values)

plt.title("AI-Based Water Quality Analysis")
plt.xlabel("Water Quality Parameters")
plt.ylabel("Sensor Value")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()