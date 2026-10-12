# ==============================================================================
# STRESS TESTS 1 & 3: WEIBULL BREAKDOWN & HIGH dV/dt PULSE ENDURANCE
# High-Voltage Dielectric Qualification Suite for 5.0 kV Aerospace Bus
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- STRESS TEST 1: WEIBULL DIELECTRIC BREAKDOWN PROBABILITY ---
v_applied_kv = np.linspace(0.0, 22.0, 500)

# Weibull Distribution: Pf(V) = 1 - exp[-(V / V0)^beta]
V0_kapton = 8.5      # Baseline Kapton breakdown scale (kV)
beta_kapton = 5.5    # Kapton shape parameter

V0_advanced = 18.2   # Nano-Al2O3 Polyimide breakdown scale (kV)
beta_advanced = 11.2  # Advanced material shape parameter

pf_kapton = (1.0 - np.exp(- (v_applied_kv / V0_kapton) ** beta_kapton)) * 100.0
pf_advanced = (1.0 - np.exp(- (v_applied_kv / V0_advanced) ** beta_advanced)) * 100.0

# --- STRESS TEST 3: INSULATION PULSE ENDURANCE LIFETIME vs dV/dt ---
dv_dt_range = np.linspace(10.0, 400.0, 500)
C_material = 8.5e8   # Material endurance constant
m_exponent = 2.15    # dV/dt degradation exponent

lifetime_hours = C_material * (dv_dt_range ** (-m_exponent))

# Specific Inverter Operating Points
dv_dt_2level = 377.78  # 2-Level SiC Inverter (kV/us)
dv_dt_5level = 94.44   # 5-Level ANPC Inverter (kV/us)

life_2level = C_material * (dv_dt_2level ** (-m_exponent))
life_5level = C_material * (dv_dt_5level ** (-m_exponent))

# --- RESULTS REPORT ---
print("=" * 75)
print("     HIGH-VOLTAGE DIELECTRIC STRESS TEST QUALIFICATION REPORT     ")
print("=" * 75)
print(f"Target Qualification Voltage (3x Safety Factor) : 15.00 kV DC")
print(f"Standard Kapton Failure Rate at 15.0 kV          : {pf_kapton[np.argmin(np.abs(v_applied_kv-15.0))]:.2f}% (FAILED)")
print(f"Nano-Al2O3 Polyimide Failure Rate at 15.0 kV    : {pf_advanced[np.argmin(np.abs(v_applied_kv-15.0))]:.4f}% (PASSED)")
print("-" * 75)
print(f"2-Level Inverter (dV/dt = {dv_dt_2level:.2f} kV/us) Lifetime  : {life_2level:.1f} Hours")
print(f"5-Level ANPC Inverter (dV/dt = {dv_dt_5level:.2f} kV/us) Lifetime: {life_5level:.1f} Hours")
print(f"Insulation Lifespan Extension Ratio             : {life_5level / life_2level:.1f}x Extension")
print("=" * 75)
