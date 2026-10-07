# AI-Based Water Quality Classification — Consolidated Project

This folder consolidates code that was scattered across **three separate locations** on this
machine into one structure, so the project can be reviewed and managed in one place.
**Nothing was deleted or edited at the source** — everything here is a *copy*. Original
locations:

1. `Desktop/abes engineering college/python1/` — the main scratch/working folder (70+ files,
   mostly undocumented experiments, by far the largest source).
2. `Desktop/WaterQualityAI/AI-based-water-quality-classification/` — a local git repository
   (never committed) with a remote already pointed at
   `github.com/gaurang161204-max/AI-based-water-quality-classification.git`.
3. `Desktop/WaterQualityAI/ai based water quality classification/` — two leftover InfluxDB
   test scripts, a near-duplicate of #2.

See [`FINDINGS_AND_STRATEGY.md`](FINDINGS_AND_STRATEGY.md) for the full issue list, what's
missing, and the recommended fix-it plan. See [`MANIFEST.md`](MANIFEST.md) for exactly which
original file became which file here.

## Folder guide

| Folder | What it is | Status |
|---|---|---|
| `01_ml_model/schema_simple_binary/` | The one ML pipeline that actually runs: `train_model.py` reads a 4-feature CSV (pH, Turbidity, TDS, Temperature) and trains a `RandomForestClassifier` → `Normal`/`Abnormal`. | Runs, but on a toy 11-row dataset |
| `01_ml_model/schema_advanced_multiclass/` | Three abandoned, more serious rewrite attempts using a 9-feature WHO/BIS-style schema (pH, Turbidity, TDS, Hardness, Chloramines, Sulfate, Conductivity, Organic_Carbon, Trihalomethanes) → 3-class output (`Good`/`Moderate`/`Poor` or `Safe`/`Marginal`/`Unsafe`). | Never wired to the rest of the project |
| `02_data_ingestion_mqtt/` | MQTT subscriber that writes incoming sensor readings to InfluxDB. | Subscriber exists; **the publisher/sensor-simulator file is empty everywhere it appears** |
| `03_influxdb_writers/` | Six variations of "connect to InfluxDB and write a point" scripts. | One is syntactically broken; four others hardcode live-looking API tokens |
| `04_dashboards/` | Four unrelated dashboard implementations (Tkinter desktop GUI ×2, Streamlit ×2, Plotly Dash ×1) that never talk to each other or to the real data pipeline. | All use randomly generated fake data, not live sensor/DB data |
| `05_grafana/` | The only real Grafana-related code: a `grafanalib`-based dashboard-as-code generator with Prometheus metrics export. | Needs `grafanalib`, Prometheus and Grafana itself (none installed/running); uses the 9-feature schema, not the 4-feature one |
| `06_data_files/` | All CSV/XLSX data found, including two **incompatible** versions of "water_quality.csv" (capitalized vs lowercase column names). | |
| `07_git_repo_snapshot/` | Copy of what's sitting staged (uncommitted) in the real git repo bound to GitHub. | Contains a hardcoded credential — see findings |
| `08_archive_experiments/` | Smaller one-off experiments kept for reference. | Not part of any working path |
| `run_log/` | Output captured from actually compiling/running the code during this review. | |

## Known-good quick test

```bash
cd 01_ml_model/schema_simple_binary
python train_model.py
```
This is the only piece of the whole project confirmed to run end-to-end as-is.
