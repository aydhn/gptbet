from typing import List, Dict, Any, Optional
from sports_signal_bot.overlay_mesh_governance.contracts import (
    ControllerTierCapRecord,
    ControllerConsortiumActionRecord,
    ControllerBaselineRegistryActionRecord,
    ControllerRecoveryPathRecord
)

def extend_resilience_controller_with_registry_inputs(controller_id: str, registry_refs: List[str]) -> Dict[str, Any]:
    return {
        "controller_id": controller_id,
        "monitored_registries": registry_refs,
        "status": "extended"
    }

def apply_controller_caps_to_route_governance(route_ref: str, caps: List[ControllerTierCapRecord]) -> str:
    if caps:
        # e.g., downgrade to review_only if capped
        return "capped_to_review_only"
    return "unbounded"

def summarize_controller_extended_actions(actions: List[ControllerConsortiumActionRecord]) -> Dict[str, Any]:
    return {
        "total_actions": len(actions),
        "action_types": [a.action_type for a in actions]
    }
