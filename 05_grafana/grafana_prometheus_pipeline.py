"""
AI-based water quality classification dashboard, built with the Python
`grafanalib` library (Grafana dashboards as code).

Steps (run from the VS Code terminal):
    pip install -r requirements.txt
    python water_quality_dashboard.py train       # train ML model  -> model.joblib
    python water_quality_dashboard.py serve       # sensors + AI -> Prometheus metrics (:8000)
    docker compose up -d                          # Prometheus (:9090) + Grafana (:3000)
    python water_quality_dashboard.py dashboard --push   # build dashboard with grafanalib & upload

Without --push it only writes water_quality_dashboard.json (import it manually in Grafana).
"""
import argparse
import json
import random
import time

import numpy as np
import pandas as pd

FEATURES = ["ph", "turbidity", "tds", "hardness", "chloramines",
            "sulfate", "conductivity", "organic_carbon", "trihalomethanes"]
CLASSES = ["Good", "Moderate", "Poor"]
BASE = {"ph": 7.2, "turbidity": 2.0, "tds": 380, "hardness": 180, "chloramines": 2.5,
        "sulfate": 240, "conductivity": 480, "organic_carbon": 3.0, "trihalomethanes": 55}
STATIONS = ["Reservoir-A", "Treatment-Plant-B", "Distribution-C"]


# ----------------------------------------------------------------- 1. AI model
def make_data(n=8000, seed=42):
    r = np.random.default_rng(seed)
    df = pd.DataFrame({
        "ph": r.normal(7.2, 1.0, n).clip(3, 11), "turbidity": r.gamma(2, 1.2, n),
        "tds": r.normal(400, 180, n).clip(20, 2500), "hardness": r.normal(180, 50, n).clip(40, 400),
        "chloramines": r.normal(2.5, 1.2, n).clip(0, 10), "sulfate": r.normal(250, 80, n).clip(20, 600),
        "conductivity": r.normal(500, 150, n).clip(100, 1200),
        "organic_carbon": r.normal(3, 1.5, n).clip(0.2, 15),
        "trihalomethanes": r.normal(60, 25, n).clip(0, 180)})
    v = (((df.ph < 6.5) | (df.ph > 8.5)).astype(int) + (df.turbidity > 5) + (df.tds > 600)
         + (df.chloramines > 4) + (df.sulfate > 400) + (df.organic_carbon > 5)
         + (df.trihalomethanes > 80))
    return df, np.select([v == 0, v <= 2], [0, 1], default=2)


def train():
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    X, y = make_data()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)
    model = RandomForestClassifier(n_estimators=200, random_state=1).fit(Xtr[FEATURES], ytr)
    print(classification_report(yte, model.predict(Xte[FEATURES]), target_names=CLASSES))
    joblib.dump(model, "model.joblib")
    print("Saved model.joblib")


# ------------------------------------------------ 2. Sensors + AI -> Prometheus
def serve(interval):
    import joblib
    from prometheus_client import Counter, Gauge, start_http_server
    model = joblib.load("model.joblib")
    gauges = {f: Gauge(f"wq_{f}", f, ["station"]) for f in FEATURES}
    g_class = Gauge("wq_class_code", "0=Good 1=Moderate 2=Poor", ["station"])
    g_conf = Gauge("wq_confidence", "Model confidence 0-1", ["station"])
    c_pred = Counter("wq_predictions", "Predictions", ["station", "quality"])
    state = {s: {k: v * random.uniform(0.9, 1.1) for k, v in BASE.items()} for s in STATIONS}
    event = {s: 0 for s in STATIONS}
    start_http_server(8000)
    print("Metrics: http://localhost:8000/metrics   (Ctrl+C to stop)")
    while True:
        for s in STATIONS:
            if not event[s] and random.random() < 0.04:
                event[s] = random.randint(8, 20)            # simulated contamination
            tgt = dict(BASE)
            if event[s]:
                event[s] -= 1
                tgt.update(turbidity=9, tds=800, trihalomethanes=110,
                           organic_carbon=7, ph=5.8, chloramines=5)
            for k, b in tgt.items():
                state[s][k] = max(0.05, state[s][k] + 0.25 * (b - state[s][k]) + random.gauss(0, b * 0.03))
            p = model.predict_proba(pd.DataFrame([state[s]])[FEATURES])[0]
            c = int(np.argmax(p))
            for f in FEATURES:
                gauges[f].labels(s).set(state[s][f])
            g_class.labels(s).set(c)
            g_conf.labels(s).set(float(p[c]))
            c_pred.labels(s, CLASSES[c]).inc()
            print(f"{s:18s} {CLASSES[c]:9s} {p[c]:.0%}")
        time.sleep(interval)


# ------------------------------------------- 3. Dashboard with grafanalib
def build_dashboard():
    from grafanalib.core import (Dashboard, GaugePanel, GridPos, PieChartv2, Repeat, Stat,
                                 StatValueMapping, StateTimeline, Target, Template,
                                 Templating, Threshold, Time, TimeSeries)
    DS = "Prometheus"
    maps = [StatValueMapping(text=n, mapValue=str(i), id=i) for i, n in enumerate(CLASSES)]
    class_thr = [Threshold("green", 0, 0.0), Threshold("orange", 1, 1.0), Threshold("red", 2, 2.0)]

    panels = [
        Stat(title="$station - Water Quality", dataSource=DS, gridPos=GridPos(h=5, w=8, x=0, y=0),
             targets=[Target(expr='wq_class_code{station="$station"}', refId="A")],
             mappings=maps, thresholds=class_thr, colorMode="background", graphMode="none",
             repeat=Repeat(direction="h", variable="station", maxPerRow=3)),
        GaugePanel(title="Model Confidence", dataSource=DS, gridPos=GridPos(h=8, w=6, x=0, y=5),
                   targets=[Target(expr='avg(wq_confidence{station=~"$station"})', refId="A")],
                   min=0, max=1, format="percentunit",
                   thresholds=[Threshold("red", 0, 0.0), Threshold("orange", 1, 0.6),
                               Threshold("green", 2, 0.85)]),
        StateTimeline(title="AI Classification Timeline", dataSource=DS,
                      gridPos=GridPos(h=8, w=12, x=6, y=5),
                      targets=[Target(expr='wq_class_code{station=~"$station"}',
                                      legendFormat="{{station}}", refId="A")],
                      mappings=maps, thresholds=class_thr, showValue="never"),
        PieChartv2(title="Predictions by Class", dataSource=DS, gridPos=GridPos(h=8, w=6, x=18, y=5),
                   targets=[Target(
                       expr='sum by (quality) (increase(wq_predictions_total{station=~"$station"}[$__range]))',
                       legendFormat="{{quality}}", refId="A")],
                   pieType="donut", legendDisplayMode="table", legendValues=["value"]),
    ]

    params = [("pH", "ph", 8.5), ("Turbidity (NTU)", "turbidity", 5), ("TDS (mg/L)", "tds", 600),
              ("Hardness (mg/L)", "hardness", None), ("Chloramines (ppm)", "chloramines", 4),
              ("Sulfate (mg/L)", "sulfate", 400), ("Conductivity (uS/cm)", "conductivity", None),
              ("Organic Carbon (ppm)", "organic_carbon", 5),
              ("Trihalomethanes (ug/L)", "trihalomethanes", 80)]
    for i, (title, metric, limit) in enumerate(params):
        targets = [Target(expr=f'wq_{metric}{{station=~"$station"}}',
                          legendFormat="{{station}}", refId="A")]
        if limit is not None:   # safe-limit reference line
            targets.append(Target(expr=f"vector({limit})", legendFormat="limit", refId="B"))
        panels.append(TimeSeries(title=title, dataSource=DS, targets=targets, lineWidth=2,
                                 gridPos=GridPos(h=8, w=8, x=(i % 3) * 8, y=13 + (i // 3) * 8)))

    station_var = Template(name="station", label="Station", dataSource=DS, type="query",
                           query="label_values(wq_class_code, station)",
                           includeAll=True, multi=True, refresh=2, default="$__all")
    return Dashboard(title="AI Water Quality Classification", uid="water-quality-ai",
                     tags=["water", "ai"], refresh="5s", time=Time("now-15m", "now"),
                     templating=Templating(list=[station_var]), panels=panels).auto_panel_ids()


def dashboard(push, url, user, password):
    from grafanalib._gen import DashboardEncoder
    data = json.loads(json.dumps(build_dashboard().to_json_data(), cls=DashboardEncoder))
    with open("water_quality_dashboard.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Wrote water_quality_dashboard.json")
    if not push:
        return
    import requests
    auth = (user, password)
    ds = {"name": "Prometheus", "uid": "prometheus", "type": "prometheus", "access": "proxy",
          "url": "http://prometheus:9090", "isDefault": True}
    r = requests.post(f"{url}/api/datasources", json=ds, auth=auth, timeout=10)
    print("Data source:", "created" if r.ok else f"{r.status_code} {r.text[:80]}")
    r = requests.post(f"{url}/api/dashboards/db", json={"dashboard": data, "overwrite": True},
                      auth=auth, timeout=10)
    print("Dashboard:", r.status_code, r.text[:120])
    if r.ok:
        print(f"Open {url}{r.json().get('url', '')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("cmd", choices=["train", "serve", "dashboard"])
    ap.add_argument("--interval", type=float, default=5)
    ap.add_argument("--push", action="store_true", help="upload to Grafana via its HTTP API")
    ap.add_argument("--url", default="http://localhost:3000")
    ap.add_argument("--user", default="admin")
    ap.add_argument("--password", default="admin")
    a = ap.parse_args()
    if a.cmd == "train":
        train()
    elif a.cmd == "serve":
        serve(a.interval)
    else:
        dashboard(a.push, a.url, a.user, a.password)