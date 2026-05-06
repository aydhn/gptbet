from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any
from src.sports_signal_bot.geo_quorum_hardening.contracts import GlobalOperatorCoverageSynthesisRecord

def build_global_operator_coverage_synthesis(inputs: Dict[str, Any]) -> GlobalOperatorCoverageSynthesisRecord:
    warnings = []
    status = "coverage_synthesized"
    if inputs.get("ownerless_critical_window"):
        warnings.append("Critical window lacks explicit owner.")
        status = "coverage_blocked"
    if inputs.get("escalation_unreachable"):
        warnings.append("Escalation path is unreachable.")
        status = "coverage_gapped"
    if inputs.get("stale_calendar_data"):
        warnings.append("Stale calendar data cannot form strong synthesis basis.")
        status = "coverage_caveated"

    return GlobalOperatorCoverageSynthesisRecord(
        coverage_synthesis_id=f"gocs-{uuid.uuid4().hex[:8]}",
        synthesis_family=inputs.get("family", "global_oncall_coverage_synthesis"),
        region_refs=inputs.get("regions", []),
        window_refs=inputs.get("windows", []),
        owner_refs=inputs.get("owners", []),
        seam_refs=inputs.get("seams", []),
        overlap_refs=inputs.get("overlaps", []),
        gap_refs=inputs.get("gaps", []),
        escalation_reachability_refs=inputs.get("escalations", []),
        synthesis_status=status,
        warnings=warnings,
        created_at=datetime.now(timezone.utc)
    )
