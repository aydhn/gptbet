from typing import List, Dict, Any
from sports_signal_bot.consistency_ledgers.contracts import (
    DisputeTribunalMeshRecord,
    TribunalMeshFamily,
    TribunalMeshEdgeRecord,
    TribunalMeshEdgeInputRecord,
    TribunalMeshEdgeStatus,
    TribunalMeshPressureRecord,
    MeshPressureState,
    HealthStatus,
)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def build_dispute_tribunal_mesh(
    family: TribunalMeshFamily,
    routing_policy: str,
    escalation_policy: str,
    pressure_policy: str,
) -> DisputeTribunalMeshRecord:
    return DisputeTribunalMeshRecord(
        tribunal_mesh_id=generate_id("trib_mesh"),
        mesh_family=family,
        node_refs=[],
        edge_refs=[],
        case_refs=[],
        routing_policy_ref=routing_policy,
        escalation_policy_ref=escalation_policy,
        pressure_policy_ref=pressure_policy,
        health_status=HealthStatus.HEALTHY,
        warnings=[],
    )


def add_tribunal_mesh_edge(
    mesh: DisputeTribunalMeshRecord, edge_input: TribunalMeshEdgeInputRecord
) -> TribunalMeshEdgeRecord:
    edge = TribunalMeshEdgeRecord(
        edge_id=generate_id("trib_edge"),
        source_node_ref=edge_input.source_node_ref,
        target_node_ref=edge_input.target_node_ref,
        supported_case_families=edge_input.supported_cases,
        supported_scope_classes=edge_input.supported_scopes,
        caveat_transfer_policy=edge_input.caveat_policy,
        currentness_state="current",
        edge_status=TribunalMeshEdgeStatus.EDGE_CURRENT,
        warnings=[],
    )
    mesh.edge_refs.append(edge.edge_id)
    return edge


def validate_tribunal_mesh_edge(
    edge: TribunalMeshEdgeRecord, source_node: Any, target_node: Any
) -> TribunalMeshEdgeRecord:
    """Validates the edge. Scope widening is forbidden."""

    # Check for scope widening
    if (
        "wide" in edge.supported_scope_classes
        and "narrow" in source_node.supported_case_families
    ):
        edge.edge_status = TribunalMeshEdgeStatus.EDGE_BLOCKED
        edge.warnings.append("Scope widening detected. Edge blocked.")

    if (
        source_node.currentness_state != "current"
        or target_node.currentness_state != "current"
    ):
        if edge.edge_status != TribunalMeshEdgeStatus.EDGE_BLOCKED:
            edge.edge_status = TribunalMeshEdgeStatus.EDGE_DEGRADED
            edge.warnings.append("Edge degraded due to stale node(s).")

    return edge


def compute_tribunal_mesh_pressure(
    mesh: DisputeTribunalMeshRecord,
    nodes: Dict[str, Any],
    edges: Dict[str, TribunalMeshEdgeRecord],
) -> TribunalMeshPressureRecord:

    stale_count = sum(
        1 for n in nodes.values() if getattr(n, "currentness_state", "") != "current"
    )
    degraded_edge_count = sum(
        1
        for e in edges.values()
        if e.edge_status == TribunalMeshEdgeStatus.EDGE_DEGRADED
    )

    metrics = {
        "stale_case_density": stale_count / max(1, len(nodes)),
        "degraded_edge_ratio": degraded_edge_count / max(1, len(edges)),
        "backlog_growth": 0.5,  # placeholder
        "no_safe_visibility_burden": 0.1,
    }

    state = MeshPressureState.LOW
    if metrics["degraded_edge_ratio"] > 0.5 or metrics["stale_case_density"] > 0.5:
        state = MeshPressureState.CRITICAL
    elif metrics["degraded_edge_ratio"] > 0.3:
        state = MeshPressureState.HIGH
    elif metrics["degraded_edge_ratio"] > 0.1:
        state = MeshPressureState.MODERATE

    warnings = []
    if state in [MeshPressureState.HIGH, MeshPressureState.CRITICAL]:
        warnings.append(
            f"Mesh pressure is {state.value}. Routing may be biased or suppressed."
        )

    return TribunalMeshPressureRecord(
        record_id=generate_id("trib_press"),
        mesh_id=mesh.tribunal_mesh_id,
        pressure_state=state,
        metrics=metrics,
        warnings=warnings,
    )


def preserve_no_safe_visibility_under_mesh_pressure(
    pressure: TribunalMeshPressureRecord,
) -> TribunalMeshPressureRecord:
    if pressure.metrics.get("no_safe_visibility_burden", 0) > 0:
        pressure.warnings.append("No-safe visibility burden preserved under pressure.")
    return pressure


def downgrade_tribunal_routes_due_to_pressure(
    paths: List[Dict[str, Any]], pressure: TribunalMeshPressureRecord
) -> List[Dict[str, Any]]:
    from sports_signal_bot.consistency_ledgers.mesh_paths import (
        apply_tribunal_mesh_constraints,
    )

    effective_pressure = pressure.pressure_state
    if effective_pressure == MeshPressureState.HIGH:
        effective_pressure = MeshPressureState.REVIEW_ONLY_BIAS
    elif effective_pressure == MeshPressureState.CRITICAL:
        effective_pressure = MeshPressureState.SUPPRESS_NONCRITICAL_TRIBUNAL_PATHS

    return apply_tribunal_mesh_constraints(paths, effective_pressure)
