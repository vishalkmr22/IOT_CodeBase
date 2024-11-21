#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi and MQTT details
const char* ssid = "__pavan__";
const char* password = "Pavan@2002";
const char* mqtt_server = "192.168.26.253";

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

String receivedData = "";  // String to store incoming data

void setup_wifi() {
  WiFi.begin(ssid, password);
  int c = 0;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    delay(1000);
    c++;
    if (c > 10) {
        ESP.restart();  // Restart ESP if connection takes too long
    }
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void connect_mqttServer() {
  while (!client.connected()) {
    if (WiFi.status() != WL_CONNECTED) {
      setup_wifi();
    }

    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266_client1")) {
      Serial.println("connected to MQTT broker");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" trying again in 2 seconds");
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud rate
  setup_wifi();
  client.setServer(mqtt_server, 1883);  // Set MQTT broker and port
}

void loop() {
  if (!client.connected()) {
    connect_mqttServer();
  }
  client.loop();

  // Check if data is available to read
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == '\n') {
      Serial.println("Received: " + receivedData);
      
      // Publish received data to the MQTT topic
      if (receivedData.length() > 0) {  // Ensure data is not empty
        client.publish("esp32/sensor1", receivedData.c_str());  // Publish data
        Serial.println("Published to MQTT: " + receivedData);
      }
      receivedData = "";  // Clear the string for new data
    } else {
      receivedData += data;  // Append character to the receivedData string
    }
  }
}
