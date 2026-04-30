---
owner: ops
family: guide
freshness_window_days: 60
---

# Auto Progression and Auto Kill Guide

## Introduction
The Auto-Promotion engine semi-autonomously evaluates staged candidates. It significantly reduces human toil by managing clear-cut cases.

## How it Works
Run the heuristic engine:
```bash
python -m sports_signal_bot.main auto-promotion run-auto-promotion-pass
```

The system will generate an evaluation summary and write decision artifacts (JSON) to the working directory.

## Interpreting Output
- **Auto-Progress**: The candidate met all heuristic requirements and safety checks, and had quota available to move to the next stage.
- **Auto-Hold**: The candidate lacked fresh gate results, had minor conflicts, or hit quota limits, but isn't failing critically.
- **Auto-Kill**: The candidate failed required gates with low readiness, had unresolved critical disputes, or was superseded by a stronger candidate in its target family.
- **Review Required**: The candidate didn't qualify for auto-progress but didn't meet kill criteria. Human intervention is required.
