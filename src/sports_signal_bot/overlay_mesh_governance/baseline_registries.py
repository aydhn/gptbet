from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sports_signal_bot.overlay_mesh_governance.contracts import (
    SovereignResilienceBaselineRegistryRecord,
    BaselineRegistryEntryRecord,
    BaselineRegistryHealthRecord,
    BaselineRegistryCurrentPointerRecord,
    BaselineRegistryApplicabilityRecord,
    BaselineRegistrySupersessionRecord
)

def build_baseline_registry(registry_id: str, family: str) -> SovereignResilienceBaselineRegistryRecord:
    return SovereignResilienceBaselineRegistryRecord(
        baseline_registry_id=registry_id,
        registry_family=family,
        registered_baseline_refs=[],
        current_pointer_refs=[],
        applicability_refs=[],
        validation_refs=[],
        supersession_refs=[],
        health_status=BaselineRegistryHealthRecord(status="healthy", details={})
    )

def register_baseline_entry(registry: SovereignResilienceBaselineRegistryRecord, entry: BaselineRegistryEntryRecord) -> SovereignResilienceBaselineRegistryRecord:
    if entry.baseline_registry_entry_id not in registry.registered_baseline_refs:
        registry.registered_baseline_refs.append(entry.baseline_registry_entry_id)
    return registry

def validate_baseline_currentness(entry: BaselineRegistryEntryRecord) -> str:
    now = datetime.now(timezone.utc)
    if "end" in entry.validity_window and entry.validity_window["end"] < now:
        entry.currentness_state = "expired"
        return "expired"
    if entry.supersession_state.successor_ref is not None:
        entry.currentness_state = "superseded"
        return "superseded"
    return entry.currentness_state

def compute_baseline_registry_health(registry: SovereignResilienceBaselineRegistryRecord) -> BaselineRegistryHealthRecord:
    if len(registry.warnings) > 0:
        registry.health_status.status = "degraded"
    else:
        registry.health_status.status = "healthy"
    return registry.health_status

def summarize_baseline_registry(registry: SovereignResilienceBaselineRegistryRecord) -> Dict[str, Any]:
    return {
        "registry_id": registry.baseline_registry_id,
        "entry_count": len(registry.registered_baseline_refs),
        "health": registry.health_status.status
    }

def compute_baseline_applicability(entry: BaselineRegistryEntryRecord, context_scopes: List[str]) -> float:
    match_count = sum(1 for s in context_scopes if s in entry.applicability_scope.applicability_scopes)
    if not context_scopes: return 1.0
    return match_count / len(context_scopes)

def validate_baseline_scope_match(entry: BaselineRegistryEntryRecord, scope: str) -> bool:
    return scope in entry.applicability_scope.applicability_scopes

def downgrade_baseline_hint_on_scope_mismatch(entry: BaselineRegistryEntryRecord) -> str:
    if entry.currentness_state == "current":
        return "current_with_caveats"
    return entry.currentness_state

def summarize_baseline_applicability(entry: BaselineRegistryEntryRecord) -> Dict[str, Any]:
    return {
        "entry_id": entry.baseline_registry_entry_id,
        "scopes": entry.applicability_scope.applicability_scopes
    }

def supersede_baseline_registry_entry(entry: BaselineRegistryEntryRecord, successor_ref: str, reason: str) -> BaselineRegistryEntryRecord:
    entry.supersession_state = BaselineRegistrySupersessionRecord(
        supersession_reason=reason,
        successor_ref=successor_ref
    )
    entry.currentness_state = "superseded"
    return entry

def link_successor_baseline(old_entry: BaselineRegistryEntryRecord, new_entry: BaselineRegistryEntryRecord) -> None:
    supersede_baseline_registry_entry(old_entry, new_entry.baseline_registry_entry_id, "stronger baseline revision")

def project_supersession_into_overlays_and_mesh(entry: BaselineRegistryEntryRecord) -> List[str]:
    # Returns list of impacted components
    return [f"overlay_{entry.baseline_ref}"]

def summarize_baseline_supersession(entry: BaselineRegistryEntryRecord) -> Dict[str, Any]:
    return {
        "entry_id": entry.baseline_registry_entry_id,
        "is_superseded": entry.currentness_state == "superseded",
        "successor": entry.supersession_state.successor_ref
    }

def enforce_sovereignty_in_baseline_registry(entry: BaselineRegistryEntryRecord) -> bool:
    # Returns True if block enforced
    if "sovereignty_block" in entry.applicability_scope.applicability_scopes:
        return True
    return False

def downgrade_baseline_by_sovereignty(entry: BaselineRegistryEntryRecord) -> BaselineRegistryEntryRecord:
    if entry.currentness_state == "current":
        entry.currentness_state = "review_only_current"
    return entry

def explain_sovereignty_baseline_interaction(entry: BaselineRegistryEntryRecord) -> str:
    return f"Entry {entry.baseline_registry_entry_id} currentness: {entry.currentness_state} due to sovereignty evaluation."
