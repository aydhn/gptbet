from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import (
    CorridorHealthRecord,
    SovereignRuntimeCorridorRecord
)

def compute_corridor_health(corridor: SovereignRuntimeCorridorRecord, context: Dict[str, Any]) -> CorridorHealthRecord:
    status = "healthy"
    metrics = {
        "gap_burden": 0,
        "translation_drift": 0
    }
    if context.get("has_drift"):
        status = "translation_stressed"
        metrics["translation_drift"] = 1

    return CorridorHealthRecord(
        corridor_ref=corridor.corridor_id,
        health_status=status,
        metrics=metrics
    )

def compare_corridor_health_snapshots(current: CorridorHealthRecord, previous: CorridorHealthRecord) -> Dict[str, Any]:
    return {
        "status_changed": current.health_status != previous.health_status
    }

def summarize_corridor_health_drivers(health: CorridorHealthRecord) -> List[str]:
    drivers = []
    if health.health_status == "translation_stressed":
        drivers.append("Translation drift detected")
    return drivers

def downgrade_corridor_on_gap_pressure(corridor: SovereignRuntimeCorridorRecord, health: CorridorHealthRecord) -> SovereignRuntimeCorridorRecord:
    if health.health_status in ["blocked", "continuity_risk"]:
        corridor.corridor_status = "corridor_degraded"
    return corridor
