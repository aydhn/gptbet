from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import SovereignRuntimeCorridorRecord

def build_corridor(
    corridor_id: str,
    source_region: str,
    target_region: str,
    family: str,
    treaty_ref: str = None
) -> SovereignRuntimeCorridorRecord:
    return SovereignRuntimeCorridorRecord(
        corridor_id=corridor_id,
        corridor_family=family,
        source_region_ref=source_region,
        target_region_ref=target_region,
        treaty_ref=treaty_ref,
        corridor_status="corridor_defined"
    )

def collect_corridor_blockers(corridor: SovereignRuntimeCorridorRecord) -> List[str]:
    blockers = []
    if corridor.corridor_status == "corridor_blocked":
        blockers.append("corridor explicitly blocked")
    return blockers

def summarize_corridor_transition(corridor: SovereignRuntimeCorridorRecord) -> Dict[str, Any]:
    return {
        "id": corridor.corridor_id,
        "family": corridor.corridor_family,
        "status": corridor.corridor_status,
        "source": corridor.source_region_ref,
        "target": corridor.target_region_ref
    }
