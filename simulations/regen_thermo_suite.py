# ==============================================================================
# 1.0 MW INVERTED MOTOR + AEROSPACE KINETIC & THERMODYNAMIC REGENERATION
# Full Flight Profile Simulation with Standard Atmosphere Model
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

class AerospaceRegenSystem:
    def __init__(self):
        self.mass_kg = 88.0
        self.V_dc = 1000.0
        self.R_ref = 0.0084
        self.alpha_cu = 0.00393
        self.prop_radius = 1.85
        self.prop_area = np.pi * (self.prop_radius ** 2)
        self.C_p_regen = 0.32
        self.teg_efficiency_factor = 0.18
        self.coolant_flow_Lps = 1.85
        self.coolant_cp = 4184.0

    def isa_atmosphere(self, altitude_m):
        T0, p0, L, g, R = 288.15, 101325.0, 0.0065, 9.80665, 287.058
        T_amb = T0 - (L * altitude_m)
        p_amb = p0 * ((1 - (L * altitude_m / T0)) ** (g / (R * L)))
        rho_amb = p_amb / (R * T_amb)
        return T_amb - 273.15, rho_amb

    def evaluate_profile_step(self, altitude_ft, true_airspeed_kts, power_demand_kW, rpm):
        altitude_m = altitude_ft * 0.3048
        v_m_s = true_airspeed_kts * 0.514444
        T_amb_C, rho_amb = self.isa_atmosphere(altitude_m)
        
        R_actual = self.R_ref * (1.0 + self.alpha_cu * (T_amb_C - 20.0))
        omega = rpm * (2.0 * np.pi / 60.0)
        
        if power_demand_kW >= 0:
            P_mech = power_demand_kW * 1000.0
            I_rms = P_mech / (self.V_dc * np.sqrt(3) * 0.98)
            P_cu = 3.0 * (I_rms ** 2) * R_actual
            P_windage = 1.8e-6 * (omega ** 3)
            P_loss = P_cu + P_windage
            
            P_elec_in = P_mech + P_loss
            P_kin_regen = 0.0
            
            T_coil = T_amb_C + 25.0 + (P_loss / (self.coolant_flow_Lps * self.coolant_cp))
            dT = max(0.0, T_coil - T_amb_C)
            eta_carnot = dT / (T_coil + 273.15) if (T_coil + 273.15) > 0 else 0
            P_teg_regen = P_loss * eta_carnot * self.teg_efficiency_factor
            
            efficiency = (P_mech / P_elec_in) * 100.0
            net_power_kW = (P_elec_in - P_teg_regen) / 1000.0
            
        else:
            P_aero_harvest = 0.5 * rho_amb * self.prop_area * (v_m_s ** 3) * self.C_p_regen
            P_mech_gen = min(abs(power_demand_kW * 1000.0), P_aero_harvest)
            
            I_rms = P_mech_gen / (self.V_dc * np.sqrt(3) * 0.98)
            P_cu = 3.0 * (I_rms ** 2) * R_actual
            P_windage = 1.8e-6 * (omega ** 3)
            P_loss = P_cu + P_windage
            
            P_elec_gen = max(0.0, P_mech_gen - P_loss)
            P_kin_regen = P_elec_gen
            
            T_coil = T_amb_C + 15.0
            dT = max(0.0, T_coil - T_amb_C)
            eta_carnot = dT / (T_coil + 273.15)
            P_teg_regen = P_loss * eta_carnot * self.teg_efficiency_factor
            
            P_regen_total = P_kin_regen + P_teg_regen
            efficiency = (P_elec_gen / P_mech_gen * 100.0) if P_mech_gen > 0 else 99.2
            net_power_kW = - (P_regen_total / 1000.0)
            
        return {
            'T_amb_C': T_amb_C,
            'net_power_kW': net_power_kW,
            'P_kin_regen_kW': P_kin_regen / 1000.0,
            'P_teg_regen_kW': P_teg_regen / 1000.0,
            'efficiency': efficiency,
            'T_coil_C': T_coil
        }

if __name__ == '__main__':
    sim = AerospaceRegenSystem()
    res = sim.evaluate_profile_step(28000, 340, -280.0, 2100)
    print(f"Descent Regen Point: Net Power = {res['net_power_kW']:.1f} kW | Efficiency = {res['efficiency']:.2f}%")
