from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    EcosystemResilienceControllerRecord,
    ResilienceControllerState
)

def build_ecosystem_resilience_controller(
    controller_id: str,
    controller_family: str,
    monitored_overlay_refs: List[str],
    monitored_mesh_refs: List[str]
) -> EcosystemResilienceControllerRecord:
    return EcosystemResilienceControllerRecord(
        controller_id=controller_id,
        controller_family=controller_family,
        monitored_overlay_refs=monitored_overlay_refs,
        monitored_mesh_refs=monitored_mesh_refs,
        monitored_signal_catalog_refs=[],
        monitored_ecosystem_refs=[],
        decision_policy_ref="default_policy",
        current_state=ResilienceControllerState.MONITORING_NORMAL,
        warnings=[]
    )

def evaluate_controller_signals(controller: EcosystemResilienceControllerRecord, mesh_health: str, signal_count: int) -> str:
    if mesh_health == "critical":
        return "trigger_degraded"
    if mesh_health == "pressured":
        return "trigger_caution"
    return "ok"

def trigger_controller_decision(controller: EcosystemResilienceControllerRecord, evaluation: str) -> EcosystemResilienceControllerRecord:
    if evaluation == "trigger_degraded":
        controller.current_state = ResilienceControllerState.DEGRADED_STATE
        controller.warnings.append("Controller entered degraded state.")
    elif evaluation == "trigger_caution":
        controller.current_state = ResilienceControllerState.CAUTION_STATE
    else:
        controller.current_state = ResilienceControllerState.MONITORING_NORMAL
    return controller

def apply_visibility_or_projection_downgrade(controller: EcosystemResilienceControllerRecord) -> str:
    if controller.current_state in [ResilienceControllerState.DEGRADED_STATE, ResilienceControllerState.BLOCKED_STATE]:
        return "visibility_downgraded"
    return "visibility_normal"

def summarize_controller_state(controller: EcosystemResilienceControllerRecord) -> str:
    return f"Controller {controller.controller_id}: {controller.current_state.value}"
