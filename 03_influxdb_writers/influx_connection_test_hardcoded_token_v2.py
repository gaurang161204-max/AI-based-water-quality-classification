from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

url ="https://us-east-1-1.aws.cloud2.influxdata.com/orgs/a47909344873dc31/data-explorer?fluxScriptEditor"
token = "DMv8zXGC929QI6VNYaznoi0JVg3eUoaKW-Gr3XvreRYjpZol_hNKufSSVyhe4jifbomlOTA9VIXuYTHaaT2pAA=="
org = "WaterQuality"
bucket = "water_quality"

client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

ph_values = [6.8, 7.1, 7.4, 7.0, 7.6]

for ph in ph_values:
    point = (
        Point("water")
        .field("pH", ph)
    )

    write_api.write(
        bucket=bucket,
        org=org,
        record=point
    )

    print("pH sent:", ph)

client.close()