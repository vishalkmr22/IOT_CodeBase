import serial
import time
import pandas as pd

# Path to the CSV file
csv_file_path = "E:\IITK\sem-1\IOT\project\Crop_recommendation.csv"

# Load the CSV data
data_df = pd.read_csv(csv_file_path)

# Set up serial communication parameters
arduino_port = 'COM3'  # Update to your Arduino's port
baud_rate = 9600
timeout = 1  # Timeout in seconds

# Establish serial connection
ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)

# Allow some time for the connection to initialize
time.sleep(2)

# Iterate over each row in the dataframe and send values as a comma-separated string
for index, row in data_df.iterrows():
    # Extract the values of the row as a list, rounding floats to 2 decimal places
    values = [f"{value:.2f}" if isinstance(value, float) else str(value) for value in row.values]
    
    # Convert the list of values to a comma-separated string
    formatted_data = ",".join(values)
    
    # Send the formatted data to Arduino
    ser.write((formatted_data + '\n').encode('utf-8'))
    print(f"Sent data: {formatted_data}")

    # Delay of 10 seconds before sending the next row
    time.sleep(10)

# Close the serial connection
ser.close()
