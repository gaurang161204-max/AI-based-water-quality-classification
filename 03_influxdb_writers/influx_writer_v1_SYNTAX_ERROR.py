from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

# ============================================================
# INFLUXDB CONFIGURATION
# ============================================================

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "DMv8zXGC929QI6VNYaznoi0JVg3eUoaKW-Gr3XvreRYjpZol_hNKufSSVyhe4jifbomlOTA9VIXuYTHaaT2pAA=="
INFLUXDB_ORG = "Water Quality"
INFLUXDB_BUCKET = "water"

# ============================================================
# CONNECT TO INFLUXDB
# ============================================================

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

write_api = client.write_api
    write_options=SYNCHRONOUS
)

# ============================================================
# TEST CONNECTION
# ============================================================

try:
    health = client.health()

    print("----------------------------------------")
    print("InfluxDB Connection")
    print("----------------------------------------")
    print("Status:", health.status)
    print("Message:", health.message)
    print("----------------------------------------")

except Exception as e:
    print("InfluxDB connection failed!")
    print(e)
    client.close()
    exit()

# ============================================================
# SEND WATER QUALITY DATA
# ============================================================

try:

    while True:

        # ----------------------------------------------------
        # Generate test sensor values
        # ----------------------------------------------------

        ph = round(random.uniform(6.5, 8.5), 2)

        turbidity = round(
            random.uniform(1.0, 10.0),
            2
        )

        temperature = round(
            random.uniform(20.0, 35.0),
            2
        )

        tds = round(
            random.uniform(100.0, 500.0),
            2
        )

        # ----------------------------------------------------
        # Water quality classification
        # ----------------------------------------------------

        if 6.5 <= ph <= 8.5 and turbidity <= 5:
            classification = "Normal"
        else:
            classification = "Abnormal"

        # ----------------------------------------------------
        # Create InfluxDB point
        # ----------------------------------------------------

        point = (
            Point("water_quality")
            .field("pH", ph)
            .field("turbidity", turbidity)
            .field("temperature", temperature)
            .field("TDS", tds)
            .field("classification", classification)
        )

        # ----------------------------------------------------
        # Write data
        # ----------------------------------------------------

        write_api.write(
            bucket=INFLUXDB_BUCKET,
            org=INFLUXDB_ORG,
            record=point
        )

        # ----------------------------------------------------
        # Display data
        # ----------------------------------------------------

        print("----------------------------------------")
        print("Water Quality Data")
        print("----------------------------------------")
        print("pH           :", ph)
        print("Turbidity    :", turbidity)
        print("Temperature  :", temperature)
        print("TDS          :", tds)
        print("Classification:", classification)
        print("----------------------------------------")
        print("Data sent to InfluxDB")
        print()

        # ----------------------------------------------------
        # Wait 5 seconds
        # ----------------------------------------------------

        time.sleep(5)

except KeyboardInterrupt:

    print()
    print("Program stopped by user.")

except Exception as e:

    print("Error while sending data:")
    print(e)

finally:

    client.close()
    print("InfluxDB connection closed.")