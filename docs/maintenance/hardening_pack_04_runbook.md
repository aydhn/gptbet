# Hardening Pack 04 Runbook

Steps to maintain chaos hardening rules:
1. Update `configs/hardening/chaos.yaml` for new failure modes.
2. Review release blockers in `tests/chaos_hardening/test_release_blockers.py`.
3. Ensure CI runs the chaos iteration counts specified in `configs/hardening/chaos_ci.yaml`.
