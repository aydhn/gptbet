---
owner: principal_adaptive_promotion_engineer
family: architecture
freshness_window_days: 90
---

# Constrained Auto-Promotion Architecture (Phase 47)

## Overview
The Constrained Auto-Promotion architecture introduces a semi-autonomous progression layer built on top of the Staged Candidate Channels. It automatically progresses low-risk, explicitly clean candidates while holding or killing explicitly risky or failing candidates.

It does not make stable pointer mutations or active product releases.

## Core Principles
1. **Auto Only Where Safe**: Automation only occurs in clearly defined low/medium risk situations.
2. **Hard Boundaries First**: High-risk items, missing approvals, stale simulations, and manual overrides immediately block automation.
3. **Progression is Earned**: Candidates must prove stability and cleanliness at each stage.
4. **Kill Early When Clearly Bad**: Candidates demonstrating repeated regressions or critical violations are automatically killed to free capacity.
5. **Human Override Remains Supreme**: Manual hold/freeze commands bypass heuristics unconditionally.

## Key Components
- **Eligibility Heuristics Engine**: Computes progression scores based on readiness, evidence completeness, and gate cleanliness.
- **Safety Boundary Evaluator**: Evaluates strict block rules (staleness, dispute count, manual override).
- **Quota Manager**: Constrains how many candidates can auto-progress or auto-kill per run.
- **Fleet Awareness Engine**: Groups candidates by target family and supersedes weaker candidates in favor of stronger alternatives.
- **Decision Evaluators**: Determines if a candidate meets thresholds for auto-progress, hold, kill, or review.
