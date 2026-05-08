from typing import List, Dict, Optional
import uuid
from .contracts import (
    FinalHardeningConvergenceRecord,
    ConvergenceInputRecord,
    ConvergenceDimensionRecord,
    ConvergenceBlockerRecord,
    ConvergenceCaveatRecord,
    ConvergenceResidueRecord,
    ConvergenceDecisionRecord,
    ConvergenceReplayRecord,
    ConvergenceFreshnessRecord
)

def build_final_hardening_convergence(family: str, inputs: List[ConvergenceInputRecord]) -> FinalHardeningConvergenceRecord:
    has_stale = any(i.is_stale for i in inputs)
    status = "convergence_verified"
    warnings = []

    if has_stale:
        status = "convergence_blocked"
        warnings.append("Stale or superseded inputs cannot form a strong convergence basis.")

    return FinalHardeningConvergenceRecord(
        final_convergence_id=str(uuid.uuid4()),
        convergence_family=family,  # type: ignore
        input_refs=inputs,
        convergence_status=status,
        warnings=warnings
    )

def add_convergence_input(convergence: FinalHardeningConvergenceRecord, new_input: ConvergenceInputRecord) -> FinalHardeningConvergenceRecord:
    convergence.input_refs.append(new_input)
    if new_input.is_stale:
        convergence.convergence_status = "convergence_blocked"
        convergence.warnings.append("Added stale input. Convergence blocked.")
    return convergence

def verify_final_hardening_convergence(convergence: FinalHardeningConvergenceRecord) -> bool:
    for blocker in convergence.blocker_refs:
        if blocker.hidden:
            return False # Blockers cannot be hidden
    for residue in convergence.residue_refs:
        if residue.hidden:
            return False # Residue cannot be hidden
    if convergence.convergence_status == "convergence_blocked":
        return False
    return True

def replay_final_hardening_convergence(convergence: FinalHardeningConvergenceRecord) -> bool:
    if not convergence.replay_refs:
        return False
    for r in convergence.replay_refs:
        if not r.replayable:
            return False
    return True

def summarize_final_hardening_convergence(convergence: FinalHardeningConvergenceRecord) -> Dict:
    return {
        "id": convergence.final_convergence_id,
        "family": convergence.convergence_family,
        "status": convergence.convergence_status,
        "input_count": len(convergence.input_refs),
        "blocker_count": len(convergence.blocker_refs),
        "caveat_count": len(convergence.caveat_refs),
        "residue_count": len(convergence.residue_refs),
        "warnings": convergence.warnings
    }

def detect_convergence_gaps(convergence: FinalHardeningConvergenceRecord) -> List[str]:
    gaps = []
    if not convergence.input_refs:
        gaps.append("No inputs provided.")
    if any(b.hidden for b in convergence.blocker_refs):
        gaps.append("Hidden blockers detected.")
    if any(r.hidden for r in convergence.residue_refs):
        gaps.append("Hidden residue detected.")
    if any(i.is_stale for i in convergence.input_refs):
        gaps.append("Stale inputs detected.")
    return gaps
