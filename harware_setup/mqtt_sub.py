import paho.mqtt.client as mqtt
import time
import pandas as pd

# Initialize a list to store sensor data rows
mqtt_data = []

# Function to save data to an Excel file
def save_to_excel():
    # Check if there's any data to save
    if mqtt_data:
        # Convert the list of data into a DataFrame, automatically managing columns
        df = pd.DataFrame(mqtt_data)
        df.to_excel("mqtt_sensor_data.xlsx", index=False, header=False)  # Do not add headers
        print("Sensor data successfully saved to Excel.")
    else:
        print("No data to save.")

# Connection callback
def on_connect(client, userdata, flags, rc):
    global is_connected
    is_connected = rc == 0  # Check connection status
    if is_connected:
        subscribe_to_topics(client)
        print("Successfully connected to the MQTT broker.")
    else:
        print(f"Connection failed with code {rc}")

# Disconnection callback
def on_disconnect(client, userdata, rc):
    global is_connected
    is_connected = False
    print("Disconnected from the MQTT broker.")

# Callback functions for different messages
def on_esp8266_sensor1_message(client, userdata, message):
    decoded_message = message.payload.decode('utf-8')
    print(f"Received data from ESP8266 sensor1: {decoded_message}")

    # Split the received comma-separated string into a list
    data_row = decoded_message.split(",")  
    
    # Append the split data as a new row
    mqtt_data.append(data_row)

    # Save to Excel
    save_to_excel()

def on_esp8266_sensor2_message(client, userdata, message):
    decoded_message = message.payload.decode('utf-8')
    print(f"Received data from ESP8266 sensor2: {decoded_message}")

    # Split the comma-separated values
    data_row = decoded_message.split(",")
    
    # Append to data list
    mqtt_data.append(data_row)
    save_to_excel()

def on_rpi_broadcast_message(client, userdata, message):
    decoded_message = message.payload.decode('utf-8')
    print(f"Received Raspberry Pi broadcast: {decoded_message}")

    # Split the comma-separated values
    data_row = decoded_message.split(",")
    
    # Append to data list
    mqtt_data.append(data_row)
    save_to_excel()

# Subscription function
def subscribe_to_topics(client):
    client.subscribe("esp8266/sensor1")
    client.subscribe("rpi/broadcast")
    client.subscribe("esp8266/sensor2")

# MQTT Client setup
mqtt_client = mqtt.Client(client_id="raspberry_mqtt_client")
is_connected = False

# Setting up callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.message_callback_add('esp8266/sensor1', on_esp8266_sensor1_message)
mqtt_client.message_callback_add('esp8266/sensor2', on_esp8266_sensor2_message)
mqtt_client.message_callback_add('rpi/broadcast', on_rpi_broadcast_message)

# Connect to the MQTT broker (localhost in this case)
mqtt_client.connect('127.0.0.1', 1883)

# Start the MQTT client loop in a separate thread
mqtt_client.loop_start()

# Subscribe to topics
subscribe_to_topics(mqtt_client)

print("MQTT client setup completed... Waiting for messages...")

# Main loop to maintain connection
try:
    while True:
        time.sleep(5)
        if not is_connected:
            print("Attempting to reconnect to the MQTT broker...")
except KeyboardInterrupt:
    print("Shutting down...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
