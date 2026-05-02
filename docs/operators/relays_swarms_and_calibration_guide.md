# Relays, Swarms, and Calibration Guide

## Monitoring Relays
Relay health is continuously evaluated against continuity, freshness, and integrity. Degraded relays can be safely quarantined automatically according to the `relay_quarantine_rules`.

## Managing Swarms
Mirror swarms provide consistency checks. If a split-brain is suspected (e.g., `split_observation`), manual review may be required depending on the active resilience strategy.

## Trust Loop Calibration
The system will occasionally propose routing weight adjustments. All proposed adjustments are bounded by configured safety limits (`calibration_adjustment_bounds`) and must pass validation before affecting active routing logic.
