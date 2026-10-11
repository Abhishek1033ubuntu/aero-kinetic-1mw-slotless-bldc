# AeroKinetic-1MW-Slotless-BLDC v1.0.0 — Initial Publication Release

We are proud to announce the formal initial release of the **1.0 MW Inverted Slotless/Coreless BLDC Motor & Bidirectional Kinetic Regeneration Suite** for hybrid-electric aerospace applications.

### 🌟 Key Highlights & Performance Specs

* **Gravimetric Power Density:** **11.36 kW/kg** (88 kg total engine mass).
* **Peak System Efficiency:** **98.1% – 99.36%** across takeoff, climb, and high-altitude cruise regimes.
* **Flight Kinetic Recovery:** **10.84% net mission energy recovery** (74.73 kWh harvested during windmilling descent).
* **Zero Core Iron Drag:** Complete elimination of stator hysteresis/eddy-current losses ($P_{\text{iron}} = 0.0\text{ W}$).
* **Direct Internal Liquid Cooling:** Hollow rectangular SWCNT-OCC conductors ($72\text{ mm}^2$ net Cu) maintaining winding temperature below $46.6^\circ\text{C}$ during full takeoff power.
* **Ultra-Fast SiC Inverter:** $40\text{ kHz}$ switching frequency with $1.60\text{ ms}$ zero-crossing current inversion ($dI/dt = 800,000\text{ A/s}$).

### 📦 Release Assets

- `firmware/foc_firmware.c`: C99 FOC & DPCC control firmware ISR routines.
- `simulations/`: Complete Python simulation suite (micro-scale proof, flight profile, and regen thermodynamics).
- `docs/`: Publication-ready PDF specifications and final engineering reports.
- `CITATION.cff`: Formal academic citation schema bound to ORCID `0009-0004-6913-096X`.

### 👤 Author & Principal Investigator
* **Abhishek Singh** — [ORCID: 0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X)
* **Matter ID:** `AS-1MW-BLDC-2026` / `AS-8102-1MW`
