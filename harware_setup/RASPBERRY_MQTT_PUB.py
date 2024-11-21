import paho.mqtt.client as mqtt
import pandas as pd

# MQTT Configuration
MQTT_BROKER = "192.168.26.253"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC = "prediction/output"

# Initialize MQTT Client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

# Read the Excel file with the predicted output
predicted_data = pd.read_excel(output_data_path, header=None)

# Convert the first row (predicted data) to a list
predicted_list = predicted_data.iloc[0].tolist()

# Convert the list to a comma-separated string
predicted_string = ','.join(map(str, predicted_list))

# Publish the predicted string without additional information
client.publish(MQTT_TOPIC, predicted_string)

# Disconnect the MQTT client
client.disconnect()
