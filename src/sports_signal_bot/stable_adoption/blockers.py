from typing import List, Dict, Any, Optional
import datetime
from .contracts import AdoptionBlockerRecord, StableAdoptionRecord

def detect_adoption_conflicts(adoption_id: str, active_adoptions: List[StableAdoptionRecord]) -> List[AdoptionBlockerRecord]:
    conflicts = []
    current_adoption = next((a for a in active_adoptions if a.adoption_id == adoption_id), None)
    if not current_adoption:
        return conflicts

    for a in active_adoptions:
        if a.adoption_id != adoption_id and a.current_status not in ["adoption_completed", "adoption_rejected", "adoption_superseded", "rollback_executed"]:
            if a.target_component_family == current_adoption.target_component_family:
                conflicts.append(AdoptionBlockerRecord(
                    blocker_id=f"blk_conflict_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
                    adoption_id=adoption_id,
                    blocker_family="family_freeze_active",
                    severity="critical",
                    reversibility="hard_block",
                    description=f"Simultaneous adoption in same family: {a.adoption_id}"
                ))
            elif a.proposed_stable_pointer_target == current_adoption.proposed_stable_pointer_target:
                conflicts.append(AdoptionBlockerRecord(
                    blocker_id=f"blk_conflict_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
                    adoption_id=adoption_id,
                    blocker_family="same_rollback_target_ambiguity",
                    severity="critical",
                    reversibility="hard_block",
                    description=f"Ambiguous rollback target due to adoption: {a.adoption_id}"
                ))
    return conflicts

def detect_superseding_adoption(adoption_id: str, candidate_release_id: str, active_adoptions: List[StableAdoptionRecord]) -> Optional[AdoptionBlockerRecord]:
    current_adoption = next((a for a in active_adoptions if a.adoption_id == adoption_id), None)
    if not current_adoption:
        return None
    for a in active_adoptions:
        if a.adoption_id != adoption_id and a.target_component_family == current_adoption.target_component_family:
            if a.candidate_release_id > candidate_release_id: # simulated freshness check
                return AdoptionBlockerRecord(
                    blocker_id=f"blk_supersede_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
                    adoption_id=adoption_id,
                    blocker_family="superseded_candidate",
                    severity="critical",
                    reversibility="hard_block",
                    description=f"Newer safer candidate {a.candidate_release_id} supersedes {candidate_release_id}"
                )
    return None

def block_conflicting_adoptions(adoption_id: str, active_adoptions: List[StableAdoptionRecord]) -> List[AdoptionBlockerRecord]:
    blockers = detect_adoption_conflicts(adoption_id, active_adoptions)
    current = next((a for a in active_adoptions if a.adoption_id == adoption_id), None)
    if current:
        superseded = detect_superseding_adoption(adoption_id, current.candidate_release_id, active_adoptions)
        if superseded:
            blockers.append(superseded)
    return blockers

def explain_adoption_supersession(blocker: AdoptionBlockerRecord) -> str:
    return f"Adoption superseded: {blocker.description} (Severity: {blocker.severity})"

def collect_rollback_blockers(adoption_id: str, previous_stable_ref: Optional[str]) -> List[AdoptionBlockerRecord]:
    blockers = []
    if not previous_stable_ref:
        blockers.append(AdoptionBlockerRecord(
            blocker_id=f"blk_rollback_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
            adoption_id=adoption_id,
            blocker_family="missing_rollback_target",
            severity="critical",
            reversibility="hard_block",
            description="No previous stable snapshot reference known for safe rollback."
        ))
    return blockers
