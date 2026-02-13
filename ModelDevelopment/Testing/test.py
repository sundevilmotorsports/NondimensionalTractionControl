import numpy as np
import tensorflow as tf
import time
import random

# --- 1. CONFIGURATION ---
MODEL_PATH = "../downloaded_models/model2.tflite"
TIRE_RADIUS = 0.2032

SCALER_MEAN = [19.630303697626477, -0.0005450365189715463, 59.8901043966616, 120.48587937144882, 59.00885398270266]
SCALER_SCALE = [8.66180044582203, 0.14460143717972843, 23.107923307685642, 57.82262435123635, 84.05533340078773]

# --- 2. LOAD MODEL ---
try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_idx = interpreter.get_input_details()[0]['index']
    output_idx = interpreter.get_output_details()[0]['index']
except Exception as e:
    print(f"Error: {e}")
    exit()

def run_inference(v, steer, temp, w, alpha):
    raw_input = np.array([v, steer, temp, w, alpha], dtype=np.float32)
    scaled_input = (raw_input - SCALER_MEAN) / SCALER_SCALE
    input_tensor = np.array([scaled_input], dtype=np.float32)
    interpreter.set_tensor(input_idx, input_tensor)
    interpreter.invoke()
    return interpreter.get_tensor(output_idx)[0][0]

# --- 3. THE RANDOMIZED LOOP ---
print(f"\n{'Scenario':<10} | {'TrueSlip':<8} | {'MathSlip':<8} | {'AI Slip':<8} | {'Error':<6} | {'Accel':<6} | {'VERDICT'}")
print("-" * 90)

try:
    while True:
        rand = random.random()
        
        # Base Conditions (Randomized)
        v_real = np.random.uniform(10.0, 35.0) 
        steer = np.random.uniform(-0.1, 0.1) # Slight steering
        temp = np.random.uniform(50.0, 80.0) # Variable temps
        
        # --- SCENARIO GENERATION ---
        if rand < 0.50:
            # NORMAL DRIVING (Random Grip)
            # Slips from 0.00 to 0.14 (Grip -> Peak Grip)
            scenario = "Normal"
            slip_actual = np.random.uniform(0.00, 0.14) 
            
            v_sensor = v_real
            w_sensor = v_real * (1 + slip_actual) / TIRE_RADIUS
            # Accel correlates with slip (0 to ~20 rad/s^2)
            alpha_sensor = slip_actual * 150.0 + np.random.normal(0, 5)

        elif rand < 0.80:
            # REAL SPIN (Random Severity)
            # Slips from 0.16 to 0.60 (Slip -> Massive Burnout)
            scenario = "SPIN!"
            slip_actual = np.random.uniform(0.16, 0.60)
            
            v_sensor = v_real
            w_sensor = v_real * (1 + slip_actual) / TIRE_RADIUS
            # High Accel (50 to 300 rad/s^2)
            alpha_sensor = slip_actual * 400.0 + np.random.normal(0, 20)

        else:
            # SENSOR FAILURE (Ghost Slip)
            scenario = "SensFail"
            slip_actual = np.random.uniform(0.00, 0.02) # TRUTH: Cruising
            
            # Speed Sensor drops by random 15% - 40%
            drop_factor = np.random.uniform(0.60, 0.85)
            v_sensor = v_real * drop_factor 
            
            # Physics: Real wheel speed (no slip) & Low Accel
            w_sensor = v_real * (1 + slip_actual) / TIRE_RADIUS 
            alpha_sensor = np.random.normal(0, 3.0) 

        # --- EXECUTE ---
        # 1. Dumb Math
        math_slip = (w_sensor * TIRE_RADIUS / v_sensor) - 1
        
        # 2. AI Prediction
        ai_slip = run_inference(v_sensor, steer, temp, w_sensor, alpha_sensor)
        
        # 3. Error
        error = abs(ai_slip - slip_actual)
        
        # 4. Verdict Logic
        verdict = "OK"
        if scenario == "SensFail":
            if math_slip > 0.15 and ai_slip < 0.15:
                verdict = "AI SAVED"
            elif ai_slip > 0.15:
                verdict = "AI FAILED"
        elif scenario == "SPIN!":
            if ai_slip > 0.15:
                verdict = "CATCH"
            else:
                verdict = "MISSED" 

        # --- PRINT ---
        print(f"{scenario:<10} | {slip_actual:<8.4f} | {math_slip:<8.4f} | {ai_slip:<8.4f} | {error:<6.4f} | {alpha_sensor:<6.0f} | {verdict}")
        
        time.sleep(0.15)

except KeyboardInterrupt:
    print("\n--- Test Stopped ---")