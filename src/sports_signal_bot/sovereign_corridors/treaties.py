from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import (
    TreatyBackedRemediationCorridorRecord,
    SovereignRuntimeCorridorRecord
)

def build_treaty_backed_corridor(
    treaty_ref: str,
    corridor_ref: str,
    limitations: Dict[str, Any]
) -> TreatyBackedRemediationCorridorRecord:
    return TreatyBackedRemediationCorridorRecord(
        treaty_ref=treaty_ref,
        corridor_ref=corridor_ref,
        limitations=limitations
    )

def validate_corridor_against_treaty(corridor: SovereignRuntimeCorridorRecord, treaty: Dict[str, Any]) -> bool:
    if corridor.treaty_ref and corridor.treaty_ref != treaty.get("treaty_id"):
        return False
    return True

def map_treaty_rules_to_corridor(treaty: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "allowed_families": treaty.get("allowed_families", []),
        "review_required": treaty.get("review_required", True)
    }

def summarize_treaty_backed_corridor(record: TreatyBackedRemediationCorridorRecord) -> Dict[str, Any]:
    return {
        "treaty": record.treaty_ref,
        "corridor": record.corridor_ref,
        "limit_count": len(record.limitations)
    }

def project_treaty_into_corridor_limits(treaty: Dict[str, Any]) -> Dict[str, Any]:
    return map_treaty_rules_to_corridor(treaty)

def invalidate_corridor_on_treaty_expiry(corridor: SovereignRuntimeCorridorRecord, treaty: Dict[str, Any]) -> SovereignRuntimeCorridorRecord:
    if treaty.get("expired", False):
        corridor.corridor_status = "corridor_expired"
        corridor.warnings.append("Treaty expired")
    return corridor

def summarize_treaty_corridor_alignment(corridor: SovereignRuntimeCorridorRecord, treaty: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "aligned": validate_corridor_against_treaty(corridor, treaty),
        "treaty_ref": treaty.get("treaty_id")
    }
