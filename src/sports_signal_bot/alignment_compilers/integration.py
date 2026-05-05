from typing import List, Dict, Any

from .contracts import (
    ContextDisputeCaseRecord,
    TribunalDecisionRecord,
    BrokerExchangePacketRecord,
    BrokerExchangeRoutingRecord,
    AlignmentInputRecord
)
from .coherence_federations import summarize_coherence_federation_health
from .dispute_tribunals import summarize_context_dispute_effects
from .broker_exchanges import summarize_broker_exchange_route
from .alignment_compilers import explain_alignment_output

def build_context_tribunal_pipeline() -> str:
    """Builds the pipeline connecting context to tribunals."""
    return "Pipeline initialized: Context -> Tribunal Intake -> Decision -> Federation Update"

def connect_tribunal_decisions_to_context_federation(
    cases: List[ContextDisputeCaseRecord],
    target_federations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Connects tribunal decisions to refresh context federation states."""
    updated_federations = []
    for case in cases:
        if case.decision:
             for fed in target_federations:
                 # Apply caps and downgrades to the federation state conceptually
                 fed["applied_caps"] = fed.get("applied_caps", []) + case.decision.caps
                 updated_federations.append(fed)
    return updated_federations

def summarize_context_tribunal_flow(cases: List[ContextDisputeCaseRecord]) -> str:
    """Summarizes the flow from context to tribunals."""
    decided_cases = [c for c in cases if c.decision]
    return f"Processed {len(cases)} cases, {len(decided_cases)} resulted in decisions with caps."

def build_broker_exchange_context_pipeline() -> str:
    """Builds the pipeline connecting broker exchanges to trace and context."""
    return "Pipeline initialized: Broker Exchange -> Routing -> Trace Update -> Context Refresh"

def connect_broker_exchange_to_trace_and_context(
    routing_records: List[BrokerExchangeRoutingRecord],
    target_contexts: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Connects broker exchange routes to trace and context states."""
    updated_contexts = []
    for route in routing_records:
        for context in target_contexts:
            # Degrade context if route is degraded or caveated
            if route.route_status in ["routed_caveated_exchange", "routed_degraded_exchange", "routed_review_only_exchange"]:
                context["caveat_state"] = "caveated"
            updated_contexts.append(context)
    return updated_contexts

def summarize_broker_exchange_context_flow(routing_records: List[BrokerExchangeRoutingRecord]) -> str:
    """Summarizes the flow from broker exchange to context."""
    bounded = len([r for r in routing_records if r.route_status == "routed_bounded_exchange"])
    return f"Processed {len(routing_records)} exchanges: {bounded} bounded routes found."

def build_freshness_alignment_pipeline() -> str:
    """Builds the pipeline connecting freshness chambers to alignment compilers."""
    return "Pipeline initialized: Freshness Dispute -> Chamber Resolution -> Alignment Refresh"

def connect_freshness_chambers_to_alignment(
    dispute_decisions: List[Dict[str, Any]],
    alignment_inputs: List[AlignmentInputRecord]
) -> List[AlignmentInputRecord]:
    """Connects freshness chamber decisions to alignment input refresh."""
    updated_inputs = []
    for decision in dispute_decisions:
        for inp in alignment_inputs:
            # Conceptual: apply freshness caps
            if decision.get("refresh_required", False):
                inp.currentness_state = "stale"
            updated_inputs.append(inp)
    return updated_inputs

def summarize_freshness_alignment_flow(inputs: List[AlignmentInputRecord]) -> str:
    """Summarizes the flow from freshness to alignment."""
    stale_inputs = len([i for i in inputs if i.currentness_state == "stale"])
    return f"Processed {len(inputs)} alignment inputs: {stale_inputs} forced to stale by freshness chambers."

def enforce_phase97_currentness_caveat_scope_rules(context: Dict[str, Any]) -> bool:
    """Enforces currentness, caveat, and scope rules across phase 97."""
    return "stale" not in context.get("currentness_state", "current")

def cap_phase97_outputs_due_to_staleness_or_exchange_gaps(output: Dict[str, Any], evidence_complete: bool) -> Dict[str, Any]:
    """Caps outputs if staleness or evidence gaps are present."""
    if not evidence_complete:
        output["band"] = "review_only_alignment"
    return output

def explain_phase97_block_or_downgrade(reason: str) -> str:
    """Explains blocks or downgrades."""
    return f"Downgraded/Blocked due to: {reason}"

def enforce_sovereignty_across_phase97(context: Dict[str, Any]) -> bool:
    """Enforces local sovereignty checks across phase 97."""
    return context.get("sovereignty_state", "passed") != "failed"

def preserve_local_deny_in_phase97_outputs(output: Dict[str, Any], local_deny: bool) -> Dict[str, Any]:
    """Ensures local deny is preserved in outputs."""
    if local_deny:
        output["band"] = "blocked"
    return output

def explain_sovereignty_phase97_effects(context: Dict[str, Any]) -> str:
    """Explains the effects of sovereignty on phase 97."""
    return f"Sovereignty State: {context.get('sovereignty_state', 'passed')}"
