# Governance Exceptions Runbook

## Investigating Expired Exceptions Still Referenced
Alert: `expired exception still referenced alert`
Action: Check the ledger manifest to ensure garbage collection or supersession tasks ran correctly. Validate that no downstream controller is caching an expired exception ID.

## Investigating Unresolved Exception Backlogs
Alert: `unresolved exception backlog spike alert`
Action: Indicates that dispute mediation or baseline councils are failing to reach resolutions, forcing the system into a high volume of temporary exceptions. Check the upstream baseline mesh council health.

## Investigating Scope Broadening Attempts
Alert: `exception scope broadening attempt alert`
Action: Critical security event. An exception tried to authorize a domain beyond its source attestation. Check the offending exception ID against the `QuorumExchangeScopeRecord` and trace back to the ingress point. Ensure that `prevent_exception_scope_broadening` is actively returning a block.
