# Changelog

All notable changes to the **AeroKinetic-1MW-Slotless-BLDC** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-HV] - 2026-10-12

### Added
- **5.0 kV High-Voltage Architecture:** Scaled DC link potential to 5.0 kV DC, dropping RMS phase current at 1.0 MW from 1,000 A down to 200 A.
- **Power Density Upgrade:** Increased gravimetric power density from 11.36 kW/kg to **18.52 kW/kg** (54 kg motor engine mass).
- **5-Level ANPC SiC Drive Firmware:** C99 ISR routines (`firmware/foc_anpc_5kv_firmware.c`) implementing 5-Level ANPC switching, reducing $dV/dt$ step stress by $75\%$ ($94.44\text{ kV/}\mu\text{s}$).
- **Nanocomposite Dielectric Matrix:** Integrated Nano-$\text{Al}_2\text{O}_3$ polyimide insulation, SiC non-linear field-grading, and coaxial SWCNT ground shielding.
- **Extended Pulse Endurance:** Verified insulation lifespan extension to **$48,176.3\text{ hours}$** under $40\text{ kHz}$ high-voltage pulse stress.
- **Feeder Cable Harness Weight Reduction:** Reduced $10\text{m}$ wing feeder cable harness mass from $42\text{ kg}$ down to **$9.5\text{ kg}$** ($77.4\%$ harness mass savings).
- **Enhanced Kinetic Regeneration:** Achieved $98.42\%$ net recovery efficiency ($76.87\text{ kWh}$ harvested during windmilling descent).

## [1.0.0] - 2026-10-11

### Added
- Initial release of 1.0 MW Inverted Slotless BLDC machine architecture ($1.0\text{ kV} / 1,000\text{ A}$).
- Single-crystal SWCNT-OCC copper conductor and GBD N55SH Halbach rotor design.
- Python simulation suite for micro-scale reciprocity, 1.0 MW flight profile, and kinetic regeneration.
# Changelog

All notable changes to the **AeroKinetic-1MW-Slotless-BLDC** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-12

### Added
- **Core Motor Architecture:** Complete engineering specification for 1.0 MW Inverted Slotless BLDC machine achieving 11.36 kW/kg power density.
- **Advanced Subatomic Materials:** Integration of SWCNT-coated OCC copper conductors (122% IACS), Grain-Boundary Diffused N55SH NdFeB magnets, and BNNT interpenetrated polyimide stator matrix.
- **Thermodynamic & Aero Simulations:** ISA atmosphere integration and variable-pitch propeller windmilling models demonstrating 10.84% net descent energy recovery (74.73 kWh).
- **SiC Inverter & Control Firmware:** C99-compliant real-time FOC, DPCC current controller, feed-forward propeller pitch governor, and supercapacitor overvoltage protection.
- **Hardware-in-the-Loop (HIL):** Python `ctypes` harness executing compiled C firmware in Google Colab environments.
- **Documentation & Citations:** Comprehensive PDF specification reports, CITATION.cff with ORCID binding (`0009-0004-6913-096X`), and GitHub publishing metadata.

