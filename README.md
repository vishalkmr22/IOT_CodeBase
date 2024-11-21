# Smart IoT-Based Agricultural Recommendation System

A smart, cost-efficient IoT-based system for agricultural recommendation that integrates hardware, machine learning models, and a user-friendly web interface. The system predicts fertilizer recommendations and crop features using real-time or simulated data and provides robust insights to enhance agricultural productivity.

---

## Features
- Operates independently of sensors using **TNN-predicted rows**.
- Employs **Decision Tree**, **Random Forest**, and **TNN** for high-accuracy predictions.
- Uses **MQTT protocol** for real-time data exchange between hardware components.
- Includes a React-based web interface for interactive data visualization and system control.
- Optimized for **IoT devices** with lightweight TFLite models for efficient deployment.

---

## Hardware Requirements
- **Raspberry Pi** (Model 3 or newer)
- **NodeMCU (ESP8266)** for Wi-Fi communication
- **Arduino Uno** for simulated sensor data
- USB cables and power supply
- Breadboard and jumper wires (for hardware connections)

---

## Software Requirements
- Python 3.8 or newer
- Required Python libraries:
  - `paho-mqtt`
  - `pandas`
  - `openpyxl`
  - `tensorflow`
  - `flask`
- React.js (Node.js and npm for frontend setup)
- MQTT Broker (e.g., Mosquitto)

---

## Setup Instructions

### 1. Install MQTT Broker on Raspberry Pi
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto

### 2. Install Python Dependencies
pip install paho-mqtt pandas openpyxl tensorflow flask

## 3. Set Up Hardware
Connect Arduino Uno to NodeMCU via serial communication:
- **TX (Arduino)** → **RX (NodeMCU)**
- **RX (Arduino)** → **TX (NodeMCU)**
- Connect **GND** pins of both devices.

Refer to the `hardware_setup_pic.jpeg` for the physical connections.

---

## 4. Program Hardware
1. Upload the provided Arduino code (`send_data_to_nodemcu.ino`) to the Arduino Uno.
2. Upload the NodeMCU code (`mqtt_pub.ino`) to NodeMCU.

---

## 5. **Run MQTT Subscriber**
Run the Python script to subscribe to the MQTT topic and store predictions:

```bash
python3 mqtt.py
---

## 6. **Train and Deploy Machine Learning Models**

### Train the models using the dataset:
```bash
python3 fertilizer_recommendation_with_metrics.py

## 7.Convert the TNN model to TFLite for efficient deployment:

python3 model.py

** 8.Deploy the TFLite model on Raspberry Pi  **

# Set Up Web Interface

## 9. Navigate to the `web-interface` folder:
   ```bash
   cd web-interface


**Acknowledgments**

Special thanks to the open-source community for providing tools and libraries.
Inspired by advancements in IoT and machine learning for agriculture.

**Authors**
Vishal Kumar
Abhishek Kumar
Pavan kumar Ponnaganti
