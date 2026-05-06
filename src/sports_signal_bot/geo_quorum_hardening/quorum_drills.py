from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any
from src.sports_signal_bot.geo_quorum_hardening.contracts import RegionalQuorumDrillRecord

def build_regional_quorum_drill(inputs: Dict[str, Any]) -> RegionalQuorumDrillRecord:
    warnings = []
    status = "quorum_verified"
    if not inputs.get("explicit_evidence"):
        warnings.append("Quorum sufficiency lacks explicit evidence.")
        status = "quorum_caveated"
    if inputs.get("stale_member_present"):
        warnings.append("Stale member cannot contribute to strong quorum.")
        status = "quorum_blocked"
    if inputs.get("unresolved_residue"):
        warnings.append("Unresolved residue found.")
        status = "quorum_review_only"

    return RegionalQuorumDrillRecord(
        quorum_drill_id=f"rqd-{uuid.uuid4().hex[:8]}",
        drill_family=inputs.get("family", "regional_quorum_loss_drill"),
        region_refs=inputs.get("regions", []),
        member_refs=inputs.get("members", []),
        window_refs=inputs.get("windows", []),
        decision_refs=inputs.get("decisions", []),
        gap_refs=inputs.get("gaps", []),
        residue_refs=inputs.get("residues", []),
        recovery_refs=inputs.get("recoveries", []),
        quorum_status=status,
        warnings=warnings,
        created_at=datetime.now(timezone.utc)
    )
