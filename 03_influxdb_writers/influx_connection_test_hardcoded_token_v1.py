from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# -----------------------------------
# INFLUXDB CLOUD SETTINGS
# -----------------------------------

url = "https://us-east-1-1.aws.cloud2.influxdata.com/"
token = "DMv8zXGC929QI6VNYaznoi0JVg3eUoaKW-Gr3XvreRYjpZol_hNKufSSVyhe4jifbomlOTA9VIXuYTHaaT2pAA=="
org = "Water Qaulity Classification Project"
bucket = "water"

# -----------------------------------
# CONNECT
# -----------------------------------

client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(
    write_options=SYNCHRONOUS
)

# -----------------------------------
# CREATE TEST DATA
# -----------------------------------

point = (
    Point("water_quality")
    .field("pH", 7.1)
    .field("Turbidity", 2.0)
    .field("TDS", 250.0)
    .field("Temperature", 24.0)
)

# -----------------------------------
# SEND TO INFLUXDB
# -----------------------------------

write_api.write(
    bucket=bucket,
    org=org,
    record=point
)

print("Data successfully sent to InfluxDB Cloud!")

client.close()