---
owner: transparency_engineer
family: platform
freshness: P30D
---

# Transparency Runbook

## Routine Checks
1. Check mirror sync health: `python -m sports_signal_bot.main transparency verify-transparency-mirrors`
2. Validate consistency of checkpoints across critical families.
3. Review unsigned checkpoints in families requiring strict signatures.

## Responding to Divergence
If a mirror flags divergence:
- System auto-quarantines the mirror.
- Manual investigation needed to see if the root log was mutated, or if mirror is desynced.
- Trigger `verify-inclusion-proof` to confirm specific decisions remain.
