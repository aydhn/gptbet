import uuid
from datetime import datetime, timezone
from typing import List
from .contracts import (
    PlaybookExchangeCatalogRecord, PlaybookListingRecord, RemediationLaneRecord,
    LaneFamily, RollbackBindingRecord, LaneStatus
)

def build_federated_playbook_exchange_catalog(listings: List[PlaybookListingRecord]) -> PlaybookExchangeCatalogRecord:
    return PlaybookExchangeCatalogRecord(
        catalog_id=f"catalog_{uuid.uuid4().hex[:8]}",
        published_at=datetime.now(timezone.utc),
        listings=listings,
        catalog_health="healthy" if listings else "empty"
    )

def adapt_federated_playbook_into_lane(listing: PlaybookListingRecord, incident_family: str) -> RemediationLaneRecord:
    status = LaneStatus.lane_defined
    allowed_steps = ["read", "observe"]

    if listing.has_rehearsal_evidence:
        allowed_steps.extend(["restart", "clear_cache"])

    lane_family = listing.supported_lane_families[0] if listing.supported_lane_families else LaneFamily.review_only_investigation_lane

    return RemediationLaneRecord(
        lane_id=f"lane_{uuid.uuid4().hex[:8]}",
        lane_family=lane_family,
        incident_family=incident_family,
        scoped_playbook_ref=f"adapted_{listing.playbook_ref}",
        current_status=status,
        allowed_step_families=allowed_steps,
        forbidden_step_families=["drop_database", "mutate_schema", "force_override"],
        rollback_binding=RollbackBindingRecord(
            rollback_playbook_ref=f"rollback_{listing.playbook_ref}",
            rollback_scope=incident_family,
            rollback_checkpoints=["system_stable"],
            is_verified_in_rehearsal=listing.has_rehearsal_evidence
        ),
        observability_refs=["ext_monitoring_1"],
        warnings=["Adapted from federated catalog; requires local review mapping"]
    )
