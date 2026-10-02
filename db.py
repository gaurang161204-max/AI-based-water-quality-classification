from influxdb_client import InfluxDBClient

from influxdb_client import InfluxDBClient

url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "jMLngUf6HbHeBfvbAeKarM-os0xmKZd5qF1-akfFc6GnoDd6_NRXyVh3KK_Ep73fxZm-ZYxuNEsKBr5bqecFQQ=="
org = "water Quality CLassifiction Project"
bucket = "water"

client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

print("Connected to InfluxDB Cloud successfully!")

client.close()
import tkinter as tk
from tkinter import ttk
import random
import math
import time
import threading

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================================
# WATER QUALITY AI DASHBOARD
# ==========================================================

class WaterQualityDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Water Quality Classification")
        self.root.geometry("1350x800")
        self.root.configure(bg="#0f172a")

        # -----------------------------
        # Variables
        # -----------------------------
        self.running = True

        self.ph = 7.0
        self.turbidity = 2.0
        self.tds = 250
        self.temperature = 25.0

        self.time_data = []
        self.ph_data = []
        self.turbidity_data = []
        self.tds_data = []
        self.classification_data = []

        self.sample_number = 0

        # -----------------------------
        # Colors
        # -----------------------------
        self.bg = "#0f172a"
        self.card = "#1e293b"
        self.card2 = "#334155"
        self.text = "#f8fafc"
        self.gray = "#94a3b8"
        self.blue = "#38bdf8"
        self.green = "#22c55e"
        self.red = "#ef4444"
        self.yellow = "#facc15"

        self.create_header()
        self.create_status_panel()
        self.create_sensor_cards()
        self.create_graph()
        self.create_table()

        self.update_dashboard()

    # ======================================================
    # HEADER
    # ======================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#111827",
            height=80
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="💧 AI-BASED WATER QUALITY MONITORING",
            font=("Segoe UI", 24, "bold"),
            bg="#111827",
            fg=self.text
        )
        title.pack(side="left", padx=30, pady=20)

        self.clock_label = tk.Label(
            header,
            text="",
            font=("Segoe UI", 12),
            bg="#111827",
            fg=self.gray
        )
        self.clock_label.pack(side="right", padx=30)

        self.update_clock()

    # ======================================================
    # STATUS PANEL
    # ======================================================

    def create_status_panel(self):

        self.status_frame = tk.Frame(
            self.root,
            bg=self.green,
            height=90
        )
        self.status_frame.pack(fill="x", padx=20, pady=15)

        self.status_label = tk.Label(
            self.status_frame,
            text="● WATER QUALITY: NORMAL",
            font=("Segoe UI", 25, "bold"),
            bg=self.green,
            fg="white"
        )

        self.status_label.pack(pady=25)

    # ======================================================
    # SENSOR CARDS
    # ======================================================

    def create_sensor_cards(self):

        container = tk.Frame(
            self.root,
            bg=self.bg
        )
        container.pack(fill="x", padx=20)

        self.ph_card = self.create_card(
            container,
            "🧪 pH",
            "7.00",
            self.blue
        )

        self.turbidity_card = self.create_card(
            container,
            "💧 Turbidity",
            "2.00 NTU",
            self.blue
        )

        self.tds_card = self.create_card(
            container,
            "⚡ TDS",
            "250 ppm",
            self.blue
        )

        self.temp_card = self.create_card(
            container,
            "🌡 Temperature",
            "25 °C",
            self.blue
        )

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg=self.card,
            width=280,
            height=110
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 13),
            bg=self.card,
            fg=self.gray
        )
        title_label.pack(pady=(15, 3))

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold"),
            bg=self.card,
            fg=color
        )
        value_label.pack()

        return value_label

    # ======================================================
    # GRAPH
    # ======================================================

    def create_graph(self):

        graph_frame = tk.Frame(
            self.root,
            bg=self.card
        )
        graph_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20, 10),
            pady=15
        )

        title = tk.Label(
            graph_frame,
            text="📈 Live Water Quality Data",
            font=("Segoe UI", 16, "bold"),
            bg=self.card,
            fg=self.text
        )

        title.pack(pady=10)

        self.figure, self.ax = plt.subplots(
            figsize=(7, 4),
            dpi=100
        )

        self.figure.patch.set_facecolor(self.card)
        self.ax.set_facecolor(self.card)

        self.ax.tick_params(
            colors="white"
        )

        self.ax.grid(
            True,
            alpha=0.2
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ======================================================
    # TABLE
    # ======================================================

    def create_table(self):

        table_frame = tk.Frame(
            self.root,
            bg=self.card,
            width=430
        )

        table_frame.pack(
            side="right",
            fill="y",
            padx=(10, 20),
            pady=15
        )

        title = tk.Label(
            table_frame,
            text="📊 Recent Readings",
            font=("Segoe UI", 16, "bold"),
            bg=self.card,
            fg=self.text
        )

        title.pack(pady=10)

        columns = (
            "Time",
            "pH",
            "NTU",
            "TDS",
            "Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=18
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=70,
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        style = ttk.Style()

        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="white",
            fieldbackground="#1e293b",
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="black",
            font=("Segoe UI", 10, "bold")
        )

    # ======================================================
    # AI CLASSIFICATION
    # ======================================================

    def classify_water(self):

        abnormal = False

        # Example water quality limits
        if self.ph < 6.5 or self.ph > 8.5:
            abnormal = True

        if self.turbidity > 5:
            abnormal = True

        if self.tds > 500:
            abnormal = True

        if abnormal:
            return "ABNORMAL"

        return "NORMAL"

    # ======================================================
    # GENERATE SENSOR DATA
    # ======================================================

    def generate_sensor_data(self):

        # Simulated sensor values
        self.ph = round(
            random.uniform(6.2, 8.8),
            2
        )

        self.turbidity = round(
            random.uniform(0.5, 8.0),
            2
        )

        self.tds = random.randint(
            150,
            650
        )

        self.temperature = round(
            random.uniform(22, 32),
            1
        )

    # ======================================================
    # UPDATE DASHBOARD
    # ======================================================

    def update_dashboard(self):

        if not self.running:
            return

        self.generate_sensor_data()

        status = self.classify_water()

        self.sample_number += 1

        current_time = time.strftime(
            "%H:%M:%S"
        )

        self.time_data.append(
            self.sample_number
        )

        self.ph_data.append(
            self.ph
        )

        self.turbidity_data.append(
            self.turbidity
        )

        self.tds_data.append(
            self.tds
        )

        self.classification_data.append(
            status
        )

        # Keep only latest 30 values
        if len(self.time_data) > 30:

            self.time_data.pop(0)
            self.ph_data.pop(0)
            self.turbidity_data.pop(0)
            self.tds_data.pop(0)
            self.classification_data.pop(0)

        # --------------------------
        # Update cards
        # --------------------------

        self.ph_card.config(
            text=f"{self.ph:.2f}"
        )

        self.turbidity_card.config(
            text=f"{self.turbidity:.2f} NTU"
        )

        self.tds_card.config(
            text=f"{self.tds} ppm"
        )

        self.temp_card.config(
            text=f"{self.temperature:.1f} °C"
        )

        # --------------------------
        # Update status
        # --------------------------

        if status == "ABNORMAL":

            self.status_frame.config(
                bg=self.red
            )

            self.status_label.config(
                text="⚠ WATER QUALITY: ABNORMAL",
                bg=self.red
            )

            self.play_alert()

        else:

            self.status_frame.config(
                bg=self.green
            )

            self.status_label.config(
                text="● WATER QUALITY: NORMAL",
                bg=self.green
            )

        # --------------------------
        # Add table row
        # --------------------------

        self.table.insert(
            "",
            0,
            values=(
                current_time,
                self.ph,
                self.turbidity,
                self.tds,
                status
            )
        )

        # Keep table small
        rows = self.table.get_children()

        if len(rows) > 10:

            self.table.delete(
                rows[-1]
            )

        # --------------------------
        # Update graph
        # --------------------------

        self.update_graph()

        # Repeat after 2 seconds
        self.root.after(
            2000,
            self.update_dashboard
        )

    # ======================================================
    # GRAPH UPDATE
    # ======================================================

    def update_graph(self):

        self.ax.clear()

        self.ax.plot(
            self.time_data,
            self.ph_data,
            marker="o",
            label="pH"
        )

        self.ax.plot(
            self.time_data,
            self.turbidity_data,
            marker="x",
            label="Turbidity"
        )

        self.ax.plot(
            self.time_data,
            np.array(self.tds_data) / 100,
            marker="s",
            label="TDS / 100"
        )

        self.ax.set_title(
            "Live Sensor Data",
            color="white"
        )

        self.ax.set_xlabel(
            "Sample",
            color="white"
        )

        self.ax.set_ylabel(
            "Sensor Value",
            color="white"
        )

        self.ax.tick_params(
            colors="white"
        )

        self.ax.grid(
            True,
            alpha=0.2
        )

        self.ax.legend()

        self.figure.tight_layout()

        self.canvas.draw()

    # ======================================================
    # ALERT SOUND
    # ======================================================

    def play_alert(self):

        # Windows beep
        try:

            import winsound

            threading.Thread(
                target=lambda:
                winsound.Beep(
                    1200,
                    400
                ),
                daemon=True
            ).start()

        except Exception:
            pass

    # ======================================================
    # CLOCK
    # ======================================================

    def update_clock(self):

        current_time = time.strftime(
            "%d-%m-%Y  %H:%M:%S"
        )

        self.clock_label.config(
            text=current_time
        )

        self.root.after(
            1000,
            self.update_clock
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WaterQualityDashboard(
        root
    )

    root.mainloop()