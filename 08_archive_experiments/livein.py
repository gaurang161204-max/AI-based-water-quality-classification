import pandas as pd

# -----------------------------------------
# 1. Raw Water Quality Input Data
# -----------------------------------------

data = {
    "Sample": [
        "Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5",
        "Sample 6", "Sample 7", "Sample 8", "Sample 9", "Sample 10"
    ],

    "pH": [
        7.1, 7.4, 6.8, 6.2, 5.7,
        7.0, 7.6, 6.5, 8.2, 7.2
    ],

    "Turbidity_NTU": [
        2, 3, 8, 15, 25,
        4, 5, 18, 22, 3
    ],

    "TDS_ppm": [
        250, 280, 320, 450, 650,
        270, 300, 500, 700, 260
    ],

    "Temperature_C": [
        24, 25, 26, 28, 30,
        24, 25, 29, 31, 24
    ]
}

df = pd.DataFrame(data)


# -----------------------------------------
# 2. Water Quality Classification
# -----------------------------------------

def classify_water(row):

    if (
        6.5 <= row["pH"] <= 8.5
        and row["Turbidity_NTU"] <= 10
        and row["TDS_ppm"] <= 500
        and row["Temperature_C"] <= 30
    ):
        return "Normal"

    else:
        return "Abnormal"


# Create output column
df["AI_Output"] = df.apply(classify_water, axis=1)


# -----------------------------------------
# 3. Display Data
# -----------------------------------------

print("\nWATER QUALITY INPUT AND OUTPUT")
print("-----------------------------------------")

print(df.to_string(index=False))


# -----------------------------------------
# 4. Create Excel File
# -----------------------------------------

file_name = "water_quality_input_output.xlsx"

df.to_excel(file_name, index=False)

print("\nExcel file created successfully!")
print("File name:", file_name)