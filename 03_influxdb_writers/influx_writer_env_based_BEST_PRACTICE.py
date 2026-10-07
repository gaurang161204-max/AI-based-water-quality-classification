import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# -----------------------------
# InfluxDB Cloud settings
# -----------------------------

URL = os.environ.get("INFLUX_URL", "").rstrip("/")
TOKEN = os.environ.get("INFLUX_TOKEN", "")
ORG = os.environ.get("INFLUX_ORG", "")
BUCKET = os.environ.get("INFLUX_BUCKET", "")

missing_settings = [
    name
    for name, value in (
        ("INFLUX_URL", URL),
        ("INFLUX_TOKEN", TOKEN),
        ("INFLUX_ORG", ORG),
        ("INFLUX_BUCKET", BUCKET),
    )
    if not value
]
if missing_settings:
    raise SystemExit(
        "Set the InfluxDB connection settings before running: "
        + ", ".join(missing_settings)
    )

# -----------------------------
client = InfluxDBClient(
    url=URL,
    token=TOKEN,
    org=ORG
)

write_api = client.write_api(
    write_options=SYNCHRONOUS
)

# -----------------------------
# Water quality values
# -----------------------------

ph = 7.2
turbidity = 3.0
tds = 280.0
temperature = 25.0

# -----------------------------
# Create InfluxDB data point
# -----------------------------

point = (
    Point("water_quality")
    .field("ph", ph)
    .field("turbidity", turbidity)
    .field("tds", tds)
    .field("temperature", temperature)
)

# -----------------------------
# Send data
# -----------------------------

try:
    health = client.health()
    if health.status != "pass":
        raise ConnectionError(f"InfluxDB health check failed: {health.message}")

    write_api.write(
        bucket=BUCKET,
        org=ORG,
        record=point
    )

    print("Data sent to InfluxDB successfully!")
    print("pH:", ph)
    print("Turbidity:", turbidity)
    print("TDS:", tds)
    print("Temperature:", temperature)

except Exception as e:
    raise SystemExit(f"InfluxDB operation failed: {e}") from e

# -----------------------------
# Close connection
# -----------------------------

client.close()