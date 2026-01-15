import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# --- FSAE CONSTANTS (Customize these for your car) ---
TIRE_RADIUS = 0.2032       # Meters (8 inches)
MASS_CAR = 250.0           # kg (Car + Driver)
AERO_DOWNFORCE_COEFF = 1.5 # N per (m/s)^2 (Approx downforce)
CG_HEIGHT = 0.28           # Meters
WHEELBASE = 1.53           # Meters

# --- PACEJKA TIRE CONSTANTS (Hoosier-ish approximation) ---
# D: Peak Friction, C: Shape, B: Stiffness, E: Curvature
# These define the shape of the force curve
PAC_D_BASE = 1.6   # Base friction coefficient (sticky tires)
PAC_C = 1.5
PAC_B = 10.0
PAC_E = 0.5

def calculate_magic_formula(slip, Fz, temp, steer):
    """
    Calculates the longitudinal force (Fx) and required Torque based on physics.
    Includes Load Sensitivity, Thermal Sensitivity, and Friction Circle.
    """
    
    # 1. LOAD SENSITIVITY
    # Tires lose efficiency as load increases. 
    # Formula: mu = mu_base * (load_norm ^ sensitivity_power)
    # We normalize load against a reference (e.g., 1000N)
    load_sensitivity = (Fz / 1000.0) ** -0.1 
    
    # 2. THERMAL SENSITIVITY (Optimum at 60C)
    # Parabolic curve dropping off away from optimum
    temp_factor = 1.0 - 0.0004 * (temp - 60.0)**2
    
    # 3. COMBINED SLIP (Friction Circle)
    # Steering uses up available grip. 
    # Simplified Derating: max_long_friction decreases as steer increases
    # Assume 0.2 rad steering reduces longitudinal grip by ~15%
    steer_factor = np.cos(steer * 2.5) 
    
    # Calculate Effective Peak Friction (Mu)
    mu_peak = PAC_D_BASE * load_sensitivity * temp_factor * steer_factor
    
    # 4. MAGIC FORMULA (The Curve)
    # Fx = D * sin(C * atan(B*slip - E*(B*slip - atan(B*slip))))
    # Note: We use the absolute slip for calculation, then re-apply sign
    slip_abs = np.abs(slip)
    sign = np.sign(slip)
    
    # Standard Pacejka Expression
    Bx = PAC_B * slip_abs
    Ex = PAC_E
    term = Bx - Ex * (Bx - np.arctan(Bx))
    fx_normalized = np.sin(PAC_C * np.arctan(term))
    
    # Longitudinal Force
    Fx = Fz * mu_peak * fx_normalized * sign
    
    # 5. CONVERT TO TORQUE
    # Torque = Force * Radius
    # (Ignoring wheel inertia I*alpha for steady-state mapping)
    torque = Fx * TIRE_RADIUS
    
    return torque, mu_peak

def generate_fsae_dataset(num_samples=50000):
    print(f"Generating {num_samples} physics-accurate samples...")
    
    data = []
    
    for _ in range(num_samples):
        # --- 1. RANDOMIZE CONDITIONS ---
        
        # Velocity: 5 to 35 m/s
        v = np.random.uniform(5.0, 35.0)
        
        # Steering: -0.25 to 0.25 radians (approx 15 deg)
        steer = np.random.uniform(-0.25, 0.25)
        
        # Temp: 20C to 100C (Normal operating range)
        temp = np.random.uniform(20.0, 100.0)
        
        # Normal Force: Weight + Aero + Random Load Transfer noise
        # Base load on rear tires (approx 55% weight distrib)
        static_weight = (MASS_CAR * 9.81) * 0.55
        aero_load = AERO_DOWNFORCE_COEFF * (v**2)
        noise_load = np.random.normal(0, 100) # Bumps/Kerbs
        Fz = static_weight + aero_load + noise_load
        Fz = np.clip(Fz, 200.0, 3000.0) # Clamp physical limits
        
        # --- 2. RANDOMIZE RESULT (SLIP) ---
        # We sample the slip, then calculate the torque required to get there.
        # We bias heavily towards the "linear" region (0-15%) where you drive mostly,
        # but include enough "peak" and "spin" data (15-100%) for the AI to learn limits.
        
        if np.random.rand() < 0.7:
            slip = np.random.uniform(0.0, 0.20) # Normal driving
        else:
            slip = np.random.uniform(0.20, 1.0) # Burnouts / Spinups
            
        # --- 3. CALCULATE PHYSICS ---
        torque, available_mu = calculate_magic_formula(slip, Fz, temp, steer)
        
        # Add some noise to torque (measurement noise)
        torque_noise = np.random.normal(0, 5.0)
        torque_measured = np.clip(torque + torque_noise, 0, 600)
        
        # Calculate Wheel Speed from Slip
        # slip = (w*r - v) / v  => w = v(1+slip)/r
        w = v * (1 + slip) / TIRE_RADIUS
        
        data.append({
            'vehicle_speed': v,
            'wheel_angular_velocity': w,
            'wheel_torque': torque_measured,
            'normal_force': Fz,
            'tire_temp': temp,
            'steering_angle': steer,
            'slip_ratio': slip
        })
        
    return pd.DataFrame(data)

# --- EXECUTION ---
df_new = generate_fsae_dataset(50000)

# Verify Correlations (Should be non-zero now!)
print("\n--- NEW DATASET CORRELATIONS ---")
print(df_new.corr()['slip_ratio'].sort_values(ascending=False))

# --- PLOTTING PROOF ---
plt.figure(figsize=(14, 5))

# Plot 1: The Magic Formula Curve (Torque vs Slip)
plt.subplot(1, 2, 1)
plt.scatter(df_new['slip_ratio'], df_new['wheel_torque'], alpha=0.05, s=1)
plt.title("Generated Torque Curve (Physics-Based)")
plt.xlabel("Slip Ratio")
plt.ylabel("Torque (Nm)")
plt.xlim(0, 1.0)
plt.grid(True)

# Plot 2: Load Sensitivity Proof
# Filter for peak slip range (0.15 - 0.25) to see peak torque capacity
peak_data = df_new[(df_new['slip_ratio'] > 0.15) & (df_new['slip_ratio'] < 0.25)]
plt.subplot(1, 2, 2)
plt.scatter(peak_data['normal_force'], peak_data['wheel_torque'], c=peak_data['steering_angle'], cmap='coolwarm', alpha=0.5)
plt.colorbar(label='Steering Angle')
plt.title("Load Sensitivity: More Force = More Torque Capacity")
plt.xlabel("Normal Force (N)")
plt.ylabel("Torque at Peak Slip (Nm)")
plt.grid(True)

plt.show()

# --- SAVE ---
filename = "synthetic_dataset_final.csv"
df_new.to_csv(filename, index=False)
print(f"Dataset saved to {filename}")