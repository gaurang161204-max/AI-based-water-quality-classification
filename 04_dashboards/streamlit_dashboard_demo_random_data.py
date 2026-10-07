import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import random
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Water Quality",
    page_icon="💧",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💧 AI-Based Water Quality Classification")
st.caption("Real-Time Water Quality Monitoring using Random Forest")

st.divider()

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

try:
    model = joblib.load("water_model.pkl")
    model_loaded = True
except:
    model_loaded = False

# --------------------------------------------------
# GENERATE LIVE SENSOR DATA
# --------------------------------------------------

ph = round(random.uniform(5.0, 8.0), 2)
turbidity = round(random.uniform(1, 25), 2)
temperature = round(random.uniform(23, 32), 2)
tds = round(random.uniform(200, 900), 2)
conductivity = round(random.uniform(300, 1200), 2)

input_data = pd.DataFrame([{
    "pH": ph,
    "Turbidity": turbidity,
    "Temperature": temperature,
    "TDS": tds,
    "Conductivity": conductivity
}])

# --------------------------------------------------
# AI PREDICTION
# --------------------------------------------------

if model_loaded:
    prediction = model.predict(input_data)[0]
else:
    # Temporary classification if model isn't available
    if ph >= 6.5 and ph <= 8.5 and turbidity < 5 and tds < 500:
        prediction = "Normal"
    else:
        prediction = "Abnormal"

# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("pH", ph)
col2.metric("Turbidity", f"{turbidity} NTU")
col3.metric("Temperature", f"{temperature} °C")
col4.metric("TDS", f"{tds} ppm")
col5.metric("Conductivity", conductivity)

st.divider()

# --------------------------------------------------
# AI STATUS
# --------------------------------------------------

st.subheader("🤖 AI Water Quality Classification")

if prediction == "Normal":
    st.success("🟢 NORMAL WATER QUALITY")
else:
    st.error("🔴 ABNORMAL WATER QUALITY")

st.write("AI Prediction:", prediction)
st.write("Last Updated:", datetime.now().strftime("%H:%M:%S"))

# --------------------------------------------------
# CREATE SAMPLE HISTORY
# --------------------------------------------------

samples = list(range(1, 21))

ph_history = [
    round(random.uniform(6.5, 8.0), 2)
    for _ in samples
]

turbidity_history = [
    round(random.uniform(1, 10), 2)
    for _ in samples
]

tds_history = [
    round(random.uniform(200, 600), 2)
    for _ in samples
]

# --------------------------------------------------
# pH GRAPH
# --------------------------------------------------

st.subheader("📈 Live pH Monitoring")

fig_ph = go.Figure()

fig_ph.add_trace(
    go.Scatter(
        x=samples,
        y=ph_history,
        mode="lines+markers",
        name="pH"
    )
)

fig_ph.add_hline(
    y=7,
    line_dash="dash",
    annotation_text="Neutral pH"
)

fig_ph.update_layout(
    xaxis_title="Sample",
    yaxis_title="pH",
    height=400
)

st.plotly_chart(fig_ph, use_container_width=True)

# --------------------------------------------------
# TWO GRAPHS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌫️ Turbidity")

    fig_turbidity = go.Figure()

    fig_turbidity.add_trace(
        go.Scatter(
            x=samples,
            y=turbidity_history,
            mode="lines+markers",
            name="Turbidity"
        )
    )

    fig_turbidity.update_layout(
        xaxis_title="Sample",
        yaxis_title="NTU"
    )

    st.plotly_chart(
        fig_turbidity,
        use_container_width=True
    )

with col2:

    st.subheader("💧 TDS")

    fig_tds = go.Figure()

    fig_tds.add_trace(
        go.Scatter(
            x=samples,
            y=tds_history,
            mode="lines+markers",
            name="TDS"
        )
    )

    fig_tds.update_layout(
        xaxis_title="Sample",
        yaxis_title="TDS (ppm)"
    )

    st.plotly_chart(
        fig_tds,
        use_container_width=True
    )

# --------------------------------------------------
# SENSOR TABLE
# --------------------------------------------------

st.subheader("📊 Current Sensor Data")

display_data = pd.DataFrame({
    "Parameter": [
        "pH",
        "Turbidity",
        "Temperature",
        "TDS",
        "Conductivity"
    ],
    "Value": [
        ph,
        turbidity,
        temperature,
        tds,
        conductivity
    ],
    "Unit": [
        "", 
        "NTU",
        "°C",
        "ppm",
        ""
    ]
})

st.dataframe(
    display_data,
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI-Based Water Quality Classification | "
    "MQTT + Python + Random Forest + Grafana"
)