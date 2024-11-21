import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

tflite_model_path = "tnn_model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

data = pd.read_excel("1.xlsx") 

features = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Rainfall", "pH"]

average_row = data[features].mean(axis=0)

scaler = StandardScaler()
scaler.fit(data[features]) 
average_row_scaled = scaler.transform([average_row])

input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
input_data = np.array(average_row_scaled, dtype=np.float32)

interpreter.set_tensor(input_index, input_data)
interpreter.invoke()
predicted_output = interpreter.get_tensor(output_index)[0][0]

result = pd.DataFrame([average_row], columns=features) 

output_data_path = "predicted_row.xlsx"
with pd.ExcelWriter(output_data_path, engine='openpyxl') as writer:
    result.to_excel(writer, index=False, header=False)  

print(f"Predicted result saved to {output_data_path}")
