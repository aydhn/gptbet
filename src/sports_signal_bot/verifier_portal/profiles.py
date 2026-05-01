from typing import Dict
from .contracts import PortalAudienceProfileRecord

def get_profile(profile_id: str) -> PortalAudienceProfileRecord:
    profiles = {
        "public_viewer": PortalAudienceProfileRecord(
            profile_id="public_viewer",
            visible_view_families=["publication_index_view", "checkpoint_summary_view", "proof_summary_view", "readiness_dashboard_view"],
            proof_depth="minimal",
            challenge_submission_rights=False,
            feed_access_level="public",
            notarization_visibility=True,
            anomaly_detail_depth="none",
            signer_metadata_masking_level="full"
        ),
        "registered_verifier": PortalAudienceProfileRecord(
            profile_id="registered_verifier",
            visible_view_families=["publication_index_view", "disclosure_bundle_view", "checkpoint_summary_view", "proof_summary_view", "challenge_status_view", "readiness_dashboard_view"],
            proof_depth="standard",
            challenge_submission_rights=True,
            feed_access_level="standard",
            notarization_visibility=True,
            anomaly_detail_depth="summary",
            signer_metadata_masking_level="partial"
        ),
        "trusted_external_verifier": PortalAudienceProfileRecord(
            profile_id="trusted_external_verifier",
            visible_view_families=["publication_index_view", "disclosure_bundle_view", "checkpoint_summary_view", "proof_summary_view", "decision_trace_view_publicsafe", "witness_consensus_view", "challenge_status_view", "notarization_status_view", "readiness_dashboard_view"],
            proof_depth="deep",
            challenge_submission_rights=True,
            feed_access_level="premium",
            notarization_visibility=True,
            anomaly_detail_depth="detailed",
            signer_metadata_masking_level="minimal"
        ),
        "external_auditor": PortalAudienceProfileRecord(
            profile_id="external_auditor",
            visible_view_families=["publication_index_view", "disclosure_bundle_view", "checkpoint_summary_view", "proof_summary_view", "decision_trace_view_publicsafe", "witness_consensus_view", "anomaly_status_view", "challenge_status_view", "notarization_status_view", "readiness_dashboard_view"],
            proof_depth="full",
            challenge_submission_rights=True,
            feed_access_level="all",
            notarization_visibility=True,
            anomaly_detail_depth="full",
            signer_metadata_masking_level="none"
        ),
        "quarantine_reviewer": PortalAudienceProfileRecord(
            profile_id="quarantine_reviewer",
            visible_view_families=["challenge_status_view", "anomaly_status_view", "disclosure_bundle_view"],
            proof_depth="standard",
            challenge_submission_rights=False,
            feed_access_level="quarantine_only",
            notarization_visibility=False,
            anomaly_detail_depth="full",
            signer_metadata_masking_level="partial"
        ),
        "internal_preview_viewer": PortalAudienceProfileRecord(
            profile_id="internal_preview_viewer",
            visible_view_families=["publication_index_view", "disclosure_bundle_view", "checkpoint_summary_view", "proof_summary_view", "decision_trace_view_publicsafe", "witness_consensus_view", "anomaly_status_view", "challenge_status_view", "notarization_status_view", "readiness_dashboard_view"],
            proof_depth="full",
            challenge_submission_rights=True,
            feed_access_level="all",
            notarization_visibility=True,
            anomaly_detail_depth="full",
            signer_metadata_masking_level="none"
        )
    }
    return profiles.get(profile_id, profiles["public_viewer"])
