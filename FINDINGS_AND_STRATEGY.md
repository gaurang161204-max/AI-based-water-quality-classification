# Findings & Strategy

Based on reading every substantive file across the three source locations, syntax-checking all
of them with `python -m py_compile`, and actually executing the training pipeline. No source
files were modified — all testing happened on copies inside this consolidated folder.

## 0. The one-line summary

This is not one project with some bugs — it's **at least four unfinished rewrites of the same
idea, mixed together in one folder, none of which are connected to each other.** The core
components (MQTT → InfluxDB → Model → Dashboard → Grafana) each exist in some form, but no two
of them agree on a data schema, and no single path runs start-to-finish.

---

## 1. Critical issues (fix first)

### 1.1 Four live-looking InfluxDB Cloud API tokens are hardcoded in plaintext
Found in:
- `03_influxdb_writers/influx_writer_v1_SYNTAX_ERROR.py` (orig. `python1/db2.py`)
- `03_influxdb_writers/influx_connection_test_hardcoded_token_v1.py`
- `03_influxdb_writers/influx_connection_test_hardcoded_token_v2.py`
- `03_influxdb_writers/influx_writer_v2_loop_hardcoded_token.py`
- `03_influxdb_writers/influx_writer_hardcoded_token_v3.py`
- `04_dashboards/tkinter_dashboard_PLUS_leftover_influx_snippet.py` (orig. `python1/db.py`)

Four **different** tokens appear across these files — meaning several real InfluxDB Cloud
accounts/buckets have had credentials pasted into source files. One of these files
(`python1/db.py`) is duplicated almost byte-for-byte inside the **git repository that already
has a GitHub remote configured** (`07_git_repo_snapshot/db.py`). If that repo is ever pushed,
the token goes public immediately; even without pushing, anyone with filesystem/OneDrive access
to this machine can already read it.

**Action: treat all four tokens as compromised and revoke/regenerate them in InfluxDB Cloud now,
regardless of anything else in this plan.**

### 1.2 The MQTT publisher (sensor simulator) does not exist
`mqtt_sensor.py` is **0 bytes** in every one of the three places it appears. The subscriber
(`02_data_ingestion_mqtt/mqtt_subscriber_to_influxdb.py`) is fully written and correctly
subscribes to `waterquality/gaurang` on the public `broker.hivemq.com` broker — but nothing in
the codebase ever publishes to that topic. **The real-time ingestion path has never actually run
end-to-end**, because the component that would feed it data was never written (or was written
and then lost — the empty file is still there as a placeholder).

### 1.3 The dashboard never loads the trained model (filename mismatch)
`04_dashboards/streamlit_dashboard_demo_random_data.py` (orig. `app.py`) does:
```python
model = joblib.load("water_model.pkl")
```
but `01_ml_model/schema_simple_binary/train_model.py` saves the model as:
```python
joblib.dump(model, "model.pkl")
```
`water_model.pkl` does not exist anywhere on disk. The `try/except` around the load means this
fails silently and the dashboard **always** falls back to a hardcoded if/else threshold rule —
the Random Forest model it claims to use ("Real-Time Water Quality Monitoring using Random
Forest") is never actually invoked. We confirmed this by running `train_model.py` and observing
it produces `model.pkl`, not `water_model.pkl`.

### 1.4 `db2.py` has a syntax error and cannot run at all
```python
write_api = client.write_api
    write_options=SYNCHRONOUS
)
```
Missing opening `(` after `client.write_api`. Confirmed with `python -m py_compile`
(`run_log/01_syntax_check.txt`). This script has never successfully executed.

### 1.5 Two incompatible "ground truth" schemas for water quality
| | Simple schema (used by `train_model.py`, the MQTT bridge, all dashboards) | Advanced schema (used by `jkkn.py` / Grafana pipeline and the `Untitled-1.py` dashboard) |
|---|---|---|
| Features | `pH, Turbidity, TDS, Temperature` (4) | `ph, turbidity, tds, hardness, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes` (9) |
| Output | `Normal` / `Abnormal` (2-class) | `Good/Moderate/Poor` or `Safe/Marginal/Unsafe` (3-class) |

These can't be merged by just renaming columns — they represent two different design decisions
about what the product even is. Right now the Grafana piece (1.6 below) is built against the
9-feature schema while literally everything else uses the 4-feature schema, so wiring Grafana
onto the "real" pipeline today would require re-deriving it.

### 1.6 Grafana is not actually integrated — only one file even tries
Despite the project description mentioning Grafana, the only code that touches it is
`05_grafana/grafana_prometheus_pipeline.py` (orig. `jkkn.py`), which:
- needs the `grafanalib` Python package (**not installed** — confirmed via `pip list`),
- needs Prometheus + Grafana running via `docker compose` (**no `docker-compose.yml` exists
  anywhere on this machine** — confirmed by filesystem search),
- generates a dashboard JSON you'd still have to import into Grafana by hand, or push via
  Grafana's HTTP API with `--push` (needs a Grafana API key — not configured anywhere).
- Separately, two Grafana **installer `.msi` files** were found in `Downloads/`
  (`grafana_13.2.3...` and `grafana-enterprise_13.2.2...`) but there's no evidence Grafana was
  ever installed or run on this machine — no config, no provisioning folder, no dashboards JSON
  saved from a running instance.

So "Grafana" in this project today is: one unfinished script + two unopened installers.

### 1.7 Inconsistent/duplicate InfluxDB field naming
Different writer scripts write the same measurement (`water_quality`) with different field name
casing — `.field("ph", ...)` vs `.field("pH", ...)`, `.field("tds", ...)` vs `.field("TDS", ...)`.
InfluxDB treats these as entirely separate fields, so if more than one of these scripts had ever
run against the same bucket, queries and Grafana panels built against one casing would silently
miss data written by the other.

---

## 2. Other correctness issues

- **The ML "accuracy: 1.0" is not meaningful.** `water_quality.csv` (the correct-schema one) has
  only **11 rows**, split into two obviously-separable clusters (pH 5-9 "Normal" vs extreme pH
  "Abnormal"). A 100% test accuracy on a train/test split this small just means the dataset is
  a toy placeholder, not that the model works. Confirmed by actually running `train_model.py`
  (see `run_log/`).
- **`paho-mqtt` 2.1.0 is installed, but the MQTT code uses the deprecated v1 callback API**
  (`mqtt.Client()` with no `callback_api_version`, and `on_connect(client, userdata, flags, rc)`
  with 4 args). It still runs today (confirmed — prints a `DeprecationWarning`, does not error),
  but will break on a future `paho-mqtt` major version, and the project will inherit this problem
  the moment the installed package is upgraded.
- **Four separate, unconnected dashboard implementations** (2× Tkinter desktop GUI, 2× Streamlit,
  1× Plotly Dash) all re-implement the same "show sensor readings + status" idea independently,
  using **randomly generated fake data** rather than real sensor/InfluxDB data in every case.
  None of them query InfluxDB for live data despite InfluxDB writers existing elsewhere in the
  project.
- **`python1/db.py` is two unrelated scripts concatenated into one file** (an InfluxDB
  connection test followed by a complete Tkinter dashboard class) — almost certainly caused by
  pasting new code into a file without clearing it first. The InfluxDB portion at the top of the
  file is dead code; nothing after line 18 uses `client`.
- **No `requirements.txt` with any actual content exists anywhere** — both files named
  `requirements.txt` found on the system (`python1/waterQalityai/requirements.txt` and the one
  referenced by the project) are **0 bytes**. There is no single authoritative list of
  dependencies; we reconstructed the likely set by reading imports (see §4).
- **Dozens of empty (0-byte) and single-letter-named files** (`bgh`, `gfug`, `jnk`, `kmnkl`,
  `mok`, `wat1`, `water3`, `wae`, ...) scattered through `python1/`, almost all paired with a
  `.py` sibling of the same name — strongly suggests a pattern of VS Code "Save As" typos or a
  script that repeatedly wrote to the wrong path. Harmless on their own, but they make it
  very hard to tell what's real.

---

## 3. What's missing entirely

1. **A real sensor data source.** Everything downstream (MQTT bridge, InfluxDB, dashboards)
   assumes data exists, but nothing has ever published a real or simulated reading to the MQTT
   topic. There's no ESP32/Arduino firmware, no physical sensor code, and the one "publisher"
   file is empty.
2. **A real, non-trivial training dataset.** 11 hand-typed rows is a placeholder, not training
   data. A credible version of this project needs either a public water-potability dataset (the
   9-feature schema already matches the well-known Kaggle "Water Potability" dataset almost
   exactly — `jkkn.py`'s feature list is a strong hint this was the intended source) or a
   logged history of real/simulated sensor readings.
3. **A decision on one schema.** The 4-feature/2-class vs 9-feature/3-class split needs to be
   resolved before anything else is worth fixing — it determines the CSV, the model, the MQTT
   payload shape, the InfluxDB fields, and the Grafana panels all at once.
4. **One dashboard**, not four. Pick one framework (Streamlit is the most complete of the
   attempts — see `full_streamlit_ml_dashboard_UNNAMED.py`) and retire the rest.
5. **An actual Grafana setup**: Grafana + InfluxDB (or Prometheus) running somewhere (local
   Docker Compose, or Grafana Cloud), with real provisioned dashboards/data sources — not just a
   dashboard-as-code generator script that has never been run.
6. **Secrets management.** No `.env` file, no `.env.example`, no use of `python-dotenv` or OS
   environment variables anywhere except the one "best practice" `influx.py` in the git repo —
   which itself has never been run against real env vars (we don't know if it works end-to-end).
7. **A `.gitignore`.** The git repo has no commits yet, but `venv/` was about to be staged
   alongside source files, and there is nothing preventing a future `git add` from staging a
   credentials file.
8. **Tests of any kind.** Zero test files exist anywhere in the project.
9. **A single README / architecture doc.** Nothing currently explains which files matter.

---

## 4. Reconstructed dependency list (for reference — not written back to any requirements.txt)

Based on grepping every import across all source files, and cross-checked against what's
actually installed on this machine (`pip list`), everything needed for the *simple-schema*
pipeline is already installed:

```
pandas, numpy, scikit-learn, joblib, streamlit, plotly, matplotlib, dash,
paho-mqtt, influxdb-client
```
Not installed, only needed for the Grafana path: `grafanalib`. Not installed/present at all:
Prometheus, Grafana server itself, Docker.

---

## 5. Recommended strategy (in order)

This is a sequencing plan, not a code change — nothing below has been applied yet.

**Phase 0 — Containment (do today, independent of everything else)**
- Revoke/rotate all four InfluxDB tokens found in §1.1, in the InfluxDB Cloud UI.
- Add a `.gitignore` to the git repo (`venv/`, `__pycache__/`, `*.pkl`, `.env`) before the first
  commit — right now `venv/` and a `.pyc` file are staged for commit 1.

**Phase 1 — Decide the shape of the project (your call, not a code task)**
- Pick **one** schema: the simple 4-feature/2-class one (fastest to get working end-to-end
  today) or the richer 9-feature/3-class one (more credible as a "real" water-quality-index
  project, matches a known public dataset, already has a Grafana story half-written).
- Pick **one** dashboard framework. Recommendation: Streamlit — it already has the most complete
  implementation (`full_streamlit_ml_dashboard_UNNAMED.py`) and is the easiest to connect to
  both a live model and live InfluxDB data.

**Phase 2 — Rebuild one straight-through pipeline on the chosen schema**
1. Replace the 11-row CSV with a real dataset (public dataset if using the 9-feature schema).
2. Fix and keep exactly one InfluxDB writer, modeled on
   `influx_writer_env_based_BEST_PRACTICE.py` (env vars, health check, error handling) — delete
   the other five.
3. Write the actual MQTT publisher/sensor-simulator (currently missing) so the existing
   subscriber has something to receive.
4. Fix the model filename mismatch so the dashboard loads the model it just trained, and have
   the dashboard read live data (InfluxDB query) instead of `random.uniform(...)`.
5. Only then revisit Grafana: point it at the same InfluxDB bucket the pipeline above writes to,
   install `grafanalib` + stand up Grafana (Docker Compose is the fastest route on Windows, or
   use the already-downloaded installer / Grafana Cloud), and regenerate the dashboard JSON
   against the final schema.

**Phase 3 — Clean up**
- Delete (or git-ignore) the ~25 empty junk files and the 3 redundant dashboard implementations
  once Phase 2's single path is confirmed working, so future-you isn't re-reading this same
  investigation in six months.
- Add a top-level `requirements.txt`, a real `README.md` in the actual project repo, and commit.

I've deliberately not touched any original file yet — this document plus the consolidated copy
in `WaterQualityAI_Consolidated/` is meant to be the map; say the word when you want me to start
executing a specific phase above.
