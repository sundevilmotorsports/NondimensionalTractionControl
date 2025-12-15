import numpy as np
import tensorflow as tf
import joblib
import serial
import time
import pandas as pd 

# --- CONFIGURATION ---
ARDUINO_PORT = "/dev/cu.usbserial-[portnumber]" 
BAUD_RATE = 9600
NUM_COLUMNS = 7 

scaler = joblib.load("scaler.pkl")

feature_names = scaler.feature_names_in_
print("--- SCALER REQUIRES THIS EXACT ORDER ---")
print(feature_names)
print("----------------------------------------")


interpreter = tf.lite.Interpreter(model_path="../Downloaded_models/slip_ratio_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
    ser.flushInput() 
    print(f"Successfully connected to {ARDUINO_PORT}")
except serial.SerialException as e:
    print(f"Error: Could not open port {ARDUINO_PORT}. {e}")
    exit()

try:
    while True:
        if ser.in_waiting > 0:
            line_bytes = ser.readline()
            line_str = line_bytes.decode('utf-8').strip()

            try:
                features_list = [float(val) for val in line_str.split(',')]

                if len(features_list) == NUM_COLUMNS:
                    
                    features_for_model_list = features_list[0:6]
                    actual_slip_ratio = features_list[6] 
                    
                    features_df = pd.DataFrame(
                        [features_for_model_list], 
                        columns=feature_names
                    )

                    scaled_data = scaler.transform(features_df)

                    interpreter.set_tensor(input_details[0]['index'], scaled_data.astype(np.float32))
                    interpreter.invoke()
                    prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]

                    percent_diff = 0.0
                    
                    if abs(actual_slip_ratio) > 0.0001: 
                        percent_diff = (abs(actual_slip_ratio - prediction) / abs(actual_slip_ratio)) * 100
                    
                    print(f"Actual: {actual_slip_ratio:.5f}   Predicted: {prediction:.5f}  (Absolute Diff: {abs(prediction-actual_slip_ratio):5.3f}))   (% Diff: {percent_diff:5.1f}%)")
                
                else:
                    print(f"Warning: Got malformed data. Expected {NUM_COLUMNS}, got {len(features_list)}. Data: '{line_str}'")

            except ValueError:
                print(f"Warning: Could not parse data: '{line_str}'")
            except Exception as e:
                print(f"An error occurred: {e}")

except KeyboardInterrupt:
    print("\nStopping script. Closing serial port.")
    ser.close()