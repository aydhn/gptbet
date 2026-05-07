# Maintenance Runbook: Hardening Pack 17

## Routine Checks
1.  Run the verification suite: `python -m sports_signal_bot.main continuity-verification-hardening run-hardening-pack-17`
2.  Review the health report: `python -m sports_signal_bot.main continuity-verification-hardening preview-continuity-verification-health`

## Troubleshooting
-   **Status is 'review_only':** Usually indicates stale evidence or insufficient quorum. Check the specific artifact JSON (e.g., `scheduler_proof_lanes.json`).
-   **Status is 'caveated':** The component is functioning but has warnings. Review the `warnings` array in the JSON output.
-   **Budget Breaches:** Check `continuity_verification_budgets.json` to see which operation exceeded its time limit.
