# File Manifest — original location → consolidated location

All paths below are relative to `C:\Users\asus\OneDrive\Desktop\` unless noted.

## 01_ml_model/schema_simple_binary/
| New file | Original |
|---|---|
| `train_model.py` | `abes engineering college/python1/train_model.py` (identical copy also existed at `.../python1/waterQalityai/train_model.py`) |
| `model.pkl` | `abes engineering college/python1/model.pkl` (pre-trained output — overwritten when we re-ran training, see run_log) |
| `water_quality.csv` | `abes engineering college/python1/waterQalityai/water_quality.csv` (the schema that matches `train_model.py`) |
| `alt_train_in_app1.py` | `abes engineering college/python1/app1.py` (a second, slightly different RandomForest training script, never used by anything) |

## 01_ml_model/schema_advanced_multiclass/
| New file | Original |
|---|---|
| `full_streamlit_ml_dashboard_UNNAMED.py` | `abes engineering college/python1/Untitled-1.py` — an unsaved VS Code tab; the most complete ML dashboard in the whole project (cross-validation, ROC curves, permutation importance, CSV upload) |
| `water2_experiment.py` | `abes engineering college/python1/water2.py` |
| `water_quality_experiment.py` | `abes engineering college/python1/water_quality.py` |

## 02_data_ingestion_mqtt/
| New file | Original |
|---|---|
| `mqtt_subscriber_to_influxdb.py` | `abes engineering college/python1/water_ai.py` |
| `mqtt_subscriber_to_influxdb_DUPLICATE.py` | `abes engineering college/python1/gfug.py` (byte-for-byte identical to the above) |
| `mqtt_publisher_sensor_simulator_MISSING_EMPTY.py` | Placeholder — `python1/mqtt_sensor.py`, `python1/mqtt_sensor - Copy.py`, and `python1/waterQalityai/mqtt_sensor.py` / `mqtt_receiver.py` are **all 0 bytes** on disk. Nothing to copy. |

## 03_influxdb_writers/
| New file | Original |
|---|---|
| `influx_writer_env_based_BEST_PRACTICE.py` | `WaterQualityAI/AI-based-water-quality-classification/influx.py` — reads credentials from environment variables, validates them, checks `client.health()` |
| `influx_writer_v1_SYNTAX_ERROR.py` | `abes engineering college/python1/db2.py` — broken (`client.write_api` missing its opening `(`) |
| `influx_writer_v2_loop_hardcoded_token.py` | `abes engineering college/python1/send_data.py` — infinite loop writing fake data every 5s |
| `influx_connection_test_hardcoded_token_v1.py` | `abes engineering college/python1/from influxdb_client import InfluxDBClie.py` |
| `influx_connection_test_hardcoded_token_v2.py` | `WaterQualityAI/AI-based-water-quality-classification/from influxdb_client import InfluxDBClie.py` |
| `influx_writer_hardcoded_token_v3.py` | `WaterQualityAI/ai based water quality classification/influx.py` |

## 04_dashboards/
| New file | Original |
|---|---|
| `tkinter_dashboard_PLUS_leftover_influx_snippet.py` | `abes engineering college/python1/db.py` — **literally two scripts pasted into one file**: an InfluxDB connection test (lines 1-18, contains a live-looking token) followed by an entire unrelated Tkinter dashboard (lines 19-650) |
| `tkinter_dashboard_alt.py` | `abes engineering college/python1/dashbord.py` |
| `tkinter_dashboard_minimal_experiment.py` | `abes engineering college/python1/bgh.py` |
| `streamlit_dashboard_demo_random_data.py` | `abes engineering college/python1/app.py` |
| `streamlit_dashboard_basic.py` | `abes engineering college/python1/streamlit.py` (identical copies also found at `WaterQualityAI/AI-based-water-quality-classification/streamlit.py` and `python1/import streamlit as st.py`) |
| `dash_plotly_dashboard.py` | `abes engineering college/python1/bhui.py` |

## 05_grafana/
| New file | Original |
|---|---|
| `grafana_prometheus_pipeline.py` | `abes engineering college/python1/jkkn.py` (duplicate extensionless copy at `python1/jkkn`) — the only file in the project that actually touches Grafana (via `grafanalib`) and Prometheus |

## 06_data_files/
| New file | Original |
|---|---|
| `water_quality_CORRECT_SCHEMA.csv` | `python1/waterQalityai/water_quality.csv` |
| `water_quality_LOWERCASE_SCHEMA_INCOMPATIBLE.csv` | `python1/water_quality.csv` — different column casing, breaks `train_model.py` |
| `water_quality_results_sample_output.csv` | `python1/water_quality_results.csv` (identical to `python1/wa` and to the git repo's own copy) |
| `live_water_quality.xlsx`, `water_quality_input_output.xlsx` | same names in `python1/` |

## 07_git_repo_snapshot/
Copy of the actual (uncommitted) working tree of the git repository at
`WaterQualityAI/AI-based-water-quality-classification/` that has `origin` already set to
`https://github.com/gaurang161204-max/AI-based-water-quality-classification.git`.

## 08_archive_experiments/
Smaller one-off scripts kept for reference: `abnormal.py`, `wa.py`, `wae.py`, `livein.py`,
`liveinout.py`, `water3.py`, `water4.py`, `kmnkl.py`, `test.py`, `LIVE WATTER QUALITY .py` — all
from `abes engineering college/python1/`.

## Not copied (left in place, zero value to duplicate)
- ~25 **empty (0-byte) files** in `python1/` created by accidental saves: `bgh`, `gfug`, `jnk`,
  `kmnkl`, `mok`, `mok.py`, `wat1`, `water3`, `wae`, `waterQua.py`, `waterQua.txt`,
  `waterQualityAI.py`, `mqtt_sensor.py`, `mqtt_sensor - Copy.py`,
  `waterQalityai/dashbord.py`, `waterQalityai/model.pkl.txt`, `waterQalityai/mqtt_receiver.py`,
  `waterQalityai/mqtt_sensor.py`, `waterQalityai/requirements.txt`,
  `waterQalityai/water_quality_model.pkl.csv`, `python water dashboard`, and others.
- `__pycache__/`, `venv/`, `.venv/` directories (build artifacts, not source).
- `tempCodeRunnerFile.py` / `.python` (VS Code "Code Runner" leftovers, not real project files).
- `New Microsoft Publisher Document.pub` (unrelated Publisher file sitting in the same folder).
- `Untitled-1.txt`, `fst.json`, `wa.txt`, `water3.txt`, `waterQua.txt` — text/JSON dumps that
  duplicate content already present in a `.py`/`.csv` sibling.
