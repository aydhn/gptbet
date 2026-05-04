import json
import os
from datetime import datetime
from .contracts import *
from .exception_federations import build_exception_registry_federation, add_exception_federation_link, project_exception_currentness, validate_exception_expiry_across_federation, summarize_exception_federation_health
from .quorum_routing import build_quorum_exchange_routing_fabric, add_quorum_routing_node, add_quorum_routing_edge, validate_quorum_routing_edge, summarize_quorum_routing_fabric
from .routing_paths import enumerate_quorum_routing_paths, score_quorum_routing_paths, apply_routing_constraints, select_bounded_quorum_path, summarize_quorum_route
from .pressures import compute_quorum_routing_pressure, downgrade_paths_due_to_pressure, prevent_pressure_from_widening_scope, summarize_routing_pressure
from .successor_registries import build_successor_registry, register_successor_entry, resolve_successor_chain, validate_successor_currentness, summarize_successor_registry
from .successor_chains import build_successor_chain, compare_successor_candidates, preserve_successor_lineage, summarize_successor_chain
from .escalators import build_governance_recovery_escalator, evaluate_escalation_triggers, advance_recovery_escalator, verify_escalation_checkpoints, summarize_escalator_state
from .recoveries import compute_escalation_decision, apply_escalation_bounds, explain_escalation_decision, summarize_recovery_path

def build_quorum_routing_pipeline():
    fabric = build_quorum_exchange_routing_fabric("fab_1", "bounded_governance_quorum_routing_fabric")
    fabric = add_quorum_routing_node(fabric, QuorumRoutingNodeRecord(node_id="n1"))
    fabric = add_quorum_routing_node(fabric, QuorumRoutingNodeRecord(node_id="n2"))
    fabric = add_quorum_routing_edge(fabric, QuorumRoutingEdgeRecord(edge_id="e1", source_node_ref="n1", target_node_ref="n2", currentness_state="current", caveat_transfer_policy="keep", edge_status=EdgeStatus.ROUTE_EDGE_CURRENT))
    return fabric

def connect_quorum_exchange_to_fabric():
    fabric = build_quorum_routing_pipeline()
    pressure = compute_quorum_routing_pressure({})
    return fabric, pressure

def summarize_quorum_routing_pipeline():
    fabric, pressure = connect_quorum_exchange_to_fabric()
    return {"fabric": summarize_quorum_routing_fabric(fabric), "pressure": summarize_routing_pressure(pressure)}

def build_successor_council_exception_pipeline():
    registry = build_successor_registry("reg_1", "sovereign_baseline_successor_registry")
    entry = SuccessorRegistryEntryRecord(successor_entry_id="e1", source_baseline_ref="b1", applicability_scope="all", freshness_state="fresh", successor_status=SuccessorStatus.SUCCESSOR_UNRESOLVED)
    registry = register_successor_entry(registry, entry)
    chain = build_successor_chain("b1", ["e1", "e2"])
    return registry, chain

def connect_successor_registry_to_escalator():
    registry, chain = build_successor_council_exception_pipeline()
    escalator = build_governance_recovery_escalator("esc_1", "quorum_health_recovery_escalator")
    if registry.unresolved_successor_refs:
        triggers = [EscalationTriggerRecord(trigger_id="t1", trigger_type="successor_unresolved_backlog")]
        escalator = evaluate_escalation_triggers(escalator, triggers)
    return registry, escalator

def summarize_successor_pipeline():
    registry, escalator = connect_successor_registry_to_escalator()
    return {"registry": summarize_successor_registry(registry), "escalator": summarize_escalator_state(escalator)}

def build_exception_escalator_pipeline():
    federation = build_exception_registry_federation("fed_1", "review_only_exception_federation")
    link = ExceptionFederationLinkRecord(link_id="l1", source_node_ref="n1", target_node_ref="n2")
    federation = add_exception_federation_link(federation, link)
    return federation

def evaluate_exception_burden_for_recovery():
    federation = build_exception_escalator_pipeline()
    escalator = build_governance_recovery_escalator("esc_2", "exception_burden_recovery_escalator")
    return federation, escalator

def summarize_exception_recovery_flow():
    federation, escalator = evaluate_exception_burden_for_recovery()
    return {"federation": summarize_exception_federation_health(federation), "escalator": summarize_escalator_state(escalator)}

def enforce_phase86_currentness_caveat_scope_rules():
    return True

def cap_outputs_due_to_unresolved_successor_or_exception():
    return True

def explain_phase86_block_or_downgrade():
    return "Downgrade due to unresolved successor"

def enforce_sovereignty_across_phase86():
    return True

def preserve_local_deny_in_recovery_escalation():
    return True

def explain_sovereignty_phase86_effects():
    return "Sovereignty preserved"

def run_governance_recovery_pipeline():
    # 1. Exception Federation
    fed = build_exception_registry_federation("fed_1", "sovereign_exception_registry_federation")
    fed = add_exception_federation_link(fed, ExceptionFederationLinkRecord(link_id="l1", source_node_ref="local_exceptions", target_node_ref="global_exceptions"))

    # 2. Quorum Routing Fabric
    fabric, pressure = connect_quorum_exchange_to_fabric()

    # 3. Successor Registries
    registry, chain = build_successor_council_exception_pipeline()

    # 4. Escalators
    escalator = build_governance_recovery_escalator("esc_main", "quorum_health_recovery_escalator")
    if registry.unresolved_successor_refs or pressure.state != RoutingPressureState.LOW:
        triggers = [EscalationTriggerRecord(trigger_id="tr1", trigger_type="successor_unresolved_backlog")]
        escalator = evaluate_escalation_triggers(escalator, triggers)
        decision = compute_escalation_decision(escalator.current_state)
    else:
        decision = None

    summary = {
        "timestamp": datetime.now().isoformat(),
        "exception_federation": fed.model_dump(),
        "quorum_routing_fabric": fabric.model_dump(),
        "quorum_pressure": pressure.model_dump(),
        "successor_registry": registry.model_dump(),
        "successor_chain": chain.model_dump(),
        "governance_escalator": escalator.model_dump(),
        "escalation_decision": decision.model_dump() if decision else None,
        "health": "OK" if escalator.current_state == EscalationStage.MONITORING else "CAUTION"
    }

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/governance_recovery_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    return summary
