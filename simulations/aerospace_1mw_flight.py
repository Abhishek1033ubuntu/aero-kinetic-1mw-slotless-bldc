# ==============================================================================
# AEROSPACE HYBRID AIRCRAFT FLIGHT PROFILE SIMULATION
# Propulsion System: 1.0 MW Inverted Slotless/Coreless Electric Motor
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

class AerospaceMotor1MW:
    def __init__(self):
        self.mass_kg = 88.0                   # Total Motor Mass (kg)
        self.V_dc = 1000.0                    # Bus Voltage (V)
        self.R_phase = 0.0084                 # Phase Resistance at 65°C (Ohms)
        self.K_e = 3.00                       # Back-EMF Constant (V*s/rad)
        self.P_rated_kW = 1000.0              # Continuous Rating (kW)
        self.P_peak_kW = 1200.0               # Peak Rating (kW)
        
        self.T_fric_base = 1.20               # Mechanical bearing drag (Nm)
        self.k_windage = 1.8e-6               # Aerodynamic rotor fin coefficient
        self.coolant_flow_Lps = 1.85          # Coolant flow (L/s)
        self.coolant_cp = 4184.0              # Specific heat capacity (J/kg*K)
        
    def evaluate_flight_point(self, power_req_kW, rpm, ambient_temp_C=20.0):
        omega = rpm * (2.0 * np.pi / 60.0)
        P_mech_out = power_req_kW * 1000.0
        
        I_rms = P_mech_out / (self.V_dc * np.sqrt(3) * 0.98)
        
        P_cu = 3.0 * (I_rms ** 2) * self.R_phase
        P_fric = self.T_fric_base * omega
        P_windage = self.k_windage * (omega ** 3)
        P_iron = 0.0
        
        P_total_loss = P_cu + P_fric + P_windage + P_iron
        P_elec_in = P_mech_out + P_total_loss
        
        eta_motor = (P_mech_out / P_elec_in) * 100.0 if P_elec_in > 0 else 0.0
        
        coolant_mass_flow = self.coolant_flow_Lps
        delta_T_coolant = P_total_loss / (coolant_mass_flow * self.coolant_cp)
        winding_temp_C = ambient_temp_C + 25.0 + delta_T_coolant
        
        return {
            'rpm': rpm,
            'P_mech_kW': power_req_kW,
            'P_elec_kW': P_elec_in / 1000.0,
            'I_rms': I_rms,
            'P_loss_kW': P_total_loss / 1000.0,
            'efficiency': eta_motor,
            'winding_temp_C': winding_temp_C
        }

if __name__ == '__main__':
    aero_motor = AerospaceMotor1MW()
    res = aero_motor.evaluate_flight_point(1150.0, 3100)
    print(f"1.0 MW Motor Takeoff Rating: {res['P_elec_kW']:.1f} kW Elec In | {res['efficiency']:.2f}% Eff | {res['winding_temp_C']:.1f}°C")
