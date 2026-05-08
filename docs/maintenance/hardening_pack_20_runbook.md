# Runbook: Hardening Pack 20

## Purpose

To ensure that the final convergence pass operates correctly and does not hide state, caveats, or blockers.

## Procedures

1.  Run the tests in `tests/final_convergence_hardening/`.
2.  Run the CLI: `python -m sports_signal_bot.main run-hardening-pack-20`.
3.  Inspect the output JSON artifacts for validity.
