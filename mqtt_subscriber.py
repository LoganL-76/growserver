import paho.mqtt.client as mqtt
import requests
import json 

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "grow/sensors"
DJANGO_ENDPOINT = "http://127.0.0.1:8000/api/sensors/ingest/"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT Broker with code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try: 
        payload = json.loads(msg.payload.decode())
        print(f"Received: {payload}")

        response = requests.post(DJANGO_ENDPOINT, json=payload)
        print(f"Django response: {response.status_code}")

    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
