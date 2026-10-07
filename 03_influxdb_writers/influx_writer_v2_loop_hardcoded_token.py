from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB details
url = "http://localhost:8086"
token = "biqZhsZuHco4f6Ez1HqIuPY1YKIK2da4KaYMC2BaffcOgMbP1gUD1mssNVi51ydvL-FJToqZnhFI3kC36jc9NA=="
org = "Water Qaulity Classification Project"
bucket = "water"

# Connect to InfluxDB
client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(
    write_options=SYNCHRONOUS
)

# Data from your Python program
ph = 7.2
turbidity = 3.4
temperature = 27.5
tds = 250

# Create InfluxDB data point
point = (
    Point("water_quality")
    .field("pH", ph)
    .field("turbidity", turbidity)
    .field("temperature", temperature)
    .field("TDS", tds)
)

# Send data
write_api.write(
    bucket=bucket,
    org=org,
    record=point
)

print("Data sent successfully!")
print("pH:", ph)
print("Turbidity:", turbidity)
print("Temperature:", temperature)
print("TDS:", tds)

client.close()