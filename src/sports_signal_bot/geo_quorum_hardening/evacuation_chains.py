from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any
from src.sports_signal_bot.geo_quorum_hardening.contracts import RollingEvacuationAuditChainRecord

def build_rolling_evacuation_audit_chain(inputs: Dict[str, Any]) -> RollingEvacuationAuditChainRecord:
    warnings = []
    status = "chain_verified"
    if not inputs.get("explicit_wave_scope"):
        warnings.append("Wave lacks explicit scope.")
        status = "chain_caveated"
    if inputs.get("broken_dependency"):
        warnings.append("Broken dependency detected.")
        status = "chain_broken"
    if not inputs.get("no_safe_continuity_preserved"):
        warnings.append("No-safe continuity is not preserved across chain.")
        status = "chain_blocked"

    return RollingEvacuationAuditChainRecord(
        evacuation_chain_id=f"reac-{uuid.uuid4().hex[:8]}",
        chain_family=inputs.get("family", "regional_evacuate_then_restore_chain"),
        wave_refs=inputs.get("waves", []),
        checkpoint_refs=inputs.get("checkpoints", []),
        dependency_refs=inputs.get("dependencies", []),
        rollback_refs=inputs.get("rollbacks", []),
        residue_refs=inputs.get("residues", []),
        gap_refs=inputs.get("gaps", []),
        continuity_refs=inputs.get("continuities", []),
        chain_status=status,
        warnings=warnings,
        created_at=datetime.now(timezone.utc)
    )
