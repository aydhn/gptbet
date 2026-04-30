# Sports Signal Bot

...

## Staged Candidate Channels (Phase 46)

The Staged Candidate Channels layer provides a progressive, multi-stage evaluation pipeline for candidate packages before they reach active deployment.

### Purpose

It is not enough for a package to be "candidate-ready". It must be safely proven in progressively stricter environments:
- **Shadow**: Runs side-by-side with production but makes no active changes. Used for comparing decisions without cost.
- **Candidate Eval**: Stricter evaluation looking at fleet conflicts, monitoring burden, and review history.
- **Live-like Safe**: The final evaluation step representing an ops-ready simulation, comparing directly against the stable-reference channel but preserving the current stable pointer.

### Fleet & Capacity

We simulate multiple simultaneous candidate patches as a "Fleet". Candidates are subject to capacity limits per-channel and conflict-detection (e.g., mutually exclusive candidates targeting the same component). Candidates can be held, or queued into later rollout "Waves" based on channel capacity.

### Rollback to Shadow & Retiring
- **Rollback to shadow**: A candidate exhibiting regression is not immediately killed. It can be bumped back to the shadow channel for safer observation and evidence gathering.
- **Supersession & Retirement**: A candidate can be retired if a newer, narrower/safer candidate replaces it, or if it has an excessively high error rate.

### Run commands
```bash
python -m sports_signal_bot.main preview-channel-state
python -m sports_signal_bot.main run-staged-rollout
python -m sports_signal_bot.main list-staged-channel-strategies
```

This phase focuses on the candidate evaluation lifecycle, deferring active percentage traffic splitting and autonomous promotions to later phases.

## Constrained Auto-Promotion (Phase 47)

The Constrained Auto-Promotion layer introduces semi-autonomous progression on top of Staged Channels. It evaluates candidates to auto-progress low-risk clean candidates, or auto-hold / auto-kill candidates that violate hard safety boundaries (stale simulations, unresolved disputes, missing approvals). It works under quota limits and features fleet-aware suppression (superseding weak candidates with stronger ones).

Auto-progressions, holds, and kills are only executed if they do not violate explicitly set hard safety boundaries or manual overrides. It explicitly avoids mutating active stable or canary product pointers.

### Run commands
```bash
# Run the auto-promotion heuristic engine over active candidates
python -m sports_signal_bot.main auto-promotion run-auto-promotion-pass

# Preview eligible progressions without state mutation (dry-run)
python -m sports_signal_bot.main auto-promotion preview-auto-progression

# List available auto-promotion strategies
python -m sports_signal_bot.main auto-promotion list-auto-promotion-strategies
```

For more detail, refer to `docs/constrained_auto_promotion_architecture.md`.

## Cohort Autopilot (Phase 50)

The Cohort Autopilot layer introduces safe, segment-based adoption control. It upgrades the system from single stable adoption to cohort-based, percentage-like rollout simulation. It features autonomous post-activation verification, automated growth, pause, shrink, and rollback decisions based on continuous health assessments.

### Run commands
```bash
python -m sports_signal_bot.main cohort-autopilot run-cohort-autopilot
python -m sports_signal_bot.main cohort-autopilot preview-adoption-cohorts
```

For more detail, refer to `docs/cohort_autopilot_architecture.md`.

### Phase 48: Candidate-to-Release Handoff
The handoff layer ensures that candidates from the constrained auto-promotion and staged channels are formally evaluated by a `Final Readiness Council`. This deterministic evaluation uses various lenses (safety, evidence, governance) to produce a Readiness Matrix.
Crucially, **this phase does not mutate the active stable pointer**. Instead, approved candidates are transitioned into an `Activation Bridge`, yielding an `ActivationBridgePackageRecord`. This differentiates `bridge_ready` from actual `activation_ready`, ensuring strict governance and enabling kill-before-handoff disciplines.
Commands:
- `python -m sports_signal_bot.main handoff run-handoff-pass`

### Phase 51: Expansion Governance
Introduces a global control plane for coordinating multiple rollout waves and cohorts. It implements global risk budgets, pressure scoring, cross-family conflict detection, and emergency circuit breakers (Global Pauses and Family Freezes) to safely manage large-scale expansion. Run `python -m sports_signal_bot.main expansion-governance run-expansion-governance` to execute a cycle.
