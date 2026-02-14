import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CONSTANTS
TIRE_RADIUS = 0.2032       
MASS_CAR = 250.0           
AERO_DOWNFORCE_COEFF = 1.5 
WHEEL_INERTIA = 0.8        

# PACEJKA PHYSICS
PAC_D_BASE = 1.6   
PAC_C = 1.5
PAC_B = 10.0
PAC_E = 0.5

def calculate_magic_formula(slip, Fz, temp, steer):
    # Standard Physics Calculation
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
    road_torque = Fx * TIRE_RADIUS
    return road_torque, mu_peak

def generate_mixed_dataset(total_samples=50000):
    data = []
    
    for i in range(total_samples):
        # --- 1. THE PHYSICS (Ground Truth) ---
        v_true = np.random.uniform(5.0, 35.0)
        steer_true = np.random.uniform(-0.25, 0.25)
        temp_true = np.random.uniform(20.0, 100.0)
        
        # Load
        static_weight = (MASS_CAR * 9.81) * 0.55
        aero_load = AERO_DOWNFORCE_COEFF * (v_true**2)
        Fz = static_weight + aero_load + np.random.normal(0, 50)
        Fz = np.clip(Fz, 200.0, 3000.0)
        
        # Slip Target
        if np.random.rand() < 0.6:
            slip_target = np.random.uniform(0.0, 0.15) # Grip
        else:
            slip_target = np.random.uniform(0.15, 0.80) # Spin
            
        # Resulting Motion
        w_true = v_true * (1 + slip_target) / TIRE_RADIUS
        
        # Acceleration Calculation
        road_torque, _ = calculate_magic_formula(slip_target, Fz, temp_true, steer_true)
        driver_excess = np.random.normal(0, 10.0)
        if slip_target > 0.15: driver_excess += np.random.uniform(50, 200)
        
        net_torque = (road_torque + driver_excess) - road_torque
        alpha_true = net_torque / WHEEL_INERTIA

        # Generate noisy data to account for actual sensor noise
        is_noisy = i > (total_samples / 1.5) # 1/3 noisy data
        
        if is_noisy:
            # Apply Sensor Noise
            v_input = v_true + np.random.normal(0, 0.3)
            steer_input = steer_true + np.random.normal(0, 0.02)
            temp_input = temp_true + np.random.normal(0, 2.0)
            w_input = w_true + np.random.normal(0, 1.5)
            
            # Heavy Accel Noise
            alpha_noise = np.random.normal(0, 12.0)
            # Occasional Spike (10% chance)
            if np.random.rand() < 0.10: 
                alpha_noise += np.random.choice([-40, 40])
            alpha_input = alpha_true + alpha_noise
            
        else:
            # CLEAN DATA (Perfect Sensors)
            v_input = v_true
            steer_input = steer_true
            temp_input = temp_true
            w_input = w_true
            alpha_input = alpha_true

        data.append({
            'vehicle_speed': v_input,
            'steering_angle': steer_input,
            'tire_temp': temp_input,
            'wheel_rotational_speed': w_input,
            'wheel_rotational_acceleration': alpha_input,
            'slip_ratio': slip_target,
            'is_noisy': int(is_noisy) # Just for debugging
        })
        
    return pd.DataFrame(data)

df_mixed = generate_mixed_dataset(50000)

# Verify the mix
print(df_mixed['is_noisy'].value_counts())

# Save
df_mixed.to_csv("synthetic_dataset_test.csv", index=False)

# Visualize the difference
plt.figure(figsize=(10, 6))
plt.scatter(df_mixed[df_mixed['is_noisy']==0]['wheel_rotational_acceleration'], 
            df_mixed[df_mixed['is_noisy']==0]['slip_ratio'], 
            alpha=0.1, s=1, color='blue', label='Clean Data')

plt.scatter(df_mixed[df_mixed['is_noisy']==1]['wheel_rotational_acceleration'], 
            df_mixed[df_mixed['is_noisy']==1]['slip_ratio'], 
            alpha=0.1, s=1, color='red', label='Noisy Data')

plt.title("Clean vs. Noisy Acceleration Data")
plt.xlabel("Wheel Acceleration (rad/s^2)")
plt.ylabel("Slip Ratio")
plt.legend()
plt.show()