# Reviewers Guide: Currentness, Successors, and Exception Boundedness

## Importance of Boundedness

When an exception is necessary, it must be **explicit, narrow, and reversible**. A key principle is that exceptional pathways only afford visibility or review-only hints; they do not widen authority.

## Currentness and Caveat Rules

1. **No caveat stripping**: Any caveat applied by a source quorum attestation must propagate exactly as-is through exchanges.
2. **Stale Evidence**: If the underlying evidence is stale, the projection degrades immediately to `review_only` or is suppressed entirely.
3. **Missing Successors**: Baseline conflicts where a successor is unresolved block strong paths. Exceptions opened for missing successors provide temporary review-only visibility, not authorization.

## Reviewing Exception Ledgers

Reviewers should frequently check exception ledgers to ensure:
- Exceptions are not masking a local sovereignty `deny`.
- `validity_window` values are appropriate and correctly triggered.
- Exceptions are expiring or being superseded correctly once conditions clear.
