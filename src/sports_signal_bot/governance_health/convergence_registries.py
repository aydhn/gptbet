import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    SuccessorConvergenceRegistryRecord,
    ConvergenceRegistryEntryRecord
)

def build_successor_convergence_registry(
    registry_family: str
) -> SuccessorConvergenceRegistryRecord:
    return SuccessorConvergenceRegistryRecord(
        convergence_registry_id=f"conv_reg_{uuid.uuid4().hex[:8]}",
        registry_family=registry_family, # type: ignore
        health_status="initializing"
    )

def register_convergence_entry(
    registry: SuccessorConvergenceRegistryRecord,
    source_successor_case_ref: str,
    candidate_successor_refs: List[str]
) -> ConvergenceRegistryEntryRecord:
    entry = ConvergenceRegistryEntryRecord(
        convergence_entry_id=f"c_entry_{uuid.uuid4().hex[:8]}",
        source_successor_case_ref=source_successor_case_ref,
        candidate_successor_refs=candidate_successor_refs,
        convergence_band="weak_convergence",
        currentness_state="evaluating"
    )
    registry.entry_refs.append(entry.convergence_entry_id)
    if source_successor_case_ref not in registry.tracked_successor_refs:
        registry.tracked_successor_refs.append(source_successor_case_ref)
    return entry

def compute_convergence_band(
    entry: ConvergenceRegistryEntryRecord,
    evidence_quality: str,
    replay_status: str,
    staleness: bool
) -> str:
    if staleness:
        band = "stale_convergence"
    elif replay_status == "mismatched":
        band = "no_convergence"
    elif not entry.selected_successor_ref and evidence_quality not in ['low', 'medium', 'high']:
        band = "weak_convergence"
    elif evidence_quality == "low":
        band = "bounded_convergence"
    elif evidence_quality == "medium" or replay_status == "caveated":
        band = "strong_convergence_with_caveats"
    else:
        band = "stable_convergence"

    entry.convergence_band = band # type: ignore
    return band

def summarize_convergence_registry(
    registry: SuccessorConvergenceRegistryRecord,
    entries: List[ConvergenceRegistryEntryRecord]
) -> Dict[str, Any]:

    bands = {
        "no_convergence": 0,
        "weak_convergence": 0,
        "bounded_convergence": 0,
        "strong_convergence_with_caveats": 0,
        "stable_convergence": 0,
        "stale_convergence": 0
    }

    for entry in entries:
        bands[entry.convergence_band] += 1

    total = len(entries)
    if total == 0:
        health = "empty"
    elif bands["stale_convergence"] > 0 or bands["no_convergence"] > 0:
        health = "degraded"
    elif bands["weak_convergence"] > total * 0.5:
        health = "fragile"
    else:
        health = "stable"

    registry.health_status = health

    return {
        "registry_id": registry.convergence_registry_id,
        "family": registry.registry_family,
        "entry_count": total,
        "health_status": health,
        "band_distribution": bands
    }
