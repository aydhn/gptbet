from datetime import datetime, timezone
import uuid
from typing import List, Dict
from .contracts import (
    CorridorRegistryRecord,
    RegistryHealthRecordV2,
    RegistryCurrentPointerRecord,
    RegistryEntryRecord,
    RegistryWarningRecord,
)
from .currentness import compute_currentness


def build_corridor_registry(
    registry_family: str, owning_scope_ref: str
) -> CorridorRegistryRecord:
    now = datetime.now(timezone.utc)
    health = RegistryHealthRecordV2(status="healthy", last_evaluated_at=now)
    return CorridorRegistryRecord(
        registry_id=f"registry_{uuid.uuid4().hex[:8]}",
        registry_family=registry_family,
        owning_scope_ref=owning_scope_ref,
        health_status=health,
    )


def register_registry_entry(
    registry: CorridorRegistryRecord, entry: RegistryEntryRecord
) -> CorridorRegistryRecord:
    if entry.entry_family == "corridor_entry":
        registry.registered_corridor_refs.append(entry.registry_entry_id)
    elif entry.entry_family == "treaty_entry":
        registry.registered_treaty_refs.append(entry.registry_entry_id)
    elif entry.entry_family == "continuity_attestation_entry":
        registry.registered_attestation_refs.append(entry.registry_entry_id)
    elif entry.entry_family == "benchmark_baseline_entry":
        registry.registered_baseline_refs.append(entry.registry_entry_id)

    return registry


def validate_registry_entry_state(entry: RegistryEntryRecord) -> bool:
    decision = compute_currentness(entry)
    return decision.is_current


def update_current_pointer(
    registry: CorridorRegistryRecord, scope_ref: str, new_current_entry_ref: str
) -> CorridorRegistryRecord:
    # In a real impl, we'd find the old pointer and overwrite, or maintain history.
    pointer = RegistryCurrentPointerRecord(
        pointer_id=f"ptr_{uuid.uuid4().hex[:8]}",
        registry_family=registry.registry_family,
        scope_ref=scope_ref,
        current_entry_ref=new_current_entry_ref,
        updated_at=datetime.now(timezone.utc),
    )
    registry.current_pointer_refs.append(pointer.pointer_id)
    return registry


def summarize_registry_state(registry: CorridorRegistryRecord) -> Dict:
    return {
        "registry_id": registry.registry_id,
        "family": registry.registry_family,
        "corridors_count": len(registry.registered_corridor_refs),
        "treaties_count": len(registry.registered_treaty_refs),
        "attestations_count": len(registry.registered_attestation_refs),
        "health": registry.health_status.status,
    }
