"""
Grafana-style Water Quality Dashboard (Plotly Dash)

Install:  pip install dash pandas plotly
Run:      python water_dashboard.py
Open:     http://127.0.0.1:8050
"""

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output

# -----------------------------------------
# 1. Data + classification (same as yours)
# -----------------------------------------
df = pd.DataFrame({
    "Sample": [f"Sample {i}" for i in range(1, 11)],
    "pH":          [7.1, 7.4, 6.8, 6.2, 5.7, 7.0, 7.6, 6.5, 8.2, 7.2],
    "Turbidity":   [2, 3, 8, 15, 25, 4, 5, 18, 22, 3],
    "TDS":         [250, 280, 320, 450, 650, 270, 300, 500, 700, 260],
    "Temperature": [24, 25, 26, 28, 30, 24, 25, 29, 31, 24],
})

# (min, max, unit) acceptable range for each parameter
LIMITS = {
    "pH":          (6.5, 8.5, ""),
    "Turbidity":   (0, 10, "NTU"),
    "TDS":         (0, 500, "mg/L"),
    "Temperature": (0, 30, "°C"),
}


def in_range(param, value):
    lo, hi, _ = LIMITS[param]
    return lo <= value <= hi


def classify_water(row):
    ok = all(in_range(p, row[p]) for p in LIMITS)
    return "Normal" if ok else "Abnormal"


df["AI_Output"] = df.apply(classify_water, axis=1)
df.to_csv("water_quality_results.csv", index=False)

# -----------------------------------------
# 2. Grafana-like styling
# -----------------------------------------
BG, PANEL, BORDER, TEXT = "#111217", "#181b1f", "#2c3235", "#d8d9da"
GREEN, RED, BLUE = "#73bf69", "#f2495c", "#5794f2"
LINE_COLORS = {"pH": BLUE, "Turbidity": "#ff9830", "TDS": "#b877d9", "Temperature": "#fade2a"}

panel_style = {
    "background": PANEL, "border": f"1px solid {BORDER}", "borderRadius": "4px",
    "padding": "8px", "minWidth": "0",
}
title_style = {"fontSize": "13px", "fontWeight": "500", "padding": "4px 6px 8px"}


def panel(title, child, style=None):
    return html.Div(
        [html.Div(title, style=title_style), child],
        style={**panel_style, **(style or {})},
    )


def base_layout(fig, height=280):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        height=height, margin=dict(l=40, r=15, t=10, b=40),
        legend=dict(orientation="h", y=-0.25),
    )
    fig.update_xaxes(gridcolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER)
    return fig


def stat_card(param, value):
    lo, hi, unit = LIMITS[param]
    color = GREEN if in_range(param, value) else RED
    return html.Div(
        [
            html.Div(param, style={"fontSize": "13px"}),
            html.Div(f"{value} {unit}", style={"fontSize": "38px", "fontWeight": "600", "color": color}),
            html.Div(f"limit: {lo} – {hi}", style={"fontSize": "11px", "opacity": 0.6}),
        ],
        style={**panel_style, "textAlign": "center", "padding": "14px"},
    )


# -----------------------------------------
# 3. Layout
# -----------------------------------------
app = Dash(__name__)
app.title = "Water Quality Monitoring"

app.layout = html.Div(
    style={"background": BG, "color": TEXT, "minHeight": "100vh", "padding": "14px",
           "fontFamily": "Inter, Helvetica, Arial, sans-serif"},
    children=[
        dcc.Interval(id="tick", interval=2000, n_intervals=0),  # live refresh

        html.Div([
            html.H2("💧 Water Quality Monitoring", style={"margin": 0, "fontSize": "20px"}),
            html.Div(id="status-badge"),
        ], style={"display": "flex", "justifyContent": "space-between",
                  "alignItems": "center", "marginBottom": "12px"}),

        # Row 1: stat panels
        html.Div(id="stat-row", style={
            "display": "grid", "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "12px", "marginBottom": "12px"}),

        # Row 2: time series + donut
        html.Div([
            panel("Parameter trend", html.Div([
                dcc.Dropdown(
                    id="param",
                    options=[{"label": p, "value": p} for p in LIMITS],
                    value="pH", clearable=False,
                    style={"color": "#000", "width": "200px", "marginBottom": "6px"}),
                dcc.Graph(id="ts", config={"displayModeBar": False}),
            ])),
            panel("Normal vs Abnormal", dcc.Graph(id="donut", config={"displayModeBar": False})),
        ], style={"display": "grid", "gridTemplateColumns": "2fr 1fr",
                  "gap": "12px", "marginBottom": "12px"}),

        # Row 3: all parameters + table
        html.Div([
            panel("All parameters (normalised to limit)",
                  dcc.Graph(id="multi", config={"displayModeBar": False})),
            panel("Raw data", dash_table.DataTable(
                id="table",
                columns=[{"name": c, "id": c} for c in df.columns],
                style_header={"backgroundColor": BG, "color": TEXT, "border": f"1px solid {BORDER}"},
                style_cell={"backgroundColor": PANEL, "color": TEXT,
                            "border": f"1px solid {BORDER}", "fontSize": "12px", "textAlign": "center"},
                style_data_conditional=[
                    {"if": {"filter_query": '{AI_Output} = "Abnormal"', "column_id": "AI_Output"},
                     "color": RED, "fontWeight": "bold"},
                    {"if": {"filter_query": '{AI_Output} = "Normal"', "column_id": "AI_Output"},
                     "color": GREEN, "fontWeight": "bold"},
                ],
            )),
        ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"}),
    ],
)


# -----------------------------------------
# 4. Live update callback
# -----------------------------------------
@app.callback(
    Output("stat-row", "children"),
    Output("status-badge", "children"),
    Output("ts", "figure"),
    Output("donut", "figure"),
    Output("multi", "figure"),
    Output("table", "data"),
    Input("tick", "n_intervals"),
    Input("param", "value"),
)
def refresh(n, param):
    # Reveal one more sample per tick (simulates live data); stops at the last sample
    live = df.iloc[: min(n + 1, len(df))]
    latest = live.iloc[-1]

    # Stat panels
    stats = [stat_card(p, latest[p]) for p in LIMITS]

    # Status badge
    ok = latest["AI_Output"] == "Normal"
    badge = html.Div(
        f"{latest['Sample']}: {latest['AI_Output']}",
        style={"background": GREEN if ok else RED, "color": "#000",
               "padding": "4px 14px", "borderRadius": "12px", "fontWeight": "600"})

    # Time series with threshold band
    lo, hi, unit = LIMITS[param]
    ts = go.Figure()
    ts.add_hrect(y0=lo, y1=hi, fillcolor=GREEN, opacity=0.10, line_width=0)
    ts.add_trace(go.Scatter(
        x=live["Sample"], y=live[param], mode="lines+markers",
        line=dict(color=LINE_COLORS[param], width=2),
        marker=dict(size=8, color=[GREEN if in_range(param, v) else RED for v in live[param]]),
        name=param))
    ts.update_yaxes(title=f"{param} {unit}".strip())
    base_layout(ts)

    # Donut
    counts = live["AI_Output"].value_counts()
    donut = go.Figure(go.Pie(
        labels=counts.index, values=counts.values, hole=0.6,
        marker=dict(colors=[GREEN if l == "Normal" else RED for l in counts.index])))
    base_layout(donut)

    # Multi-line: each value as % of its upper limit (so different units share one axis)
    multi = go.Figure()
    for p, (_, up, _) in LIMITS.items():
        multi.add_trace(go.Scatter(
            x=live["Sample"], y=live[p] / up * 100, mode="lines+markers",
            name=p, line=dict(color=LINE_COLORS[p])))
    multi.add_hline(y=100, line_dash="dash", line_color=RED)
    multi.update_yaxes(title="% of upper limit")
    base_layout(multi)

    return stats, badge, ts, donut, multi, live.to_dict("records")


if __name__ == "__main__":
    app.run(debug=True)