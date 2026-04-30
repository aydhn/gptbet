---
owner: Operators
family: Runbook
freshness_window_days: 30
---

# Control Tower & Circuit Breakers Guide

## Control Tower Summaries
The control tower provides a consolidated view of:
- Active Waves & Cohorts
- Global Status (e.g., `expansion_normal`, `global_emergency_pause`)
- Pressure Bands (Low -> Critical)
- Budget Saturation

## Circuit Breakers
If critical thresholds are crossed (e.g., repeated rollbacks, verification failures), circuit breakers fire automatically.
- **Global Pause**: Halts all growth. Requires manual override to exit.
- **Family Freeze**: Halts growth for a specific family.

To preview state: `python -m sports_signal_bot.main expansion-governance preview-control-tower`
