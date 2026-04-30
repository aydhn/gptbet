---
title: Candidate Tournament Architecture
owner: Principal Experimentation Engineer
family: architecture
freshness: P90D
---

# Batch Candidate Tournament Architecture

This phase elevates the system from evaluating single suggestions in isolation to evaluating multiple candidate patches concurrently using a shared evaluation universe.

## Core Concepts

1. **Same-Universe Fairness**: All candidates in a batch must be evaluated on the exact same `ComparisonUniverseRecord` to ensure valid comparison metrics.
2. **Multi-Objective Pareto Front**: Candidates are compared across multiple dimensions (e.g., quality vs. dispute burden). We compute non-dominated fronts before scalarizing into a single score.
3. **Safety Lanes**: Candidates are categorized into lanes (Safe Shortlist, Advisory, Exploratory, Blocked) depending on their risk profiles and evidentiary support.
4. **Shortlist Tiers**: The system produces actionable recommendations mapped to review tiers rather than automatically promoting winners to production.
