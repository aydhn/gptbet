from datetime import datetime, timezone
import uuid
from typing import List, Optional
from .contracts import (
    RegistryEntryRecord,
    CurrentnessDecisionRecord,
    RegistrySupersessionLinkRecord,
    RegistryEntryStateRecord,
)


def compute_currentness(entry: RegistryEntryRecord) -> CurrentnessDecisionRecord:
    now = datetime.now(timezone.utc)
    caveats = []

    if entry.freshness_state.valid_until < now:
        entry.freshness_state.is_stale = True
        return CurrentnessDecisionRecord(
            is_current=False,
            caveats=["Entry is expired (stale freshness)."],
            decided_at=now,
        )

    if entry.supersession_state is not None:
        return CurrentnessDecisionRecord(
            is_current=False, caveats=["Entry has been superseded."], decided_at=now
        )

    if entry.state_ref.state not in ["current", "current_with_caveats"]:
        return CurrentnessDecisionRecord(
            is_current=False,
            caveats=[f"Entry state is {entry.state_ref.state}, not current."],
            decided_at=now,
        )

    if entry.state_ref.state == "current_with_caveats":
        caveats.append("Entry is current but carries warnings/caveats.")

    return CurrentnessDecisionRecord(is_current=True, caveats=caveats, decided_at=now)


def supersede_registry_entry(
    old_entry: RegistryEntryRecord, new_entry_ref: str, reason: str
) -> RegistryEntryRecord:
    now = datetime.now(timezone.utc)

    old_entry.supersession_state = RegistrySupersessionLinkRecord(
        superseded_by_ref=new_entry_ref, supersession_reason=reason, superseded_at=now
    )

    old_entry.state_ref = RegistryEntryStateRecord(
        state="superseded",
        state_reason=f"Superseded by {new_entry_ref}",
        updated_at=now,
    )

    return old_entry


def version_registry_entry(
    entry: RegistryEntryRecord, new_version_ref: str
) -> RegistryEntryRecord:
    entry.version_ref = new_version_ref
    entry.state_ref.updated_at = datetime.now(timezone.utc)
    return entry


def explain_version_and_supersession(entry: RegistryEntryRecord) -> str:
    if entry.supersession_state:
        return f"Entry {entry.registry_entry_id} is SUPERSEDED by {entry.supersession_state.superseded_by_ref} due to {entry.supersession_state.supersession_reason}."
    else:
        return f"Entry {entry.registry_entry_id} is at version {entry.version_ref}."
