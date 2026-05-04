from typing import List, Dict, Any
from datetime import datetime, timezone
import uuid
from .contracts import EcosystemResilienceScaleActionRecord, ControllerProjectionCapRecord

def trigger_controller_actions_from_overlay_exchange(exchange_health: str) -> List[EcosystemResilienceScaleActionRecord]:
    actions = []
    if exchange_health == "degraded":
        cap = ControllerProjectionCapRecord(
            cap_id=f"cap-{uuid.uuid4().hex[:8]}",
            target_dimension="route_preference",
            max_value=0.5,
            reason="exchange_degraded"
        )
        actions.append(EcosystemResilienceScaleActionRecord(
            action_id=f"act-{uuid.uuid4().hex[:8]}",
            action_type="apply_projection_cap",
            target_ref="mesh-partition",
            applied_caps=[cap],
            reason="Exchange health is degraded, capping projection strength",
            timestamp=datetime.now(timezone.utc)
        ))
    return actions
