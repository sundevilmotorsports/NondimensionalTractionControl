import numpy as np
import tensorflow as tf
import time
import random

# --- 1. CONFIGURATION ---
TIRE_RADIUS = 0.2032       
MODEL_PATH = "../downloaded_models/slip_ratio_model.tflite"

# Physics Constants
PAC_D_BASE = 1.6   
PAC_C = 1.5
PAC_B = 10.0
PAC_E = 0.5
WHEELBASE = 1.53

# Scaler Values
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
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_idx = interpreter.get_input_details()[0]['index']
output_idx = interpreter.get_output_details()[0]['index']

def run_ai_prediction(v, w, torque, load, temp, steer):
    mu_demand = (torque / TIRE_RADIUS) / load
    load_norm = load / 1000.0
    
    raw_vector = [v, w, mu_demand, load_norm, temp, steer]
    scaled_vector = []
    for i in range(6):
        val = (raw_vector[i] - SCALER_MEAN[i]) / SCALER_SCALE[i]
        scaled_vector.append(val)
        
    input_tensor = np.array([scaled_vector], dtype=np.float32)
    interpreter.set_tensor(input_idx, input_tensor)
    interpreter.invoke()
    return interpreter.get_tensor(output_idx)[0][0]

# --- 4. THE RANDOMIZED LOOP ---
print("\n--- LIVE RANDOM TEST: MATH vs AI ---")
print(f"{'Condition':<12} | {'True Slip':<10} | {'Math Slip':<10} | {'AI Slip':<10} | {'AI Error':<8} | {'VERDICT'}")
print("-" * 90)

try:
    while True:
        # Defaults
        v_real = np.random.uniform(15.0, 30.0)
        Fz = np.random.uniform(1900, 2200)
        temp = 60.0
        steer = 0.0
        
        # Randomly choose a Scenario
        rand = random.random()
        
        if rand < 0.60:
            # SCENARIO A: NORMAL DRIVING (Varied Grip)
            condition = "Normal"
            # Random slip between 0.00 and 0.12 (Grip to Edge of Grip)
            target_slip = np.random.uniform(0.00, 0.12)
            v_sensor = v_real
            
        elif rand < 0.80:
            # SCENARIO B: REAL BURNOUT (Varied Spin)
            condition = "REAL SPIN"
            # Random slip between 0.18 and 0.60 (Moderate to Massive Burnout)
            target_slip = np.random.uniform(0.18, 0.60)
            v_sensor = v_real
            
        else:
            # SCENARIO C: GHOST SLIP (Sensor Fail)
            condition = "SENS FAIL"
            # Actual reality is low slip (0.01 - 0.05)
            target_slip = np.random.uniform(0.01, 0.05)
            
            # Sensor Failure: Reads random 15% to 30% slower than reality
            fail_factor = np.random.uniform(0.70, 0.85)
            v_sensor = v_real * fail_factor

        # --- EXECUTE ---
        # 1. Physics Engine (Generates the Torque based on the TRUE slip)
        torque = calculate_physics_torque(target_slip, Fz, temp, steer)
        w_real = v_real * (1 + target_slip) / TIRE_RADIUS
        
        # 2. Dumb Math (Uses potentially broken sensor)
        math_slip_calc = (w_real * TIRE_RADIUS / v_sensor) - 1
        
        # 3. Smart AI (Uses Sensor + Torque context)
        ai_slip_pred = run_ai_prediction(v_sensor, w_real, torque, Fz, temp, steer)
        
        # 4. Error Calculation (AI vs The Truth)
        ai_error = abs(target_slip - ai_slip_pred)
        
        # --- JUDGEMENT ---
        # The Math is "wrong" if it deviates significantly from True Slip (happens in SENS FAIL)
        math_error = abs(target_slip - math_slip_calc)
        
        if condition == "SENS FAIL":
            if ai_error < 0.10 and math_error > 0.15:
                verdict = "AI SAVED CAR"
            else:
                verdict = "AI FAILED"
        elif condition == "REAL SPIN":
            if ai_slip_pred > 0.15:
                verdict = "CORRECT CATCH"
            else:
                verdict = "MISSED SPIN"
        else:
            verdict = "OK"

        # Warnings
        warn = ""
        if verdict == "AI SAVED CAR": warn = " <<< SENSOR FUSION"
        
        print(f"{condition:<12} | {target_slip:<10.4f} | {math_slip_calc:<10.4f} | {ai_slip_pred:<10.4f} | {ai_error:<8.4f} | {verdict}{warn}")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n--- Test Stopped ---")