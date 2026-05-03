# Remediation Copilot Runbook

This runbook covers maintenance tasks for the Remediation Copilot layer.

## Checking Active Sessions
Run the CLI to see active sessions and their stages:
```bash
python -m sports_signal_bot.main remediation-copilot preview-copilot-sessions
```

## Investigating Blocked Preparations
If a playbook is blocked from execution readiness, inspect the readiness blockers:
```bash
python -m sports_signal_bot.main remediation-copilot preview-execution-readiness
```
Common blockers include missing approvals or failed rehearsal assertions.

## Reviewing the Rehearsal Ledger
To audit past rehearsal attempts and failures:
```bash
python -m sports_signal_bot.main remediation-copilot preview-rehearsal-ledgers
```
Ensure that ledger integrity is maintained and that entries correctly reflect simulation outcomes.
