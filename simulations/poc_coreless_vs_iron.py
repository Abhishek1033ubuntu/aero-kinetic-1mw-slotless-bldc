# ==============================================================================
# PROOF OF CONCEPT: Coreless DC Motor vs. Standard Iron-Core Baseline
# Dual-Mode Simulation (Motoring & Inverse EMF Generation)
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

class DCMotorModel:
    def __init__(self, name, Ra, K, I0, Tfric, k_iron=0.0):
        self.name = name
        self.Ra = Ra
        self.K = K
        self.I0 = I0
        self.Tfric = Tfric
        self.k_iron = k_iron

    def simulate_motor(self, V_supply, I_armature):
        Eb = V_supply - (I_armature * self.Ra)
        if Eb <= 0:
            return None
        
        omega = Eb / self.K
        rpm = omega * (60.0 / (2.0 * np.pi))
        
        P_elec_in = V_supply * I_armature
        P_cu = (I_armature ** 2) * self.Ra
        P_fric = self.Tfric * omega
        P_iron = self.k_iron * (omega ** 2)
        
        T_developed = self.K * I_armature
        T_loss = self.Tfric + (P_iron / omega if omega > 0 else 0)
        T_shaft = max(0.0, T_developed - T_loss)
        
        P_mech_out = T_shaft * omega
        eta = (P_mech_out / P_elec_in) * 100.0 if P_elec_in > 0 else 0.0
        
        return {
            'mode': 'Motor',
            'rpm': rpm,
            'omega': omega,
            'V_in': V_supply,
            'I_in': I_armature,
            'P_in': P_elec_in,
            'P_out': P_mech_out,
            'P_cu': P_cu,
            'P_fric': P_fric,
            'P_iron': P_iron,
            'efficiency': eta
        }

    def simulate_generator(self, rpm, I_load):
        omega = rpm * (2.0 * np.pi / 60.0)
        Eg = self.K * omega
        V_term = max(0.0, Eg - (I_load * self.Ra))
        
        P_elec_out = V_term * I_load
        P_cu = (I_load ** 2) * self.Ra
        P_fric = self.Tfric * omega
        P_iron = self.k_iron * (omega ** 2)
        
        T_elec = self.K * I_load
        T_drive = T_elec + self.Tfric + (P_iron / omega if omega > 0 else 0)
        
        P_mech_in = T_drive * omega
        eta = (P_elec_out / P_mech_in) * 100.0 if P_mech_in > 0 else 0.0
        
        return {
            'mode': 'Generator',
            'rpm': rpm,
            'omega': omega,
            'V_out': V_term,
            'I_out': I_load,
            'P_in': P_mech_in,
            'P_out': P_elec_out,
            'P_cu': P_cu,
            'P_fric': P_fric,
            'P_iron': P_iron,
            'efficiency': eta
        }

if __name__ == '__main__':
    baseline_motor = DCMotorModel(
        name="Standard 3V Iron-Core Motor",
        Ra=1.20, K=0.00200, I0=0.220, Tfric=0.00044, k_iron=1.2e-6
    )

    coreless_motor = DCMotorModel(
        name="Coreless NdFeB Redesign",
        Ra=0.50, K=0.00285, I0=0.032, Tfric=0.0000912, k_iron=0.0
    )

    V_test = 3.0
    I_test = 0.333

    m_res = coreless_motor.simulate_motor(V_supply=V_test, I_armature=I_test)
    g_res = coreless_motor.simulate_generator(rpm=m_res['rpm'], I_load=I_test)

    print("="*75)
    print(f"MILESTONE VERIFICATION: {coreless_motor.name}")
    print("="*75)
    print(f"Operating Speed (RPM)            | {m_res['rpm']:<18.1f} | {g_res['rpm']:<18.1f}")
    print(f"Armature Current (A)             | {m_res['I_in']:<18.3f} | {g_res['I_out']:<18.3f}")
    print(f"Conversion Efficiency (%)        | {m_res['efficiency']:<18.2f}% | {g_res['efficiency']:<18.2f}%")
    print("="*75)
