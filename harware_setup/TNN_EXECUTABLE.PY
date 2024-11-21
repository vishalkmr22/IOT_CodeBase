import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths for the model and data files
tflite_model_path = os.path.join(script_dir, "tnn_model.tflite")
data_file_path = os.path.join(script_dir, "/media/pavan/SUNIL/pavan/mqtt_sensor_data.xlsx")
output_data_path = os.path.join(script_dir, "predicted_row.xlsx")

# Print paths for debugging
print(f"Script directory: {script_dir}")
print(f"TensorFlow Lite model path: {tflite_model_path}")
print(f"Data file path: {data_file_path}")
print(f"Output file path: {output_data_path}")

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Read the input data
data = pd.read_excel(data_file_path,header=None)
data.columns = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Rainfall", "pH"]


# Define features
features = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Rainfall", "pH"]

# Calculate the average row
average_row = data[features].mean(axis=0)

# Scale the data
scaler = StandardScaler()
scaler.fit(data[features])
average_row_scaled = scaler.transform([average_row])

# Prepare the input for the model
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
input_data = np.array(average_row_scaled, dtype=np.float32)

# Run the model
interpreter.set_tensor(input_index, input_data)
interpreter.invoke()
predicted_output = interpreter.get_tensor(output_index)[0][0]

# Save the result to an Excel file
result = pd.DataFrame([average_row], columns=features)
with pd.ExcelWriter(output_data_path, engine='openpyxl') as writer:
    result.to_excel(writer, index=False, header=False)

# Confirm the script execution
print(f"Predicted result saved to {output_data_path}")
