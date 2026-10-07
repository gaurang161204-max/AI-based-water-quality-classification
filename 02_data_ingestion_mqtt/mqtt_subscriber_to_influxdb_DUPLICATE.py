import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json


# ---------------- MQTT ----------------

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "waterquality/gaurang"


# ---------------- INFLUXDB ----------------

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "YOUR_INFLUXDB_TOKEN"
INFLUX_ORG = "waterquality"
INFLUX_BUCKET = "water_data"


client_influx = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client_influx.write_api(
    write_options=SYNCHRONOUS
)


# ---------------- MQTT CONNECT ----------------

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("MQTT connected")

        client.subscribe(MQTT_TOPIC)

        print("Subscribed:", MQTT_TOPIC)

    else:

        print("MQTT connection failed")


# ---------------- RECEIVE DATA ----------------

def on_message(client, userdata, msg):

    try:

        data = json.loads(
            msg.payload.decode()
        )

        ph = float(data["ph"])
        turbidity = float(data["turbidity"])
        tds = float(data["tds"])
        temperature = float(data["temperature"])

        # Classification
        if 6.5 <= ph <= 8.5:

            status = 1

        else:

            status = 0


        point = (
            Point("water_quality")
            .field("ph", ph)
            .field("turbidity", turbidity)
            .field("tds", tds)
            .field("temperature", temperature)
            .field("status", status)
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=point
        )

        print(
            "Data stored:",
            ph,
            turbidity,
            tds,
            temperature,
            status
        )


    except Exception as e:

        print("Error:", e)


# ---------------- MQTT CLIENT ----------------

mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)

mqtt_client.loop_forever()