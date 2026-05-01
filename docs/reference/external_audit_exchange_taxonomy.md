# External Audit Exchange Taxonomy

## Exchange Families
- `external_challenge_review_exchange`
- `external_transparency_verification_exchange`
- `external_signed_bundle_review_exchange`
- `external_notarization_exchange`
- `external_witness_confirmation_exchange`
- `external_import_verification_exchange`
- `external_integrity_finding_exchange`

## Finding Severities
- `info`
- `warning`
- `error`
- `critical`

## Finding Families
- `proof_mismatch_finding`
- `publication_gap_finding`
- `stale_checkpoint_finding`
- `mirror_divergence_finding`
- `signer_scope_mismatch_finding`
- `notarization_supporting_finding`
- `notarization_missing_finding`
- `anomaly_confirmation_finding`
- `anomaly_rejection_finding`
- `insufficient_data_finding`
- `local_verification_needed_finding`

## Response Statuses
- `imported_pending_verification`
- `imported_verified_supporting`
- `imported_nonbinding`
- `imported_quarantined`
- `imported_rejected`
- `imported_superseded`

## Local Actions
- `no_change`
- `add_supporting_evidence`
- `open_review_case`
- `open_anomaly_case`
- `quarantine_bundle_or_response`
- `downgrade_witness_reputation`
- `upgrade_witness_reputation`
- `require_manual_adjudication`
- `freeze_family_recommended`
- `integrity_alert`
