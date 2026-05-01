from typing import Dict, Any, List, Optional
from .contracts import (
    ControlPlaneRecord, PlanePrecedence, PlaneHealthBand, PlaneTrustBand
)

def resolve_plane_precedence(plane_a: ControlPlaneRecord, plane_b: ControlPlaneRecord) -> ControlPlaneRecord:
    """Returns the plane with higher precedence."""
    if plane_a.precedence.value < plane_b.precedence.value:
        return plane_a
    elif plane_b.precedence.value < plane_a.precedence.value:
        return plane_b
    else:
        # Same precedence level, default to A for now or handle via tie-breaker
        return plane_a

def validate_parent_child_governance(parent: ControlPlaneRecord, child: ControlPlaneRecord) -> bool:
    """Validates that a parent-child relationship is valid."""
    if child.parent_plane_id != parent.plane_id:
        return False
    if child.precedence.value <= parent.precedence.value:
        return False
    return True

def explain_hierarchy_resolution(plane_a: ControlPlaneRecord, plane_b: ControlPlaneRecord) -> str:
    winner = resolve_plane_precedence(plane_a, plane_b)
    return f"Plane {winner.plane_id} ({winner.precedence.name}) wins over the other plane due to precedence rank."

def block_lower_plane_conflict_with_higher_plane(lower: ControlPlaneRecord, higher: ControlPlaneRecord) -> bool:
    """Returns True if the lower plane's action should be blocked."""
    winner = resolve_plane_precedence(lower, higher)
    return winner.plane_id == higher.plane_id

def compute_plane_health(escalation_rate: float, conflict_density: float) -> PlaneHealthBand:
    if escalation_rate > 0.5 or conflict_density > 0.5:
        return PlaneHealthBand.UNSTABLE
    if escalation_rate > 0.3 or conflict_density > 0.3:
        return PlaneHealthBand.STRESSED
    if escalation_rate > 0.1 or conflict_density > 0.1:
        return PlaneHealthBand.NOISY
    return PlaneHealthBand.HEALTHY

def compute_plane_trust(health: PlaneHealthBand, budget_violations: int) -> PlaneTrustBand:
    if health == PlaneHealthBand.UNSTABLE or budget_violations > 2:
        return PlaneTrustBand.LOW
    if health == PlaneHealthBand.STRESSED or budget_violations > 0:
        return PlaneTrustBand.LIMITED_AUTONOMY_ONLY
    if health == PlaneHealthBand.NOISY:
        return PlaneTrustBand.MEDIUM
    return PlaneTrustBand.HIGH

def summarize_plane_health_trust(plane: ControlPlaneRecord) -> str:
    return f"Plane {plane.plane_id} - Health: {plane.health.value}, Trust: {plane.trust.value}"
