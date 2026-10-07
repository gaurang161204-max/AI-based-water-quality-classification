import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =====================================================
# 1. MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title("AI-Based Water Quality Classification")
root.geometry("1200x750")

root.configure(bg="white")


# =====================================================
# 2. DATA STORAGE
# =====================================================

samples = []
ph_values = []
turbidity_values = []
tds_values = []
temperature_values = []
outputs = []


sample_number = 0


# =====================================================
# 3. AI WATER QUALITY CLASSIFICATION
# =====================================================

def classify_water(ph, turbidity, tds, temperature):

    if (
        6.5 <= ph <= 8.5
        and turbidity <= 10
        and tds <= 500
        and temperature <= 30
    ):
        return "Normal"

    else:
        return "Abnormal"


# =====================================================
# 4. DASHBOARD TITLE
# =====================================================

title = tk.Label(
    root,
    text="AI-Based Water Quality Monitoring Dashboard",
    font=("Arial", 22, "bold"),
    bg="white"
)

title.pack(pady=10)


subtitle = tk.Label(
    root,
    text="Live Water Quality Data",
    font=("Arial", 13),
    bg="white"
)

subtitle.pack()


# =====================================================
# 5. SENSOR VALUE FRAME
# =====================================================

value_frame = tk.Frame(
    root,
    bg="white"
)

value_frame.pack(pady=15)


# pH
ph_label = tk.Label(
    value_frame,
    text="pH\n--",
    font=("Arial", 16, "bold"),
    width=15,
    height=3,
    relief="ridge",
    bg="white"
)

ph_label.grid(row=0, column=0, padx=10)


# Turbidity
turbidity_label = tk.Label(
    value_frame,
    text="Turbidity\n--",
    font=("Arial", 16, "bold"),
    width=15,
    height=3,
    relief="ridge",
    bg="white"
)

turbidity_label.grid(row=0, column=1, padx=10)


# TDS
tds_label = tk.Label(
    value_frame,
    text="TDS\n--",
    font=("Arial", 16, "bold"),
    width=15,
    height=3,
    relief="ridge",
    bg="white"
)

tds_label.grid(row=0, column=2, padx=10)


# Temperature
temperature_label = tk.Label(
    value_frame,
    text="Temperature\n--",
    font=("Arial", 16, "bold"),
    width=15,
    height=3,
    relief="ridge",
    bg="white"
)

temperature_label.grid(row=0, column=3, padx=10)


# AI Output
output_label = tk.Label(
    value_frame,
    text="AI Output\n--",
    font=("Arial", 16, "bold"),
    width=15,
    height=3,
    relief="ridge",
    bg="white"
)

output_label.grid(row=0, column=4, padx=10)


# =====================================================
# 6. GRAPH
# =====================================================

fig, ax = plt.subplots(
    figsize=(8, 4),
    dpi=100
)

ax.set_title("Live pH vs Sample")
ax.set_xlabel("Sample")
ax.set_ylabel("pH")
ax.set_ylim(4, 10)
ax.grid(True)

canvas = FigureCanvasTkAgg(
    fig,
    master=root
)

canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=False,
    padx=20
)


# =====================================================
# 7. TABLE
# =====================================================

table_frame = tk.Frame(root)

table_frame.pack(
    pady=10,
    fill=tk.BOTH,
    expand=True
)


columns = (
    "Sample",
    "pH",
    "Turbidity",
    "TDS",
    "Temperature",
    "AI Output"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)


for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=150,
        anchor="center"
    )


table.pack(
    fill=tk.BOTH,
    expand=True
)


# =====================================================
# 8. UPDATE LIVE DATA
# =====================================================

def update_dashboard():

    global sample_number

    sample_number += 1

    # ---------------------------------------------
    # Simulated live sensor values
    # ---------------------------------------------

    ph = round(
        random.uniform(5.5, 8.8),
        2
    )

    turbidity = round(
        random.uniform(1, 25),
        2
    )

    tds = round(
        random.uniform(200, 700),
        2
    )

    temperature = round(
        random.uniform(22, 32),
        2
    )


    # ---------------------------------------------
    # AI classification
    # ---------------------------------------------

    output = classify_water(
        ph,
        turbidity,
        tds,
        temperature
    )


    # ---------------------------------------------
    # Store data
    # ---------------------------------------------

    samples.append(sample_number)

    ph_values.append(ph)

    turbidity_values.append(
        turbidity
    )

    tds_values.append(tds)

    temperature_values.append(
        temperature
    )

    outputs.append(output)


    # ---------------------------------------------
    # Keep last 20 samples
    # ---------------------------------------------

    if len(samples) > 20:

        samples.pop(0)
        ph_values.pop(0)
        turbidity_values.pop(0)
        tds_values.pop(0)
        temperature_values.pop(0)
        outputs.pop(0)


    # ---------------------------------------------
    # Update dashboard values
    # ---------------------------------------------

    ph_label.config(
        text=f"pH\n{ph}"
    )

    turbidity_label.config(
        text=f"Turbidity\n{turbidity} NTU"
    )

    tds_label.config(
        text=f"TDS\n{tds} ppm"
    )

    temperature_label.config(
        text=f"Temperature\n{temperature} °C"
    )

    output_label.config(
        text=f"AI Output\n{output}"
    )


    # ---------------------------------------------
    # Update table
    # ---------------------------------------------

    table.insert(
        "",
        "end",
        values=(
            f"Sample {sample_number}",
            ph,
            turbidity,
            tds,
            temperature,
            output
        )
    )


    # Keep only last 10 table rows

    rows = table.get_children()

    if len(rows) > 10:

        table.delete(rows[0])


    # ---------------------------------------------
    # Update graph
    # ---------------------------------------------

    ax.clear()

    ax.plot(
        samples,
        ph_values,
        marker="o",
        linewidth=2
    )

    ax.set_title(
        "Live Raw pH Data"
    )

    ax.set_xlabel(
        "Sample"
    )

    ax.set_ylabel(
        "pH"
    )

    ax.set_ylim(
        4,
        10
    )

    ax.grid(True)

    canvas.draw()


    # ---------------------------------------------
    # Run again after 2 seconds
    # ---------------------------------------------

    root.after(
        2000,
        update_dashboard
    )


# =====================================================
# 9. START DASHBOARD
# =====================================================

update_dashboard()

root.mainloop()