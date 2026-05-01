# Phase 61: Formal Conformance and Compliance Architecture

This phase elevates the platform from having a rich governance architecture to continuously and formally verifying it.

## Key Outcomes
- **Governance Spec Registry:** Explicit models (`GovernanceSpecRecord`, `SpecAssertionRecord`) for domain rules.
- **Policy Linting:** Early structural detection of risks (`ambiguous_precedence`, `unsafe_overlay_scope`).
- **Drift Attestation:** Attested baseline-vs-active divergence covering critical operational properties.
- **Continuous Verification Pipeline:** E2E stages (resolution, lint, static conformance, drift, gating).
- **Compliance Gates:** Block or approve promotions based on multi-stage findings.
- **Exception Discipline:** Records exceptions explicitly, banning silent or un-expiring circumventions.
- **Future Ready:** Clean APIs left for proof-carrying bundles and formal remediation.

## How to use
- `python -m sports_signal_bot.main conformance run-conformance-pass`
- `python -m sports_signal_bot.main conformance preview-governance-specs`
- `python -m sports_signal_bot.main conformance preview-policy-lint`
- `python -m sports_signal_bot.main conformance preview-drift-attestations`
- `python -m sports_signal_bot.main conformance preview-compliance-gates`

See `docs/formal_conformance_and_compliance_architecture.md` for more context.
