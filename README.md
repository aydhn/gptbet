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
