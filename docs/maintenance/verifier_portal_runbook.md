# Verifier Portal Runbook

## Overview
This runbook covers the operational tasks associated with maintaining the verifier portal and external intake APIs.

## Routine Tasks
1. **Feed Freshness Check**: Regularly run feed previews to ensure external dashboard feeds are actively updating.
   - Command: `python -m sports_signal_bot.main verifier-portal preview-dashboard-feeds`
2. **Review Quarantined Challenges**: Triaging challenges is a daily operational task to prevent the queue from backing up.
   - Command: `python -m sports_signal_bot.main verifier-portal preview-challenge-api-submissions`
3. **Validate Readiness**: Use the CLI to confirm the portal remains in a healthy state and is ready for public or auditor review.
   - Command: `python -m sports_signal_bot.main verifier-portal preview-verifier-experience-readiness`

## Troubleshooting
- **Stale Publication Index**: If the publication index is consistently returning stale warnings, check the background disclosure delivery processes.
- **Profile Leakage Warnings**: If a packet contains a "profile mismatch" alert, inspect the `redact_query_results` logic to ensure strict constraints are applied.
