from typing import Dict, Any, List, Optional
import uuid
from .contracts import PlanePressureRecord, PressureBand

def compute_local_plane_pressure(plane_id: str, drivers: Dict[str, float]) -> PlanePressureRecord:
    score = sum(drivers.values()) / max(len(drivers), 1)
    return PlanePressureRecord(
        pressure_id=f"pres_{uuid.uuid4().hex[:8]}",
        plane_id=plane_id,
        pressure_score=score,
        drivers=drivers
    )

def fuse_plane_pressures(pressures: List[PlanePressureRecord]) -> float:
    if not pressures:
        return 0.0
    return sum(p.pressure_score for p in pressures) / len(pressures)

def detect_disproportionate_plane_pressure(pressures: List[PlanePressureRecord], threshold: float = 0.8) -> List[str]:
    return [p.plane_id for p in pressures if p.pressure_score > threshold]

def highlight_pressure_outliers(pressures: List[PlanePressureRecord]) -> Dict[str, float]:
    if not pressures:
        return {}
    avg = fuse_plane_pressures(pressures)
    return {p.plane_id: p.pressure_score for p in pressures if p.pressure_score > avg * 1.5}
