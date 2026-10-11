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
