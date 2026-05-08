# Reviewer Guide: Baselines, Concealment, and Residues

This guide explains how to review baselines, ensure lack of concealment, and verify residues.

## Baseline Drift

Check `frozen_baselines.json` for `drift_refs`. Any hidden drift is a violation of the `BaselineTruthFirstStrategy`.

## Review Concealment

Check `production_readiness_review_surfaces.json` for `blocker_refs`, `residue_refs`, and `gap_refs`. Ensure `hidden` is `false`.

## Acceptance Residues

Check `terminal_acceptance_packs.json` for `residue_refs` and ensure they are not hidden. Acceptance evidence must also be `replayable`.
