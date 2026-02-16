import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# fsae constants from research - will replace with our cars values
CONSTANTS = {
    'dt': 0.01,
    'mass': 250.0,             # kg - taken from spreadsheet (with driver)
    'wheel_radius': 0.203,     # m - taken from spreadsheet
    'wheel_inertia': 0.25,     # kg-m^2 - total inertia of tire, rims, and other parts
    'cg_height': 0.2957,       # m - taken from spreadsheet
    'wheelbase': 1.53,         # m - taken from spreadsheet
    'drag_coeff': 1.19,        # taken from spreadsheet
    'gear_ratio': 11.5,        # based off final drive ratio (from spreadsheet), primary reduction, and selected gear ratios
    'max_torque': 50,          # Nm - taken from spreadsheet
    'peak_slip_angle': 0.12,   # theoretical
    'base_friction': 1.6,      # chosen friction coef
    'drivetrain_damping': 0.8, #common for FSAE cars

    # tire temp model components
    'tire_heat_coeff': 0.00175,         # friction -> heat conversion (FSAE compound)
    'tire_cool_coeff': 0.000068,        # convective cooling rate
    'tire_temp_max': 130.0,            # deg C max
    'optimal_tire_temp': 87.0,         # deg C peak grip (mid-range of 82-93°C)
}

# realistic driver throttle model based on current slip, target slip, and aggression
def get_driver_input(t, current_slip, target_slip, aggression):
    # repeating 15s cycle
    phase = int(t * 10) % 150 / 10.0

    # feedback gain scales continuously with aggression
    base_kp = 2.0 - aggression * 1.2 # more aggressive - lets slip build up, slower reaction to slip increase
    kp = base_kp
    base_tps = 0.0
    run_bias = np.random.normal(0.0, 0.02)

    # launch - high throttle (0-2s)
    if phase < 2.0:
        base_tps = 0.75 + aggression * 0.20
        kp = base_kp * 0.4
        if np.random.rand() < 0.05 + aggression * 0.08:
            base_tps = np.clip(base_tps + np.random.uniform(0.05, 0.15), 0, 1)

    # technical corners - oscillating throttle at mid-slip (2-11s)
    elif phase < 11.0:
        base_tps = 0.48 + 0.35 * np.sin(t * 6.0) + aggression * 0.10
        kp = base_kp
        if np.random.rand() < 0.40 + aggression * 0.10:
            base_tps = np.clip(base_tps + np.random.uniform(0.08, 0.18), 0, 1)

    # short straight (11-13s)
    elif phase < 13.0:
        base_tps = 0.75 + aggression * 0.15
        kp = base_kp * 1.2
        if np.random.rand() < 0.20 + aggression * 0.10:
            base_tps = np.clip(base_tps + np.random.uniform(0.05, 0.15), 0, 1)

    # coast / recovery for low slip samples (13-15s)
    else:
        base_tps = 0.0
        kp = 0.0

    # feedback correction for over/under-slipping (adjusting steering)
    error = current_slip - target_slip
    correction = error * kp * (1.5 - aggression * 0.7)  # less correction when aggressive
    final_tps = base_tps - correction

    # rare throttle bursts
    if np.random.rand() < 0.008 + aggression * 0.008:
        burst_strength = np.random.uniform(0.10, 0.30)
        final_tps = np.clip(final_tps + burst_strength, 0.0, 1.0)

    # launch boost
    if phase < 2.0 and np.random.rand() < 0.02 + aggression * 0.04:
        final_tps = np.clip(final_tps + np.random.uniform(0.10, 0.25), 0.0, 1.0)

    # progressive throttle reduction above optimal slip
    if current_slip > 0.15:
        scale = max(0.15, 1.0 - (current_slip - 0.15) * 2.2)
        final_tps *= scale

    # high slip trim (aggressive drivers cut back less)
    if current_slip > 0.25:
        reduction = 0.60 + (1.0 - aggression) * 0.25  # 0.60 (aggressive) to 0.85 (cautious)
        final_tps = np.clip(final_tps * (1.0 - reduction), 0.0, 1.0)

    # human foot noise & run bias
    foot_noise = np.random.normal(0, 0.032)
    final_tps = np.clip(final_tps + foot_noise + run_bias, 0.0, 1.0)

    # steering angle generation
    steer = np.sin(t * 1.0) * 0.2 + np.random.normal(0, 0.01)
    return final_tps, steer


# calculates normal load based on mass, cg_height and wheel base
def calculate_normal_load(ax, const):
    static_weight = (const['mass'] * 9.81) / 2
    transfer = (const['mass'] * ax * const['cg_height']) / const['wheelbase']
    normal_load = static_weight + transfer  # Rear load increases with accel
    return max(normal_load, 50.0)


# pacejka magic formula for distribution
def magic_formula(slip, load, steer_angle, peak_slip, current_mu):
    """
    Simplified Pacejka with:
      - Steering penalty
      - Post-peak grip drop-off (falling friction regime)
    """

    # steer penalty - models grip loss when increased steering
    steer_penalty = max(0.6, 1.0 - abs(steer_angle) * 1.0)

    # mu_peak
    mu_peak = current_mu * steer_penalty

    # )
    abs_slip = abs(slip)

    if abs_slip < peak_slip:
        # Rising grip region
        ratio = abs_slip / peak_slip
        force = load * mu_peak * np.sin(ratio * 1.57)
    else:
        # Post-peak: grip decays with increasing slip (falling friction)
        overshoot = abs_slip - peak_slip
        decay = max(0.55, 0.98 - 0.8 * overshoot)
        force = load * mu_peak * decay

    return force


# tire temp model for dynamic + realistic tire temps that affect grip
def update_tire_temp(temp, fx, slip, vx, ambient, const):
    heat_gen = abs(fx * slip) * const['tire_heat_coeff']  # heat generation
    cooling = (temp - ambient) * const['tire_cool_coeff'] * max(vx, 1.0) # cooling

    temp += (heat_gen - cooling) * const['dt']
    temp = np.clip(temp, ambient, const['tire_temp_max']) # clip to realistic temps

    return temp


# models tire grip based on temp - peaks at optimal temp
def tire_temp_grip_factor(temp, optimal_temp): 
    delta = temp - optimal_temp
    if delta < 0:
        # Cold: gradual loss (wider parabola)
        factor = 1.0 - 0.00015 * delta**2
    else:
        # Hot: sharper degradation
        factor = 1.0 - 0.0004 * delta**2

    return np.clip(factor, 0.4, 1.0)


# generates a single session - 40000 steps
def generate_session(session_id, steps=40000, vx_init=5.0, temp_init=30.0, ambient=25.0):
    c = CONSTANTS

    vx = vx_init
    omega = vx / c['wheel_radius']
    temp = temp_init
    ax_prev = 0.0
    last_slip = 0.0

    data_rows = []

    # randomized physical conditions (no driver styles)
    target_slip = np.random.uniform(0.06, 0.20)
    aggression = np.random.uniform(0.0, 1.0)
    surface_mu = c['base_friction']

    for i in range(steps):
        t = i * c['dt']

        # randomize conditions every ~25s segment
        if i % 2500 == 0:
            target_slip = np.random.uniform(0.08, 0.22)  # centered on 10-15% zone
            aggression = np.random.uniform(0.0, 1.0)     # continuous aggression
            surface_mu = np.random.uniform(1.4, 1.6)     # surface friction variation

        # Driver Input
        tps, steer = get_driver_input(t, last_slip, target_slip, aggression)

        # Drivetrain (Modeled)
        engine_torque = tps * c['max_torque']
        net_torque = engine_torque * c['gear_ratio']
        rpm = omega * c['gear_ratio'] * 9.54

        # Normal load with weight transfer
        static_weight = (c['mass'] * 9.81) / 2
        transfer = (c['mass'] * ax_prev * c['cg_height']) / c['wheelbase']
        fz = max(static_weight + transfer, 50.0)

        # Slip ratio
        denom = max(vx, 0.5)
        raw_slip = (omega * c['wheel_radius'] - vx) / denom
        true_slip = np.clip(max(0.0, raw_slip), 0.0, 1.0)
        last_slip = true_slip

        # Tire temp -> grip factor (using per-segment surface friction)
        temp_factor = tire_temp_grip_factor(temp, c['optimal_tire_temp'])
        effective_mu = surface_mu * temp_factor

        # Tire force (with post-peak drop-off)
        fx = magic_formula(true_slip, fz, steer, c['peak_slip_angle'], effective_mu)

        # 7. Vehicle dynamics integration
        drag = c['drag_coeff'] * vx**2
        ax = (fx - drag) / c['mass']
        vx += ax * c['dt']

        damping = omega * c['drivetrain_damping']
        alpha = (net_torque - fx * c['wheel_radius'] - damping) / c['wheel_inertia']
        omega += alpha * c['dt']

        vx = max(vx, 0.0)
        omega = max(omega, 0.0)
        ax_prev = ax

        # Update tire temperature
        temp = update_tire_temp(temp, fx, true_slip, vx, ambient, c)

        # Sensor readings (with noise)
        front_wheel_speed_mps = vx + np.random.normal(0, 0.1)

        # create df row + some val to model sensor noise
        row = {
            'wheel_omega': omega + np.random.normal(0, 0.5),
            'accel_x': ax + np.random.normal(0, 0.2),
            'tps': tps,
            'engine_rpm': rpm + np.random.normal(0, 50),
            'steering_angle': steer,
            'yaw_rate': (vx * np.tan(steer) / c['wheelbase']) + np.random.normal(0, 0.1),
            'tire_temp': temp + np.random.normal(0, 1.0),  # noisy temp sensor
            'front_wheel_speed': front_wheel_speed_mps,
            'TARGET_slip_ratio': true_slip
        }
        data_rows.append(row)

    return pd.DataFrame(data_rows)


# generates full dataset over multiple sessions
def generate_dataset(num_sessions=20, steps_per_session=40000):
    all_sessions = []

    for s in range(num_sessions):
        # Randomize initial conditions per session
        vx_init = np.random.uniform(3.0, 8.0)
        temp_init = np.random.uniform(50.0, 75.0)  # FSAE: after warmers / formation lap
        ambient = np.random.uniform(20.0, 35.0)

        print(f"  Session {s+1}/{num_sessions}: "
              f"v0={vx_init:.1f} m/s, T0={temp_init:.1f}°C, ambient={ambient:.1f}°C")

        df_session = generate_session(
            session_id=s,
            steps=steps_per_session,
            vx_init=vx_init,
            temp_init=temp_init,
            ambient=ambient
        )
        all_sessions.append(df_session)

    # Concatenate all sessions
    df = pd.concat(all_sessions, ignore_index=True)

    # Shuffle to break temporal ordering
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

    return df

# main
def main():
    print("=" * 50)
    print("GENERATING SYNTHETIC TRACTION CONTROL DATASET")
    print("=" * 50)

    df = generate_dataset(num_sessions=20, steps_per_session=40000)

    # --- Slip Distribution Report ---
    print("\n" + "-" * 40)
    print("SLIP DISTRIBUTION REPORT")
    print("-" * 40)
    s = df['TARGET_slip_ratio']
    b1 = len(s[(s >= 0.00) & (s < 0.05)])
    b2 = len(s[(s >= 0.05) & (s < 0.10)])
    b3 = len(s[(s >= 0.10) & (s < 0.15)])
    b4 = len(s[(s >= 0.15) & (s < 0.25)])
    b5 = len(s[(s >= 0.25)])

    total = len(df)
    print(f"Total samples: {total:,}")
    print(f"0-5%:   {b1/total*100:.1f}%")
    print(f"5-10%:  {b2/total*100:.1f}%")
    print(f"10-15%: {b3/total*100:.1f}% (GOAL: >15%)")
    print(f"15-25%: {b4/total*100:.1f}% (GOAL: >10%)")
    print(f"25%+:   {b5/total*100:.1f}%")
    print("-" * 40)

    # --- Tire Temperature Report ---
    print(f"\nTire Temp Range: {df['tire_temp'].min():.1f}°C - {df['tire_temp'].max():.1f}°C")
    print(f"Tire Temp Mean:  {df['tire_temp'].mean():.1f}°C")
    print(f"Tire Temp Std:   {df['tire_temp'].std():.1f}°C")

    # --- Save ---
    output_file = "synthetic_dataset_v3.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved {total:,} samples to {output_file}")

    # --- Visualization ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Slip distribution histogram
    axes[0].hist(df['TARGET_slip_ratio'], bins=50, color='purple', alpha=0.7)
    axes[0].axvline(0.10, color='red', linestyle='--', label='10%')
    axes[0].axvline(0.15, color='red', linestyle='--', label='15%')
    axes[0].axvline(0.25, color='orange', linestyle='--', label='25%')
    axes[0].set_title("Slip Ratio Distribution")
    axes[0].set_xlabel("Slip Ratio")
    axes[0].set_ylabel("Count")
    axes[0].legend()

    # 2. Tire temperature distribution
    axes[1].hist(df['tire_temp'], bins=50, color='orangered', alpha=0.7)
    axes[1].axvspan(82.0, 93.0, color='green', alpha=0.2, label='Optimal (82-93°C)')
    axes[1].set_title("Tire Temperature Distribution")
    axes[1].set_xlabel("Temperature (°C)")
    axes[1].set_ylabel("Count")
    axes[1].legend()

    # 3. Slip vs Tire Force (shows post-peak drop-off)
    sample = df.sample(min(5000, len(df)), random_state=42)
    axes[2].scatter(sample['TARGET_slip_ratio'], sample['accel_x'],
                    alpha=0.15, s=1, color='blue')
    axes[2].set_title("Slip Ratio vs Longitudinal Acceleration")
    axes[2].set_xlabel("Slip Ratio")
    axes[2].set_ylabel("Accel X (m/s²)")

    plt.tight_layout()
    plt.savefig("dataset_diagnostics_v3.png", dpi=150)
    plt.show()
    print("Saved diagnostic plots to dataset_diagnostics_v2.5.png")


if __name__ == "__main__":
    main()