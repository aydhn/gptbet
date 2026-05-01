# Multi-Signer Trust Runbook

## Daily Ops
- Run `preview-multi-signer-approvals`
- Address any `THRESHOLD_FAILED` blocks.

## Break-Glass Recovery
- In a critical failure, operators can issue a break-glass record. Ensure it is resolved and reviewed within the mandated expiry window (e.g., 24 hours).

## Dealing with Expiry
- All emergency and pending approvals without sufficient weight eventually expire, preventing hanging state within the trust matrix.
