# Reviewer Guide: Freshness Evidence & Context Integrity

## Core Philosophy
Currentness, proof freshness, and no-safe visibility are load-bearing properties of this system.

## Reviewing Freshness
- Proofs naturally decay into bands: `fresh`, `borderline`, `stale`, `severely_stale`.
- Reviewers should verify that proof freshness councils are opening cases for borderline or stale proofs.
- If refresh evidence is insufficient, reviewers should ensure the case remains blocked or is downgraded to review-only.

## Reviewing Context Integrity
- Check `ContextBundleRecord` outputs.
- Verify that `no_safe_visibility_state` and sovereignty warnings are preserved in the final output. If they are dropped, the assembly is considered a failure and will be blocked.
