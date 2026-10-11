/**
 * @file   foc_firmware.c
 * @brief  Aerospace-Grade FOC, DPCC, and Regeneration ISR for 1.0 MW Inverted Motor
 * @target Dual-Core DSP / ARM Cortex-R5F / Colab C-HIL Wrapper
 */

#include <math.h>
#include <stdint.h>
#include <stdio.h>

// --- PHYSICAL MOTOR & SYSTEM CONSTANTS ---
#define PHASE_INDUCTANCE_H     42.0e-6f    // 42 uH Phase Inductance
#define PHASE_RESISTANCE_OHM   0.0084f     // 8.4 mOhm Stator Resistance
#define FLUX_LINKAGE_WB        0.00318f    // N55SH Rotor Flux Linkage
#define POLE_PAIRS             6           // 12-Pole Rotor Configuration
#define TS_CURRENT_LOOP_SEC    0.000020f   // 50 kHz Current Loop (20 microseconds)
#define MAX_IQ_RAMP_A_PER_SEC  500000.0f   // Current Rate Limiter (dI/dt)

// --- SYSTEM STATES & TELEMETRY STRUCT ---
typedef struct {
    float i_phase_u;       // Measured Phase U Current (A)
    float i_phase_v;       // Measured Phase V Current (A)
    float theta_elec;      // Rotor Electrical Angle (rad)
    float omega_elec;      // Rotor Electrical Velocity (rad/s)
    float v_dc_bus;        // Measured DC Bus Voltage (V)
    
    float id_ref;          // Direct Axis Reference (0.0 A for MTPA)
    float iq_ref_target;   // Demanded Quadrature Current (A)
    float iq_ref_actual;   // Rate-Limited Quadrature Current (A)
    
    float prop_pitch_beta; // Measured Propeller Blade Pitch Angle (deg)
    uint8_t regen_enable;  // Regeneration Flag

    // Output Command Signals
    float vd_cmd;          // Calculated Direct Axis Voltage (V)
    float vq_cmd;          // Calculated Quadrature Axis Voltage (V)
    uint8_t supercap_gate; // Overvoltage Router Gate
} MotorController_t;

static MotorController_t g_motor;

// --- HARDWARE INTERFACE STUBS ---
void GPIO_SetPinHigh(int pin) { g_motor.supercap_gate = 1; }
void GPIO_SetPinLow(int pin)  { g_motor.supercap_gate = 0; }
void Update_SVPWM_Hardware_Registers(float v_alpha, float v_beta, float v_dc) {}

// --- INITIALIZATION API ---
void init_controller(void) {
    g_motor.i_phase_u = 0.0f;
    g_motor.i_phase_v = 0.0f;
    g_motor.theta_elec = 0.0f;
    g_motor.omega_elec = 1947.79f; // 3,100 RPM * 6 * 2pi/60
    g_motor.v_dc_bus = 1000.0f;
    g_motor.id_ref = 0.0f;
    g_motor.iq_ref_target = 1000.0f;
    g_motor.iq_ref_actual = 1000.0f;
    g_motor.prop_pitch_beta = 28.0f;
    g_motor.regen_enable = 1;
    g_motor.supercap_gate = 0;
    g_motor.vd_cmd = 0.0f;
    g_motor.vq_cmd = 0.0f;
}

// --- FOC REAL-TIME STEP ROUTINE (5 kHz / 200 µs Period) ---
void run_foc_step(float new_iq_target, float pitch_beta, float v_dc) {
    g_motor.iq_ref_target = new_iq_target;
    g_motor.prop_pitch_beta = pitch_beta;
    g_motor.v_dc_bus = v_dc;

    // 1. Feed-Forward Pitch Coordination
    if (g_motor.prop_pitch_beta <= 16.0f && g_motor.regen_enable) {
        float pitch_scale = (16.0f - g_motor.prop_pitch_beta) / 4.0f;
        if (pitch_scale > 1.0f) pitch_scale = 1.0f;
        if (pitch_scale < 0.0f) pitch_scale = 0.0f;
        g_motor.iq_ref_target = -280.0f * pitch_scale; 
    }

    // 2. Rate-Limiter (dI/dt Governor)
    float max_step = MAX_IQ_RAMP_A_PER_SEC * (1.0f / 5000.0f);
    float delta_iq = g_motor.iq_ref_target - g_motor.iq_ref_actual;
    
    if (delta_iq > max_step) {
        g_motor.iq_ref_actual += max_step;
    } else if (delta_iq < -max_step) {
        g_motor.iq_ref_actual -= max_step;
    } else {
        g_motor.iq_ref_actual = g_motor.iq_ref_target;
    }

    // Phase Current Reconstruction
    g_motor.i_phase_u = g_motor.iq_ref_actual * cosf(g_motor.theta_elec);
    g_motor.i_phase_v = g_motor.iq_ref_actual * cosf(g_motor.theta_elec - 2.094395f);

    // 3. Clarke Transformation
    float i_alpha = g_motor.i_phase_u;
    float i_beta  = 0.577350269f * (g_motor.i_phase_u + 2.0f * g_motor.i_phase_v);

    // 4. Park Transformation
    float cos_th = cosf(g_motor.theta_elec);
    float sin_th = sinf(g_motor.theta_elec);
    
    float i_d =  i_alpha * cos_th + i_beta * sin_th;
    float i_q = -i_alpha * sin_th + i_beta * cos_th;

    // 5. Deadbeat Predictive Current Control (DPCC)
    float vd_decouple = -g_motor.omega_elec * PHASE_INDUCTANCE_H * i_q;
    float vq_decouple =  g_motor.omega_elec * PHASE_INDUCTANCE_H * i_d + g_motor.omega_elec * FLUX_LINKAGE_WB;

    g_motor.vd_cmd = PHASE_RESISTANCE_OHM * i_d + (PHASE_INDUCTANCE_H / TS_CURRENT_LOOP_SEC) * (g_motor.id_ref - i_d) + vd_decouple;
    g_motor.vq_cmd = PHASE_RESISTANCE_OHM * i_q + (PHASE_INDUCTANCE_H / TS_CURRENT_LOOP_SEC) * (g_motor.iq_ref_actual - i_q) + vq_decouple;

    // 6. Supercapacitor Overvoltage Router
    if (g_motor.v_dc_bus > 1050.0f) {
        GPIO_SetPinHigh(0);
    } else if (g_motor.v_dc_bus < 1010.0f) {
        GPIO_SetPinLow(0);
    }

    // Angle Update
    g_motor.theta_elec += g_motor.omega_elec * (1.0f / 5000.0f);
    if (g_motor.theta_elec > 6.283185f) g_motor.theta_elec -= 6.283185f;
}

// --- C TELEMETRY GETTERS FOR CTYPES WRAPPER ---
float get_iq_actual(void)       { return g_motor.iq_ref_actual; }
float get_iq_target(void)       { return g_motor.iq_ref_target; }
float get_vq_cmd(void)          { return g_motor.vq_cmd; }
uint8_t get_supercap_state(void){ return g_motor.supercap_gate; }
