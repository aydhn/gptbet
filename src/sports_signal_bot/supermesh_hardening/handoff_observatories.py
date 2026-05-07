from typing import List
from .contracts import PlanetaryHandoffObservatoryRecord, HandoffObservatoryWindowRecord

def build_planetary_handoff_observatory(observatory_id: str, family: str) -> PlanetaryHandoffObservatoryRecord:
    return PlanetaryHandoffObservatoryRecord(
        planetary_handoff_observatory_id=observatory_id,
        observatory_family=family,
        observatory_status="observatory_verified"
    )

def register_observatory_window(observatory: PlanetaryHandoffObservatoryRecord, window: HandoffObservatoryWindowRecord):
    observatory.window_refs.append(window.window_id)
    if window.is_ownerless:
        observatory.observatory_status = "observatory_gapped"

def verify_handoff_observatory(observatory: PlanetaryHandoffObservatoryRecord) -> str:
    return observatory.observatory_status

def summarize_planetary_handoff_observatory(observatory: PlanetaryHandoffObservatoryRecord) -> dict:
    return {
        "id": observatory.planetary_handoff_observatory_id,
        "family": observatory.observatory_family,
        "status": observatory.observatory_status,
        "window_count": len(observatory.window_refs),
        "replay_count": len(observatory.replay_refs),
        "gap_count": len(observatory.gap_refs)
    }
