---
owner: ops
family: runbook
freshness: 30d
---

# Candidate Promotion Runbook

## Commands

To run candidate promotion pipeline:
```bash
python -m sports_signal_bot.main candidate-promotion run-candidate-promotion
```

To preview readiness:
```bash
python -m sports_signal_bot.main candidate-promotion preview-candidate-readiness
```

To preview decisions:
```bash
python -m sports_signal_bot.main candidate-promotion preview-candidate-decisions
```

## Troubleshooting
- **Blocked Candidates**: Check the stage failures using `preview-candidate-stages`. If it's a safety block, the candidate must be revised or killed.
- **Stuck in Hold**: Usually due to missing manual approvals or stale gate results. Verify `CandidateReadinessRecord.missing_requirements`.
