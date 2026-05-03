from datetime import datetime, timezone
import uuid
from typing import List, Optional
from .contracts import (
    RegistryEntryRecord,
    RegistryEntryStateRecord,
    RegistryFreshnessRecord,
    VersionLineageRecord,
)


def build_registry_entry(
    entry_family: str,
    target_ref: str,
    version_ref: str,
    lineage_refs: VersionLineageRecord,
    valid_until: datetime,
) -> RegistryEntryRecord:
    now = datetime.now(timezone.utc)

    state_ref = RegistryEntryStateRecord(
        state="drafted", state_reason="Initial creation", updated_at=now
    )

    freshness = RegistryFreshnessRecord(
        last_verified_at=now, valid_until=valid_until, is_stale=False
    )

    return RegistryEntryRecord(
        registry_entry_id=f"entry_{uuid.uuid4().hex[:8]}",
        entry_family=entry_family,
        target_ref=target_ref,
        version_ref=version_ref,
        state_ref=state_ref,
        lineage_refs=lineage_refs,
        discoverability_state="discoverable_review_only",
        freshness_state=freshness,
        supersession_state=None,
        warnings=[],
    )
