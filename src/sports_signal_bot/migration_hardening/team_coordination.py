from pydantic import Field
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .contracts import DrillFamily, ReadinessStatus

class TeamRoleRecord(BaseModel):
    role_id: str
    role_family: str
    owner: Optional[str] = None

class CoordinationHandoffRecord(BaseModel):
    handoff_id: str
    from_role: str
    to_role: str
    details: str
    is_acknowledged: bool = False
    freshness_note_preserved: bool = False

class CoordinationGapRecord(BaseModel):
    gap_id: str
    description: str

class CoordinationResidueRecord(BaseModel):
    residue_id: str
    description: str

class CoordinationWarningRecord(BaseModel):
    warning_id: str
    description: str

class MultiTeamCoordinationDrillRecord(BaseModel):
    coordination_drill_id: str
    drill_family: DrillFamily
    team_role_refs: List[TeamRoleRecord] = Field(default_factory=list)
    handoff_refs: List[CoordinationHandoffRecord] = Field(default_factory=list)
    gap_refs: List[CoordinationGapRecord] = Field(default_factory=list)
    residue_refs: List[CoordinationResidueRecord] = Field(default_factory=list)
    readiness_status: ReadinessStatus = ReadinessStatus.coordination_gapped
    warnings: List[CoordinationWarningRecord] = Field(default_factory=list)

def build_multi_team_coordination_drill(drill_id: str, family: DrillFamily) -> MultiTeamCoordinationDrillRecord:
    return MultiTeamCoordinationDrillRecord(
        coordination_drill_id=drill_id,
        drill_family=family
    )

def register_team_role(drill: MultiTeamCoordinationDrillRecord, role: TeamRoleRecord) -> None:
    drill.team_role_refs.append(role)
    if not role.owner:
        drill.gap_refs.append(CoordinationGapRecord(
            gap_id=f"gap_ownerless_{role.role_id}",
            description=f"Role {role.role_family} has no explicit owner."
        ))

def execute_coordination_handoff(drill: MultiTeamCoordinationDrillRecord, handoff: CoordinationHandoffRecord) -> None:
    drill.handoff_refs.append(handoff)
    if not handoff.is_acknowledged:
        drill.gap_refs.append(CoordinationGapRecord(
            gap_id=f"gap_no_ack_{handoff.handoff_id}",
            description=f"Handoff {handoff.handoff_id} not acknowledged."
        ))
    if not handoff.freshness_note_preserved:
        drill.warnings.append(CoordinationWarningRecord(
            warning_id=f"warn_freshness_lost_{handoff.handoff_id}",
            description=f"Freshness note lost in handoff {handoff.handoff_id}."
        ))

def detect_coordination_gaps(drill: MultiTeamCoordinationDrillRecord) -> None:
    if drill.gap_refs:
        drill.readiness_status = ReadinessStatus.coordination_gapped
    elif drill.warnings:
        drill.readiness_status = ReadinessStatus.coordination_caveated
    else:
        drill.readiness_status = ReadinessStatus.coordination_verified

def summarize_multi_team_coordination(drill: MultiTeamCoordinationDrillRecord) -> Dict:
    return {
        "drill_id": drill.coordination_drill_id,
        "family": drill.drill_family.value,
        "status": drill.readiness_status.value,
        "handoffs_count": len(drill.handoff_refs),
        "gaps_count": len(drill.gap_refs)
    }
