---
title: Consistency Ledgers Taxonomy Reference
family: consistency_ledgers
owner_role: Principal Alignment Federation Engineer
freshness_window: 90d
---

# Taxonomy Reference

## AlignmentAgreementBand
- `no_agreement`
- `weak_agreement`
- `bounded_agreement`
- `strong_agreement_with_caveats`
- `stable_agreement`

## TribunalMeshRouteOutcome
- `bounded_tribunal_route`
- `review_only_tribunal_route`
- `caveated_tribunal_route`
- `degraded_tribunal_route`
- `replay_required_tribunal_route`
- `blocked_tribunal_route`
- `no_safe_tribunal_route`

## ConsistencyState
- `consistent_with_caps`
- `caveated_consistency`
- `review_only_consistency`
- `degraded_consistency`
- `contradicted`
- `stale_consistency`
- `blocked_consistency`

See `src/sports_signal_bot/consistency_ledgers/contracts.py` for the full taxonomy definitions.
