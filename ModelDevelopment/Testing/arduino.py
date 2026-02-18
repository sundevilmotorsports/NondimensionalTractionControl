import numpy as np
import tensorflow as tf
import joblib
import serial 
import time    

ARDUINO_PORT = "/dev/cu.usbserial-[portnumber]" 
BAUD_RATE = 9600
NUM_FEATURES = 6 

scaler = joblib.load("scaler.pkl")

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
    print("Is the port correct? Is the Arduino plugged in?")
    exit()


print("Starting inference loop. Press Ctrl+C to stop.")

try:
    while True:
        if ser.in_waiting > 0:
            line_bytes = ser.readline()
            
            line_str = line_bytes.decode('utf-8').strip()

            try:
                features_list = [float(val) for val in line_str.split(',')]

                if len(features_list) == NUM_FEATURES:
                    
                    features_np = np.array(features_list, dtype=np.float32).reshape(1, -1)
                    
                    scaled_data = scaler.transform(features_np)

                    # Run inference
                    interpreter.set_tensor(input_details[0]['index'], scaled_data)
                    interpreter.invoke()
                    prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]

                    print(f"Prediction: {prediction:.5f}")
                
                else:
                    print(f"Warning: Got malformed data. Expected {NUM_FEATURES}, got {len(features_list)}. Data: '{line_str}'")

            except ValueError:
                print(f"Warning: Could not parse data: '{line_str}'")
            except Exception as e:
                print(f"An error occurred: {e}")

except KeyboardInterrupt:
    print("\nStopping script. Closing serial port.")
    ser.close()