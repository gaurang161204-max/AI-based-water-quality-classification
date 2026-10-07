import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# 1. Sample Water Quality Input Data
# -----------------------------------------

data = {
    "Sample": ["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5",
               "Sample 6", "Sample 7", "Sample 8", "Sample 9", "Sample 10"],

    "pH": [7.1, 7.4, 6.8, 6.2, 5.7, 7.0, 7.6, 6.5, 8.2, 7.2],

    "Turbidity": [2, 3, 8, 15, 25, 4, 5, 18, 22, 3],

    "TDS": [250, 280, 320, 450, 650, 270, 300, 500, 700, 260],

    "Temperature": [24, 25, 26, 28, 30, 24, 25, 29, 31, 24]
}

df = pd.DataFrame(data)

# -----------------------------------------
# 2. Water Quality Classification
# -----------------------------------------

def classify_water(row):

    if (6.5 <= row["pH"] <= 8.5 and
        row["Turbidity"] <= 10 and
        row["TDS"] <= 500 and
        row["Temperature"] <= 30):

        return "Normal"

    else:
        return "Abnormal"


df["AI_Output"] = df.apply(classify_water, axis=1)

# -----------------------------------------
# 3. Display Input and Output
# -----------------------------------------

print("\nWATER QUALITY CLASSIFICATION")
print("---------------------------------------------")
print(df.to_string(index=False))

# -----------------------------------------
# 4. Save results to CSV
# -----------------------------------------

df.to_csv("wa.", index=False)

print("\nResults saved as wa.csv")

# -----------------------------------------
# 5. Graph 1 - Turbidity
# -----------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(df["Sample"], df["Turbidity"])

plt.xlabel("Water Sample")
plt.ylabel("Turbidity (NTU)")
plt.title("Turbidity of Different Water Samples")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------------------
# 6. Graph 2 - pH
# -----------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(df["Sample"], df["pH"], marker="o")

plt.xlabel("Water Sample")
plt.ylabel("pH")
plt.title("pH of Different Water Samples")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------------------
# 7. Graph 3 - TDS
# -----------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(df["Sample"], df["TDS"])

plt.xlabel("Water Sample")
plt.ylabel("TDS (ppm)")
plt.title("TDS of Different Water Samples")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------------------
# 8. Graph 4 - AI Classification
# -----------------------------------------

# Convert classification into numerical values
df["Classification_Value"] = df["AI_Output"].map({
    "Normal": 0,
    "Abnormal": 1
})

plt.figure(figsize=(10, 5))

plt.plot(df["Sample"], df["Classification_Value"],marker="o")
plt.xlabel("Water Sample")
plt.ylabel("AI Classification")
plt.title("AI-Based Water Quality Classification")

plt.yticks([0, 1], ["Normal", "Abnormal"])

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
