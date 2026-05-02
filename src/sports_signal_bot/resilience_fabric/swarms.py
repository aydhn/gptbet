from datetime import datetime, timezone
from typing import List, Dict, Any
from src.sports_signal_bot.resilience_fabric.contracts import MirrorSwarmRecord, SwarmAgreementRecord

def evaluate_swarm_agreement(swarm: MirrorSwarmRecord, member_observations: Dict[str, Any], stale_members: List[str]) -> SwarmAgreementRecord:
    active_members = [m for m in swarm.member_mirror_refs if m not in stale_members]

    if not active_members:
        return SwarmAgreementRecord(
            swarm_id=swarm.swarm_id,
            agreement_result="quorum_failed",
            participating_members=[],
            stale_members_excluded=stale_members,
            timestamp=datetime.now(timezone.utc),
            details={"reason": "No active members"}
        )

    # Simple agreement logic: check if all active members have the same observation
    first_obs = member_observations.get(active_members[0])
    all_agree = all(member_observations.get(m) == first_obs for m in active_members)

    if all_agree:
        result = "unanimous_agreement"
    else:
        result = "split_observation"

    return SwarmAgreementRecord(
        swarm_id=swarm.swarm_id,
        agreement_result=result,
        participating_members=active_members,
        stale_members_excluded=stale_members,
        timestamp=datetime.now(timezone.utc),
        details={"observations": member_observations}
    )

def detect_split_brain_suspicion(agreement: SwarmAgreementRecord) -> str:
    if agreement.agreement_result == "split_observation":
        return "suspected_split_brain"
    return "no_split_brain"
