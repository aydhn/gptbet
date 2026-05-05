from typing import Any
from typing import List, Dict, Optional
import datetime
from .contracts import (
    ContextDisputeTribunalRecord,
    ContextDisputeCaseRecord,
    TribunalClaimRecord,
    TribunalEvidenceRecord,
    TribunalPanelRecord,
    TribunalDecisionRecord,
    ContextDisputeTribunalWarningRecord
)

def build_context_dispute_tribunal(
    tribunal_id: str,
    family: str,
    quorum_policy: str,
    precedence_policy: str
) -> ContextDisputeTribunalRecord:
    """Builds a new context dispute tribunal."""
    return ContextDisputeTribunalRecord(
        context_dispute_tribunal_id=tribunal_id,
        tribunal_family=family,
        governed_context_refs=[],
        participant_refs=[],
        quorum_policy_ref=quorum_policy,
        precedence_policy_ref=precedence_policy,
        backlog_ref="default_backlog",
        health_status="initializing",
        warnings=[],
        cases=[]
    )

def open_context_dispute_case(
    tribunal: ContextDisputeTribunalRecord,
    case_id: str,
    case_family: str,
    context_refs: List[str]
) -> ContextDisputeCaseRecord:
    """Opens a new case in the tribunal."""
    case = ContextDisputeCaseRecord(
        context_dispute_case_id=case_id,
        case_family=case_family,
        input_context_refs=context_refs,
        input_trace_refs=[],
        input_proof_refs=[],
        input_dashboard_refs=[],
        input_narrative_refs=[],
        input_signal_refs=[],
        decision_needed="resolve_context_conflict",
        escalation_state="none",
        case_status="case_opened",
        warnings=[]
    )
    tribunal.cases.append(case)
    return case

def collect_context_dispute_evidence(
    case: ContextDisputeCaseRecord,
    evidence_records: List[TribunalEvidenceRecord]
) -> None:
    """Collects evidence for the dispute case."""
    case.case_status = "case_collecting_evidence"
    # Process evidence...
    if any(e.completeness != "complete" for e in evidence_records):
         case.warnings.append(ContextDisputeTribunalWarningRecord("incomplete_evidence", "Some evidence is incomplete."))

def resolve_context_dispute_case(
    case: ContextDisputeCaseRecord,
    decision_type: str,
    caps: List[str],
    refresh_requirements: List[str]
) -> TribunalDecisionRecord:
    """Resolves the dispute case with a decision."""
    decision = TribunalDecisionRecord(
        decision_type=decision_type,
        caps=caps,
        refresh_requirements=refresh_requirements
    )
    case.decision = decision
    if decision_type in ["block_due_to_unresolved_context_conflict", "downgrade_to_review_only_context"]:
        case.case_status = "case_review_only" if decision_type == "downgrade_to_review_only_context" else "case_blocked"
    else:
        case.case_status = "case_decided_with_caveats" if caps else "case_decided"
    return decision

def summarize_context_dispute_tribunal(
    tribunal: ContextDisputeTribunalRecord
) -> Dict[str, str]:
    """Summarizes the context dispute tribunal."""
    return {
        "tribunal_id": tribunal.context_dispute_tribunal_id,
        "cases_count": str(len(tribunal.cases)),
        "health_status": tribunal.health_status
    }

def build_tribunal_claim(
    claim_id: str,
    claim_type: str,
    description: str
) -> TribunalClaimRecord:
    """Builds a new tribunal claim."""
    return TribunalClaimRecord(
        claim_id=claim_id,
        claim_type=claim_type,
        description=description
    )

def validate_tribunal_claim_scope(claim: TribunalClaimRecord) -> bool:
    """Validates the scope of a tribunal claim."""
    valid_types = [
        "freshness_claim", "context_integrity_claim", "trace_integrity_claim",
        "proof_sufficiency_claim", "sovereignty_visibility_claim",
        "no_safe_visibility_claim", "caveat_integrity_claim", "cap_application_claim"
    ]
    return claim.claim_type in valid_types

def compare_tribunal_claims(claim1: TribunalClaimRecord, claim2: TribunalClaimRecord) -> str:
    """Compares two tribunal claims to find conflicts."""
    if claim1.claim_type == claim2.claim_type:
        return "conflict" if claim1.description != claim2.description else "aligned"
    return "orthogonal"

def explain_claim_conflicts(conflicts: List[str]) -> str:
    """Explains conflicts between claims."""
    return f"Found {len([c for c in conflicts if c == 'conflict'])} conflicts among claims."

def apply_context_dispute_decision(
    decision: TribunalDecisionRecord,
    target_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Applies the tribunal decision to a target context."""
    target_context["applied_caps"] = target_context.get("applied_caps", []) + decision.caps
    target_context["refresh_requirements"] = target_context.get("refresh_requirements", []) + decision.refresh_requirements
    target_context["tribunal_decision"] = decision.decision_type
    return target_context

def explain_context_dispute_outcome(decision: TribunalDecisionRecord) -> str:
    """Explains the outcome of the context dispute."""
    return f"Decision: {decision.decision_type}. Caps: {len(decision.caps)}. Refresh Reqs: {len(decision.refresh_requirements)}."

def record_context_dispute_lineage(case: ContextDisputeCaseRecord) -> str:
    """Records the lineage of the context dispute."""
    return f"Case {case.context_dispute_case_id} ({case.case_family}) -> {case.case_status}"

def summarize_context_dispute_effects(case: ContextDisputeCaseRecord) -> str:
    """Summarizes the effects of the context dispute."""
    if case.decision:
        return f"Effects: {case.decision.decision_type} applied with {len(case.decision.caps)} caps."
    return "No decision yet."

def build_tribunal_panel(
    panel_id: str,
    panel_family: str,
    findings: List[str]
) -> TribunalPanelRecord:
    """Builds a new tribunal panel."""
    return TribunalPanelRecord(
        panel_id=panel_id,
        panel_family=panel_family,
        findings=findings
    )

def aggregate_panel_findings(panels: List[TribunalPanelRecord]) -> List[str]:
    """Aggregates findings from multiple panels."""
    all_findings = []
    for p in panels:
        all_findings.extend(p.findings)
    return list(set(all_findings))

def summarize_panel_disagreement(panels: List[TribunalPanelRecord]) -> str:
    """Summarizes disagreement among panels."""
    # Simplified disagreement detection
    if len(panels) < 2:
        return "No disagreement (single panel)."
    return "Potential disagreement detected across panels."

def explain_panel_effect_on_decision(panels: List[TribunalPanelRecord], decision: TribunalDecisionRecord) -> str:
    """Explains how panel findings affected the decision."""
    findings_count = sum(len(p.findings) for p in panels)
    return f"Decision '{decision.decision_type}' was influenced by {findings_count} findings across {len(panels)} panels."
