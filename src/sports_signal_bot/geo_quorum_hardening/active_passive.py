from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any
from src.sports_signal_bot.geo_quorum_hardening.contracts import ActivePassiveRehearsalRecord

def build_active_passive_rehearsal(inputs: Dict[str, Any]) -> ActivePassiveRehearsalRecord:
    warnings = []
    status = "rehearsal_honest"
    if inputs.get("passive_stale"):
        warnings.append("Passive target is stale, cannot serve as a strong fallback.")
        status = "rehearsal_blocked"
    if inputs.get("unmeasured_readiness"):
        warnings.append("Passive readiness is assumed, not measured.")
        status = "rehearsal_caveated"
    if not inputs.get("explicit_rollback_path"):
        warnings.append("Explicit rollback path missing.")
        status = "rehearsal_review_only"

    return ActivePassiveRehearsalRecord(
        active_passive_rehearsal_id=f"apr-{uuid.uuid4().hex[:8]}",
        rehearsal_family=inputs.get("family", "active_to_passive_failover_rehearsal"),
        active_region_ref=inputs.get("active_region", ""),
        passive_region_ref=inputs.get("passive_region", ""),
        readiness_refs=inputs.get("readiness", []),
        lag_refs=inputs.get("lags", []),
        fallback_refs=inputs.get("fallbacks", []),
        residue_refs=inputs.get("residues", []),
        rehearsal_status=status,
        warnings=warnings,
        created_at=datetime.now(timezone.utc)
    )
