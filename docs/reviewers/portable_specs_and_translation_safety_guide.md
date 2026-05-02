---
owner: "@principal_assurance_engineer"
family: "reviewer_guide"
freshness_window: "90d"
---

# Portable Specs & Translation Safety Guide

## Portable Spec Bundles
When exporting governance rules to external federation partners, we use **Portable Spec Bundles**.
- Internal constraints, sensitive risk thresholds, and local-only logic are stripped or redacted.
- Bundles are classified by portability (e.g., `fully_portable`, `review_only_portable`).

## Translation Safety
During negotiation, foreign registries might map our claims to theirs, or vice versa.
- **Rule:** Claim translation must NEVER artificially amplify trust.
- If a translation suggests mapping a low-assurance local claim to a high-assurance foreign semantic, it must be rejected or downgraded to the common safe subset.

## Reviewing Translations
Reviewers must examine `NegotiatedTranslationRuleRecord` entries in `CapabilityDiffRecord` objects. Ensure no semantic loss occurs that weakens the safety posture of the receiving registry.
