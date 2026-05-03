# Phase 70: Remediation Copilot & Rehearsal Ledger

This phase introduces the **Remediation Copilot** layer, converting advisory outputs into approval-gated, rehearseable recovery preparation flows.

## What's New

1. **Approval-Gated Flow**: Recommendations generate Review Packets, necessitating structured approvals (`scope`, `duration`) before advancing to rehearsal.
2. **Rehearsal Ledgers**: Playbook viability is proven in isolated/simulation contexts first. Real observed results are logged into immutable `RehearsalLedgers`.
3. **Execution Readiness**: Readiness evaluations ensure zero live-execution until guards pass, rehearsal succeeds, and rollbacks are sufficient.
4. **Portable Playbook Federation**: Playbooks can be exported across domains, paired with required `Adaptation` layers restricting unverified semantic expansions locally.
5. **Self-Healing Preparation**: Identifies candidates for automation and envelopes them (`AutomationEnvelopeRecord`), preparing boundaries for future bounded self-healing without bypassing current governance.

## Key CLI Operations

- `python -m sports_signal_bot.main remediation-copilot run-remediation-copilot-pass`
- `python -m sports_signal_bot.main remediation-copilot preview-copilot-sessions`
- `python -m sports_signal_bot.main remediation-copilot preview-rehearsal-ledgers`
- `python -m sports_signal_bot.main remediation-copilot preview-execution-readiness`

## Future Integration

Ready for Phase 71 (Semi-Autonomous Copilots), bounded auto-execution lanes, and dynamic playback loops within the Rehearsal Ledger.
