from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# -----------------------------
# InfluxDB Cloud settings
# -----------------------------

URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
TOKEN = "hump-dhdD9s3KdmvY6mkVaI-M3FJ9uu9ivZG-Xyl-WNSGnGdiVgfTc3KKftsQsHp8_bUYFXTWc9ydc05NKCyiA=="
ORG = "WaterQuality"
BUCKET = "water"

# -----------------------------
# Connect to InfluxDB
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
    print("Error:", e)

# -----------------------------
# Close connection
# -----------------------------

client.close()