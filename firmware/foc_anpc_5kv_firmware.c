/*
 * 5.0 kV 5-Level ANPC FOC & Dynamic Coil Switching Interlock Firmware
 * Target Bus: 5000 V DC | Phase Current: 200 A RMS | f_sw: 40 kHz
 */

#include <math.h>
#include <stdint.h>

#define V_DC_BUS_NOMINAL_V      5000.0f
#define V_LEVEL_STEP_V          1250.0f  // V_DC / 4 for 5-Level ANPC
#define REGEN_IQ_TARGET_5KV_A   -56.0f   // Equivalent to -280A at 1.0 kV
#define MAX_IQ_RAMP_A_PER_SEC   100000.0f

typedef struct {
    float i_phase_u, i_phase_v, theta_elec, omega_elec;
    float id_ref, iq_ref_target, iq_ref_actual;
    float prop_pitch_beta;
    uint8_t regen_active;
    uint8_t active_coil_mask;
    uint8_t coil_switch_pending;
    uint8_t anpc_level_u, anpc_level_v, anpc_level_w;
} Controller5KV_t;

static Controller5KV_t g_ctrl;

// 5-Level ANPC Level Selection (Clamps dV/dt to 1.25 kV steps)
static uint8_t compute_anpc_level(float v_command) {
    if (v_command < 1250.0f) return 0;       // 0 V node
    else if (v_command < 2500.0f) return 1;  // 1250 V node
    else if (v_command < 3750.0f) return 2;  // 2500 V node
    else if (v_command < 5000.0f) return 3;  // 3750 V node
    else return 4;                           // 5000 V node
}

void run_5kv_foc_step(float demand_iq, float pitch_beta, uint8_t target_coil_mask) {
    g_ctrl.prop_pitch_beta = pitch_beta;
    g_ctrl.iq_ref_target = demand_iq;

    // Windmilling Kinetic Regeneration Feed-Forward
    if (g_ctrl.prop_pitch_beta <= 16.0f) {
        float regen_scale = (16.0f - g_ctrl.prop_pitch_beta) / 4.0f;
        if (regen_scale > 1.0f) regen_scale = 1.0f;
        if (regen_scale < 0.0f) regen_scale = 0.0f;
        g_ctrl.iq_ref_target = REGEN_IQ_TARGET_5KV_A * regen_scale;
        g_ctrl.regen_active = 1;
    }

    // Zero-Current Safe Interlock for Dynamic Coil Switching
    if (target_coil_mask != g_ctrl.active_coil_mask) {
        g_ctrl.coil_switch_pending = 1;
        g_ctrl.iq_ref_target = 0.0f; // Force current down before opening contactors
        
        if (fabsf(g_ctrl.iq_ref_actual) < 1.0f) {
            g_ctrl.active_coil_mask = target_coil_mask; // Execute safe coil switch
            g_ctrl.coil_switch_pending = 0;
        }
    }

    // Rate Limiting (Slewing Control)
    float max_step = MAX_IQ_RAMP_A_PER_SEC * (1.0f / 50000.0f); // 50 kHz current loop
    float delta_iq = g_ctrl.iq_ref_target - g_ctrl.iq_ref_actual;
    if (delta_iq > max_step) g_ctrl.iq_ref_actual += max_step;
    else if (delta_iq < -max_step) g_ctrl.iq_ref_actual -= max_step;
    else g_ctrl.iq_ref_actual = g_ctrl.iq_ref_target;

    // Compute ANPC Switching Levels
    g_ctrl.anpc_level_u = compute_anpc_level(2500.0f + g_ctrl.iq_ref_actual * 2.0f);
}
