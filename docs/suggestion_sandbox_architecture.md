# Suggestion Sandbox Architecture

## Purpose
The Suggestion Sandbox architecture provides a safe, isolated environment to evaluate candidate patch suggestions before they affect the live system. It acts as an experimentation laboratory to measure the before-and-after impact of configurations, policies, and weights.

## Core Concepts
- **Candidate Patch**: A proposed change derived from an automated or manual suggestion.
- **Sandbox Isolation**: Execution environment that guarantees no live state mutations.
- **Baseline vs Variant**: Comparing the exact same historical sample (same-universe) using the current behavior (baseline) against the new behavior (variant).
- **Materiality & Recommendations**: Automated scoring of the simulation delta to provide actionable recommendations (e.g., Safe for Review, Reject Patch).

## Components
1. **Patch Builder**: Converts suggestions into testable overrides.
2. **Sandbox Environment Manager**: Manages namespaces and override lifecycle.
3. **Execution Engines**: Handles what-if replays and baseline extraction.
4. **Comparison Engine**: Calculates deltas and validates the same-universe requirement.
5. **Recommendation Engine**: Issues recommendations based on materiality bands.

## Future Path
- Automated Safe Candidate Ranking
- Batch Tournaments
- Constrained Policy Search
