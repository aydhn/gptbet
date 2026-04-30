---
owner_role: Principal Data Reliability Engineer
doc_family: reference
freshness_window_days: 90
---

# Reconciliation Conflict Taxonomy

This reference documents the taxonomy of conflicts caught by the reconciliation engine.

## Fixture Conflicts
- `kickoff_time_mismatch`: (Medium) Different start times reported.
- `home_away_swap_suspected`: (High) Participants reversed.
- `event_status_mismatch`: (Critical) E.g., one source says "postponed", another says "live".

## Odds Conflicts
- `line_value_mismatch`: (High) Disagreement on handicap or total lines.
- `decimal_odds_outlier`: (Medium) One bookmaker's odds deviate wildly from consensus.
- `missing_selection_odds`: (Low) Partial market availability.

## Results Conflicts
- `final_score_mismatch`: (Critical) Providers disagree on the final outcome.
- `cancelled_vs_finished_conflict`: (Critical) Opposing settlement statuses.

## Team Metadata Conflicts
- `team_alias_conflict`: (Low) Minor string variations.
- `canonical_name_conflict`: (Medium) Different canonical mappings.
