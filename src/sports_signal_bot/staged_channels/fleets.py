import uuid
from typing import List, Dict, Any
from .contracts import CandidateFleetRecord, FleetConflictRecord

def build_candidate_fleet(candidates: List[str], description: str) -> CandidateFleetRecord:
    return CandidateFleetRecord(
        fleet_id=str(uuid.uuid4()),
        description=description,
        members=candidates,
        fleet_policy="default"
    )

def detect_fleet_conflicts(fleet: CandidateFleetRecord, candidate_metadata: Dict[str, Any]) -> List[FleetConflictRecord]:
    conflicts = []

    # 1. Capacity logic based on members count
    if len(fleet.members) > 5:
        conflicts.append(FleetConflictRecord(
            conflict_id=str(uuid.uuid4()),
            involved_candidates=fleet.members[:2],
            conflict_type="capacity_warning",
            severity="low",
            description="Fleet is getting large"
        ))

    # 2. Logic checking metadata targets
    seen_targets = {}
    for cand in fleet.members:
        target = candidate_metadata.get(cand, {}).get("target_family")
        if target:
            if target in seen_targets:
                conflicts.append(FleetConflictRecord(
                    conflict_id=str(uuid.uuid4()),
                    involved_candidates=[seen_targets[target], cand],
                    conflict_type="target_conflict",
                    severity="high",
                    description=f"Multiple candidates targeting the same family: {target}"
                ))
            else:
                seen_targets[target] = cand

    return conflicts

def suppress_conflicting_assignments(conflicts: List[FleetConflictRecord]) -> List[str]:
    suppressed = []
    for c in conflicts:
        if c.severity == "high":
            suppressed.extend(c.involved_candidates)
    return list(set(suppressed))
