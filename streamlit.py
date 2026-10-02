import streamlit as st
import pandas as pd
import random
import time

# -----------------------------------------
# Page setup
# -----------------------------------------

st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="💧",
    layout="wide"
)

st.title("💧 AI-Based Water Quality Dashboard")
st.write("Live Water Quality Monitoring")

# -----------------------------------------
# Create session data
# -----------------------------------------

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=[
            "Sample",
            "pH",
            "Turbidity",
            "TDS",
            "Temperature",
            "AI_Output"
        ]
    )

# -----------------------------------------
# Generate live sensor data
# -----------------------------------------

sample_number = len(st.session_state.data) + 1

ph = round(random.uniform(5.5, 8.8), 2)
turbidity = round(random.uniform(1, 25), 2)
tds = round(random.uniform(200, 700), 2)
temperature = round(random.uniform(22, 32), 2)

# -----------------------------------------
# AI Classification
# -----------------------------------------

if (
    6.5 <= ph <= 8.5
    and turbidity <= 10
    and tds <= 500
    and temperature <= 30
):
    output = "Normal"
else:
    output = "Abnormal"

# -----------------------------------------
# Add new sample
# -----------------------------------------

new_row = pd.DataFrame({
    "Sample": [f"Sample {sample_number}"],
    "pH": [ph],
    "Turbidity": [turbidity],
    "TDS": [tds],
    "Temperature": [temperature],
    "AI_Output": [output]
})

st.session_state.data = pd.concat(
    [st.session_state.data, new_row],
    ignore_index=True
)

# Keep last 20 samples
st.session_state.data = st.session_state.data.tail(20)

# -----------------------------------------
# Current values
# -----------------------------------------

st.subheader("Live Sensor Values")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("pH", ph)
col2.metric("Turbidity", f"{turbidity} NTU")
col3.metric("TDS", f"{tds} ppm")
col4.metric("Temperature", f"{temperature} °C")
col5.metric("AI Output", output)

# -----------------------------------------
# pH graph
# -----------------------------------------

st.subheader("Live pH Graph")

chart_data = st.session_state.data.set_index("Sample")

st.line_chart(
    chart_data["pH"]
)

# -----------------------------------------
# Turbidity graph
# -----------------------------------------

st.subheader("Live Turbidity Graph")

st.line_chart(
    chart_data["Turbidity"]
)

# -----------------------------------------
# TDS graph
# -----------------------------------------

st.subheader("Live TDS Graph")

st.line_chart(
    chart_data["TDS"]
)

# -----------------------------------------
# Temperature graph
# -----------------------------------------

st.subheader("Live Temperature Graph")

st.line_chart(
    chart_data["Temperature"]
)

# -----------------------------------------
# Raw data table
# -----------------------------------------

st.subheader("Live Raw Data")

st.dataframe(
    st.session_state.data,
    use_container_width=True
)

# -----------------------------------------
# Download Excel data
# -----------------------------------------

excel_data = st.session_state.data

st.download_button(
    label="Download Current Data as CSV",
    data=excel_data.to_csv(index=False),
    file_name="water_quality_live_data.csv",
    mime="text/csv"
)

# -----------------------------------------
# Auto refresh
# -----------------------------------------

time.sleep(2)

st.rerun()