---
owner: "@principal_assurance_engineer"
family: "reference"
freshness_window: "90d"
---

# Capability Negotiation Taxonomy

## Capability Families
- `artifact_support_capability`
- `claim_support_capability`
- `proof_format_capability`
- `replay_capability`
- `notarization_capability`
- `translation_capability`
- `spec_bundle_capability`
- `trust_model_capability`

## Negotiation Statuses
- `negotiation_opened`: Started
- `partially_matched`: Common subset found but narrower than requested
- `fully_matched`: Exact match on requested dimensions
- `matched_with_caveats`: Translations or constraints required
- `blocked_incompatible`: No common safe subset found
- `quarantined_unknown_profile`: Unrecognized or overly broad capabilities claimed

## Replay Outcomes
- `replay_matched`: Negotiated profile remains valid.
- `replay_changed_due_to_new_policy`: Federation policy has tightened since negotiation.
- `replay_stale_profile`: Profile has expired.
