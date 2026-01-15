import numpy as np
import tensorflow as tf
import joblib
import time
import pandas as pd 
import random
import math

# --- CONFIGURATION ---
# No Arduino port needed anymore
TIRE_RADIUS = 0.2032 # meters (approx 8 inches)
SLEEP_TIME = 0.5     # Seconds between simulated readings

# Load Assets
scaler = joblib.load("scaler.pkl")
feature_names = scaler.feature_names_in_

print("--- SCALER REQUIRES THIS EXACT ORDER ---")
print(feature_names)
print("----------------------------------------")

interpreter = tf.lite.Interpreter(model_path="../Downloaded_models/slip_ratio_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = input_details[0]['index']
output_index = output_details[0]['index']

import random

# ... (Previous setup code: imports, scaler load, interpreter setup) ...

print("\n--- STARTING SIMULATION (ACCELERATION ONLY) ---")
print(f"{'Actual Slip':<12} | {'Predicted':<12} | {'Diff':<10} | {'% Error':<10}")
print("-" * 55)

try:
    while True:
        # --- 1. GENERATE POSITIVE-ONLY "ACCELERATION" DATA ---
        
        # Vehicle Speed: 5 to 30 m/s (Always positive)
        sim_speed  = random.uniform(5.0, 30.0)
        
        # Target Slip: Generate only POSITIVE slip (0.0 to 0.4)
        # 0.0 = Grip, 0.4 = Massive burnout
        sim_slip   = random.uniform(0.0, 0.4) 
        
        # Calculate Wheel Speed based on positive slip
        # Formula: w = v(1 + slip) / r
        sim_w_vel  = (sim_speed * (1 + sim_slip)) / TIRE_RADIUS
        
        # Torque: Positive only (Drive torque)
        sim_torque = random.uniform(10.0, 250.0) 
        
        # Normal Force: Positive (Downforce + Weight)
        sim_norm_f = random.uniform(800.0, 1400.0)
        
        # Temp: Positive
        sim_temp   = random.uniform(40.0, 80.0)
        
        # Steering: Keep absolute (0 to 0.5 rad) to avoid confusion, 
        # or keep +/- if your model expects left/right turns. 
        # For now, let's assume absolute steering magnitude:
        sim_steer  = abs(random.uniform(-0.1, 0.1))

        # --- 2. CALCULATE PHYSICS TRUTH ---
        # (w*r - v) / v
        actual_slip_calc = ((sim_w_vel * TIRE_RADIUS) - sim_speed) / sim_speed

        # FORCE POSITIVE: In case floating point math gives -0.000001
        actual_slip_calc = max(0.0, actual_slip_calc)

        # Pack into list [speed, w, torque, norm, temp, steer, slip]
        features_list = [sim_speed, sim_w_vel, sim_torque, sim_norm_f, sim_temp, sim_steer, actual_slip_calc]

        # --- 3. PREDICT ---
        features_for_model = features_list[0:6]
        
        # Create DataFrame with correct column names
        features_df = pd.DataFrame([features_for_model], columns=feature_names)

        # Scale inputs (NOTE: Scaled values CAN be negative, this is normal for Neural Nets)
        scaled_data = scaler.transform(features_df)

        interpreter.set_tensor(input_index, scaled_data.astype(np.float32))
        interpreter.invoke()
        
        # Get result and clamp it to be positive (Physical constraint)
        raw_prediction = interpreter.get_tensor(output_index)[0][0]
        prediction = max(0.0, float(raw_prediction))

        # --- 4. CALCULATE ERROR ---
        diff = abs(actual_slip_calc - prediction)
        
        percent_err = 0.0
        # Avoid divide by zero if slip is exactly 0
        if actual_slip_calc > 0.001:
            percent_err = (diff / actual_slip_calc) * 100

        # --- 5. PRINT ---
        # Using simple floats to avoid the formatting error you saw earlier
        print(f"{actual_slip_calc:<12.5f} | {prediction:<12.5f} | {diff:<10.5f} | {percent_err:5.1f}%")
        
        time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
    print("\nStopping simulation.")