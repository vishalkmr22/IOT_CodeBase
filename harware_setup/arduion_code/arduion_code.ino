void setup() {
    Serial.begin(9600);   // Initialize Serial communication to NodeMCU
}

void loop() {
    // Check if there is data available from the Python script
    if (Serial.available() > 0) {
        // Read the incoming data from Python
        String receivedData = Serial.readStringUntil('\n');

        // Send the received data to NodeMCU
        Serial.println(receivedData);
    }

    // Add a small delay to avoid overwhelming the serial buffer
    delay(10000);
}
