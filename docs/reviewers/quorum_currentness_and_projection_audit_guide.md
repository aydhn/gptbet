# Reviewer Guide: Quorums, Currentness, and Audit Replays

## Verifying Council Decisions
Reviewers must ensure that Council Decisions carry a verifiable lineage.
*   Check the `CouncilDecisionEnvelopeRecord` for `caveats` and `lineage_refs`.
*   Ensure that failed quorums correctly map to `case_blocked` rather than proceeding silently.

## Auditing Federated Baselines
Federated baseline currentness is a common source of drift.
*   A `BaselineFederationCurrentnessRecord` with `freshness_projection="stale"` must result in a `currentness_outcome` that is bounded or caveated, *never* strong.
*   Look for `federation_drift_status` in the logs to spot mismatches in applicability.

## Projection Audit Replays
Audit Exchanges are the primary defense against unwarranted projection strength.
*   When reviewing an audit exchange, look at the `ProjectionAuditReplayRecord`.
*   If `replay_outcome` is `replay_currentness_drifted` or similar, the associated `ProjectionAuditDecisionRecord` *must* show `final_status="capped"`.
*   Packets lacking evidence references should be rejected outright (`audit_blocked`).
