import tkinter as tk
from tkinter import messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- SETTINGS ----------------
PH_MIN = 6.5
PH_MAX = 8.5

sample_number = 0
samples = []
ph_values = []


# ---------------- FUNCTIONS ----------------
def get_live_ph():
    """
    Demo function.
    Replace this with your MQTT sensor value later.
    """
    return round(random.uniform(5.5, 9.5), 2)


def update_dashboard():
    global sample_number

    # Get new pH value
    ph = get_live_ph()

    sample_number += 1

    samples.append(sample_number)
    ph_values.append(ph)

    # Keep last 30 samples
    if len(samples) > 30:
        samples.pop(0)
        ph_values.pop(0)

    # Display current pH
    ph_label.config(text=f"Current pH: {ph}")

    # Check water quality
    if PH_MIN <= ph <= PH_MAX:
        status_label.config(
            text="STATUS: NORMAL"
        )
        alert_label.config(
            text="✓ Water quality is normal"
        )
    else:
        status_label.config(
            text="STATUS: ABNORMAL"
        )
        alert_label.config(
            text="⚠ ALERT: pH OUT OF RANGE"
        )

        # Popup alert
        messagebox.showwarning(
            "Water Quality Alert",
            f"Abnormal pH detected!\n\n"
            f"Current pH: {ph}\n"
            f"Allowed range: {PH_MIN} - {PH_MAX}"
        )

    # Update graph
    ax.clear()

    ax.plot(
        samples,
        ph_values,
        marker="x",
        linewidth=2
    )

    ax.axhline(
        PH_MIN,
        linestyle="--",
        linewidth=1
    )

    ax.axhline(
        PH_MAX,
        linestyle="--",
        linewidth=1
    )

    ax.set_title("Live pH vs Sample Number")
    ax.set_xlabel("Sample Number")
    ax.set_ylabel("pH")

    ax.grid(True)

    canvas.draw()

    # Run again after 2 seconds
    root.after(2000, update_dashboard)


# ---------------- TKINTER WINDOW ----------------
root = tk.Tk()
root.title("AI-Based Water Quality Classification")
root.geometry("900x650")


# Title
title_label = tk.Label(
    root,
    text="AI-Based Water Quality Dashboard",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=10)


# Current pH
ph_label = tk.Label(
    root,
    text="Current pH: --",
    font=("Arial", 18)
)

ph_label.pack(pady=5)


# Status
status_label = tk.Label(
    root,
    text="STATUS: WAITING",
    font=("Arial", 18, "bold")
)

status_label.pack(pady=5)


# Alert
alert_label = tk.Label(
    root,
    text="Waiting for sensor data...",
    font=("Arial", 16)
)

alert_label.pack(pady=5)


# ---------------- GRAPH ----------------
figure = Figure(figsize=(8, 4), dpi=100)

ax = figure.add_subplot(111)

ax.set_title("Live pH vs Sample Number")
ax.set_xlabel("Sample Number")
ax.set_ylabel("pH")
ax.grid(True)

canvas = FigureCanvasTkAgg(
    figure,
    master=root
)

canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)


# Start dashboard
root.after(1000, update_dashboard)

root.mainloop()