# Context Assembly Runbook

## Handling Blocked Context Bundles
1. Check inputs: Are any inputs marked `stale` or `blocked`?
2. Check sections: Is a `no_safe_visibility` section required but missing?
3. Action: Resolve the underlying freshness or sovereignty conflict.

## Freshness Council Quorum Failures
1. Symptom: Council cases remain in `CASE_QUORUM_PENDING` or degrade to `CASE_REVIEW_ONLY`.
2. Action: Verify participant refs and ensure enough board members are online to vote.

## Stale Federation Routes
1. Symptom: Federation output is `federation_stale`.
2. Action: Identify the stale trace route and invoke the trace router refresh pipeline.
