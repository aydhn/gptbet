from typing import Any, Dict, List

from .contracts import ActiveActiveRehearsalRecord


def build_active_active_rehearsal(
    rehearsal_id: str, family: str
) -> ActiveActiveRehearsalRecord:
    return ActiveActiveRehearsalRecord(
        active_active_rehearsal_id=rehearsal_id,
        rehearsal_family=family,
        region_pair_refs=[],
        symmetry_refs=[],
        divergence_refs=[],
        conflict_refs=[],
        fallback_refs=[],
        residue_refs=[],
        rehearsal_status="rehearsal_honest",
        warnings=[],
    )


def compare_region_symmetry(rehearsal: ActiveActiveRehearsalRecord, symmetry_id: str):
    rehearsal.symmetry_refs.append(symmetry_id)
    return rehearsal


def detect_rehearsal_divergence(
    rehearsal: ActiveActiveRehearsalRecord, divergence_id: str
):
    rehearsal.divergence_refs.append(divergence_id)
    rehearsal.rehearsal_status = "rehearsal_caveated"
    return rehearsal


def summarize_active_active_rehearsal(
    rehearsal: ActiveActiveRehearsalRecord,
) -> Dict[str, Any]:
    return {
        "rehearsal_id": rehearsal.active_active_rehearsal_id,
        "status": rehearsal.rehearsal_status,
        "symmetry_checks": len(rehearsal.symmetry_refs),
        "divergences": len(rehearsal.divergence_refs),
    }
