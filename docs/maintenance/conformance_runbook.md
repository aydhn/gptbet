# Conformance Runbook

In case of a compliance gate block:
1. Examine the `reason` output.
2. If it's a lint failure, review the `policy_lint_findings` for syntax/semantic issues.
3. If it's a drift, use the `remediation_hint` from the `drift_attestation` to synchronize states.
4. Only request an exemption for non-critical failures, providing clear rationale.
