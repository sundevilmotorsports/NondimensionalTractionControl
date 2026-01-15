import numpy as np
import tensorflow as tf
import time
import random

# --- 1. CONFIGURATION ---
TIRE_RADIUS = 0.2032       
MODEL_PATH = "../downloaded_models/slip_ratio_model.tflite"

# Physics Constants (Must match Training!)
PAC_D_BASE = 1.6   
PAC_C = 1.5
PAC_B = 10.0
PAC_E = 0.5

# Scaler Values (As verified)
SCALER_MEAN = [20.034541014154737, 123.2994466292431, 0.8804743504359366, 2.0565089501338054, 60.171122645472714, -0.0005658642720516501]
SCALER_SCALE = [8.704530897784993, 60.44627874838102, 0.341922541515805, 0.5255823686244583, 23.080190741648874, 0.14413750764623715]

# --- 2. PHYSICS ENGINE ---
def calculate_physics_torque(slip, Fz, temp, steer):
    load_sensitivity = (Fz / 1000.0) ** -0.1 
    temp_factor = 1.0 - 0.0004 * (temp - 60.0)**2
    steer_factor = np.cos(steer * 2.5) 
    mu_peak = PAC_D_BASE * load_sensitivity * temp_factor * steer_factor
    
    slip_abs = np.abs(slip)
    sign = np.sign(slip)
    Bx = PAC_B * slip_abs
    Ex = PAC_E
    term = Bx - Ex * (Bx - np.arctan(Bx))
    fx_normalized = np.sin(PAC_C * np.arctan(term))
    
    Fx = Fz * mu_peak * fx_normalized * sign
    return Fx * TIRE_RADIUS

# --- 3. TFLITE SETUP ---
print("Loading TFLite Model...")
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = input_details[0]['index']
output_index = output_details[0]['index']

def run_ai_prediction(v, w, torque, load, temp, steer):
    mu_demand = (torque / TIRE_RADIUS) / load
    load_norm = load / 1000.0
    
    raw_vector = [v, w, mu_demand, load_norm, temp, steer]
    
    scaled_vector = []
    for i in range(6):
        val = (raw_vector[i] - SCALER_MEAN[i]) / SCALER_SCALE[i]
        scaled_vector.append(val)
        
    input_tensor = np.array([scaled_vector], dtype=np.float32)
    interpreter.set_tensor(input_index, input_tensor)
    interpreter.invoke()
    return interpreter.get_tensor(output_index)[0][0]

# --- 4. INFINITE TEST LOOP ---
print("\n--- INFINITE STREAM: TRUE vs AI ---")
print(f"{'TRUE Slip':<12} | {'AI Slip':<12} | {'ERROR':<10} | {'Scenario'}")
print("-" * 60)

try:
    while True:
        # 1. Randomize Environment
        v = np.random.uniform(10.0, 35.0)
        Fz = np.random.uniform(1800, 2300)
        temp = np.random.uniform(55, 65)
        steer = np.random.uniform(-0.1, 0.1)
        
        # 2. Pick a Scenario (Weighted randomness)
        # 60% Grip (Driving), 20% Peak (Cornering), 20% Spin (Burnout)
        rand_val = random.random()
        if rand_val < 0.6:
            target_slip = np.random.uniform(0.00, 0.10)
            scenario = "Grip"
        elif rand_val < 0.8:
            target_slip = np.random.uniform(0.10, 0.18)
            scenario = "Peak"
        else:
            target_slip = np.random.uniform(0.18, 0.45)
            scenario = "Spin"
            
        # 3. Calculate Physics Truth
        torque_input = calculate_physics_torque(target_slip, Fz, temp, steer)
        w_input = v * (1 + target_slip) / TIRE_RADIUS
        
        # 4. Run AI
        predicted_slip = run_ai_prediction(v, w_input, torque_input, Fz, temp, steer)
        
        # 5. Print
        error = abs(target_slip - predicted_slip)
        
        # Color coding for terminal (Optional, works in most terminals)
        # Green for low error, Red for high error
        if error < 0.03:
            status = " OK "
        else:
            status = "WARN"

        print(f"{target_slip:<12.4f} | {predicted_slip:<12.4f} | {error:<10.4f} | {scenario:<5} {status}")
        
        # Small delay so you can read it
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n--- Test Stopped by User ---")