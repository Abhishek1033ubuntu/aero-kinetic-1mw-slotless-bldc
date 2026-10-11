# Contributing to AeroKinetic-1MW-Slotless-BLDC

Thank you for your interest in contributing to the 1.0 MW Inverted Slotless BLDC Engine and Aero-Kinetic Regeneration Suite!

## How to Contribute

1. **Bug Reports & Feature Requests:** Please open an Issue detailing the bug, expected behavior, and reproduction steps.
2. **Pull Requests:**
   - Fork the repository and create your branch from `main`.
   - Ensure C firmware changes (`firmware/foc_firmware.c`) maintain deterministic execution under 20 µs current loop timing.
   - Run simulation scripts in `simulations/` to verify electrical and aerodynamic convergence.
   - Submit a PR with a clear description of changes and rationale.

## Code Standards
- **C Firmware:** C99 compliant, zero dynamic memory allocation (`malloc`), strict rate limiting on all current steps.
- **Python Scripts:** PEP 8 compliance, explicit typing where applicable, self-contained dependencies for Google Colab execution.

## License
By contributing, you agree that your contributions will be licensed under the repository's MIT License.
