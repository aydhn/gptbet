---
owner: "resilience-orchestrator-team"
doc_family: "architecture"
freshness_window_days: 90
---

# Resilience Advisor & Recovery Orchestration Architecture

## Overview
Phase 69 introduces the Resilience Advisor, a bounded, advisory-first orchestration layer that synthesizes historical failure pattern memory with live signals to produce safe, reviewable remediation playbooks and orchestration plans.

## Key Principles
1. **Advice Before Action:** Produces actionable guidance; mutation is gated by policy.
2. **Memory is Structured:** Failure patterns are indexed, ranked, and weighted.
3. **Playbooks are Synthesized:** Playbooks are generated dynamically from patterns and constraints.
4. **Recovery is Bounded:** Scopes are restricted, rollbacks are explicit, and review lanes are enforced.

## Subsystems
- **Pattern Memory:** `sports_signal_bot.resilience_advisor.memory`
- **Playbook Synthesis:** `sports_signal_bot.resilience_advisor.synthesis`
- **Orchestration:** `sports_signal_bot.resilience_advisor.orchestration`
- **Confidence & Guards:** `sports_signal_bot.resilience_advisor.confidence`, `guards.py`

## Integration
Feeds off `resilience_fabric`, `streaming_discovery`, and `conformance` layers. Output serves as input to approval-gated auto-healing in future phases.
