# ==============================================================================
# 5.0 kV HIGH-VOLTAGE 5-LEVEL ANPC FLIGHT PROFILE & THERMODYNAMIC SIMULATION
# System Power: 1.0 MW | Bus Voltage: 5.0 kV DC | Phase Current: 200 A RMS
# ==============================================================================

import numpy as np

# --- SYSTEM PHYSICAL PARAMETERS ---
V_DC_BUS = 5000.0             # DC Link Voltage (V)
P_RATED_W = 1.0e6             # Rated Motor Power (1.0 MW)
I_PHASE_RMS_1MW = 200.0       # Phase Current at 1.0 MW (A RMS)
R_PHASE_20C = 0.0084          # Phase Resistance (Ohms)
ALPHA_CU = 0.00393            # Resistance Temperature Coefficient (1/C)
MASS_MOTOR_KG = 54.0          # Total Engine Mass (kg)
MASS_CABLE_HARNESS_KG = 9.5   # 10m Feeder Harness Mass (kg)

# Feeder Cable Specifications
R_CABLE_10M = 0.0232          # Cable Resistance for 10m run (Ohms)

# Liquid Cooling System Parameters (50/50 Deionized Water/Glycol)
COOLANT_FLOW_LPS = 0.45       # Coolant Flow Rate (Liters/second)
COOLANT_HEAT_CAP = 3400.0     # Specific Heat Capacity (J/kg*K)
COOLANT_DENSITY = 1050.0      # Coolant Density (kg/m^3)
COOLANT_INLET_TEMP = 25.0     # Inlet Temperature (C)

# --- FLIGHT MISSION PROFILE DATA ---
flight_phases = [
    {"name": "Taxi & Warmup",       "time_s": 300,  "power_kw": +120.0, "alt_ft": 0,     "v_air_kts": 15},
    {"name": "Takeoff Burst",      "time_s": 60,   "power_kw": +1150.0,"alt_ft": 1000,  "v_air_kts": 140},
    {"name": "Climb Phase",        "time_s": 1200, "power_kw": +920.0, "alt_ft": 15000, "v_air_kts": 220},
    {"name": "High Cruise",        "time_s": 2400, "power_kw": +680.0, "alt_ft": 28000, "v_air_kts": 340},
    {"name": "Windmilling Descent","time_s": 1000, "power_kw": -285.0, "alt_ft": 10000, "v_air_kts": 260},
    {"name": "Touchdown Roll",     "time_s": 180,  "power_kw": -150.0, "alt_ft": 0,     "v_air_kts": 80}
]

print("=" * 85)
print("    5.0 kV / 200 A HIGH-VOLTAGE FLIGHT PROFILE & LOSS SIMULATION SUMMARY    ")
print("=" * 85)
print(f"{'Phase Name':<20} | {'Power (kW)':<10} | {'Mot/Gen Loss':<12} | {'Cable Loss':<10} | {'Inverter Loss':<13} | {'Net DC Power':<12} | {'System Eff':<10}")
print("-" * 85)

total_consumed_kwh = 0.0
total_recovered_kwh = 0.0

for phase in flight_phases:
    p_shaft_kw = phase["power_kw"]
    duration_h = phase["time_s"] / 3600.0
    
    # Calculate Phase Current Scaling relative to 1.0 MW baseline
    load_ratio = abs(p_shaft_kw) / 1000.0
    i_rms = I_PHASE_RMS_1MW * load_ratio
    
    # Winding Temperature Estimate under Direct Cooling
    if p_shaft_kw > 0:
        t_winding = COOLANT_INLET_TEMP + (load_ratio * 13.2)
    else:
        t_winding = COOLANT_INLET_TEMP + (load_ratio * 8.0)
        
    r_phase_temp = R_PHASE_20C * (1.0 + ALPHA_CU * (t_winding - 20.0))
    
    # Loss Vector Computations
    p_stator_loss_w = 3.0 * (i_rms ** 2) * r_phase_temp
    p_cable_loss_w = 3.0 * (i_rms ** 2) * R_CABLE_10M
    
    # 5-Level ANPC Inverter Switching & Conduction Losses
    if p_shaft_kw >= 0:
        p_inv_loss_w = (0.0012 * abs(p_shaft_kw * 1000.0)) + 180.0
        p_dc_net_kw = p_shaft_kw + ((p_stator_loss_w + p_cable_loss_w + p_inv_loss_w) / 1000.0)
        eff = (p_shaft_kw / p_dc_net_kw) * 100.0
        total_consumed_kwh += p_dc_net_kw * duration_h
    else:
        # Kinetic Regeneration Mode
        p_inv_loss_w = (0.0010 * abs(p_shaft_kw * 1000.0)) + 120.0
        p_dc_net_kw = p_shaft_kw + ((p_stator_loss_w + p_cable_loss_w + p_inv_loss_w) / 1000.0)
        eff = (abs(p_dc_net_kw) / abs(p_shaft_kw)) * 100.0
        total_recovered_kwh += abs(p_dc_net_kw) * duration_h

    print(f"{phase['name']:<20} | {p_shaft_kw:>10.1f} | {p_stator_loss_w/1000.0:>12.2f} kW | {p_cable_loss_w:>10.1f} W | {p_inv_loss_w/1000.0:>13.2f} kW | {p_dc_net_kw:>12.2f} | {eff:>9.2f}%")

print("=" * 85)
print(f"Total Flight Consumed Energy   : {total_consumed_kwh:.2f} kWh")
print(f"Total Descent Recovered Energy : {total_recovered_kwh:.2f} kWh")
print(f"Net Flight Battery Draw        : {total_consumed_kwh - total_recovered_kwh:.2f} kWh")
print(f"Net Mission Regeneration Ratio : {(total_recovered_kwh / total_consumed_kwh) * 100.0:.2f}%")
print("=" * 85)
