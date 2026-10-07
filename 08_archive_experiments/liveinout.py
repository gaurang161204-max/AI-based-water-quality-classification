import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------------------
# 1. Sample Water Quality Input Data
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

    "Turbidity": [
        2, 3, 8, 15, 25,
        4, 5, 18, 22, 3
    ],

    "TDS": [
        250, 280, 320, 450, 650,
        270, 300, 500, 700, 260
    ],

    "Temperature": [
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
        and row["Turbidity"] <= 10
        and row["TDS"] <= 500
        and row["Temperature"] <= 30
    ):
        return "Normal"

    else:
        return "Abnormal"


df["AI_Output"] = df.apply(classify_water, axis=1)


# -----------------------------------------
# 3. Display Raw Data
# -----------------------------------------

print("\nWATER QUALITY RAW DATA")
print("---------------------------------------------")

print(df.to_string(index=False))


# -----------------------------------------
# 4. Save Raw Data
# -----------------------------------------

df.to_csv("water_quality_results.csv", index=False)

print("\nResults saved as water_quality_results.csv")


# =================================================
# 5. LIVE RAW DATA GRAPH: SAMPLE vs pH
# =================================================

fig, ax = plt.subplots(figsize=(10, 6))


def update(frame):

    # Take raw data up to the current sample
    live_data = df.iloc[:frame + 1]

    # Clear previous graph
    ax.clear()

    # -----------------------------------------
    # Plot RAW pH data
    # -----------------------------------------

    ax.plot(
        live_data["Sample"],
        live_data["pH"],
        marker="o",
        linewidth=2,
        markersize=7
    )

    # -----------------------------------------
    # Graph labels
    # -----------------------------------------

    ax.set_xlabel("Water Sample")
    ax.set_ylabel("Raw pH Value")

    ax.set_title(
        "LIVE RAW WATER DATA: pH vs Sample"
    )

    # -----------------------------------------
    # pH scale
    # -----------------------------------------

    ax.set_ylim(4, 10)

    # -----------------------------------------
    # X-axis sample labels
    # -----------------------------------------

    ax.set_xticks(range(len(live_data)))

    ax.set_xticklabels(
        live_data["Sample"],
        rotation=45
    )

    # -----------------------------------------
    # Grid
    # -----------------------------------------

    ax.grid(True)

    # -----------------------------------------
    # Display current raw pH value
    # -----------------------------------------

    current_sample = live_data.iloc[-1]

    ax.text(
        0.02,
        0.95,
        f"Current Sample: {current_sample['Sample']}\n"
        f"Raw pH: {current_sample['pH']}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top"
    )

    plt.tight_layout()


# =================================================
# 6. LIVE UPDATE
# =================================================

animation = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=2000,       # Update every 2 seconds
    repeat=False
)

plt.show()