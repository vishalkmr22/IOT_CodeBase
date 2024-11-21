import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

data = pd.read_excel("new.xlsx")

features = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Rainfall", "pH"]
X = data[features]
y = data["Fertilizer"]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = Sequential([
    Dense(10, input_shape=(6,), activation='relu'),  
    Dense(5, activation='relu'),                      
    Dense(1, activation='linear')                   
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_scaled, y_encoded, epochs=10, verbose=1)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

tflite_model_path = "tnn_model.tflite"
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)
print(f"TFLite model saved to {tflite_model_path}")
