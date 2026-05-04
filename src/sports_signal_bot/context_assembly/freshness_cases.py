import uuid
from typing import List, Dict, Any
from .contracts import (
    ProofFreshnessCouncilRecord,
    ProofFreshnessCaseRecord,
    ProofFreshnessEvidenceRecord,
    ProofFreshnessDecisionRecord
)

CASE_OPENED = "case_opened"
CASE_COLLECTING_EVIDENCE = "case_collecting_evidence"
CASE_QUORUM_PENDING = "case_quorum_pending"
CASE_DECIDED = "case_decided"
CASE_DECIDED_WITH_CAVEATS = "case_decided_with_caveats"
CASE_REVIEW_ONLY = "case_review_only"
CASE_BLOCKED = "case_blocked"
CASE_SUPERSEDED = "case_superseded"
CASE_ARCHIVED = "case_archived"

DECISION_PRESERVE_EXISTING_FRESHNESS_CAP = "preserve_existing_freshness_cap"
DECISION_DOWNGRADE_TO_REVIEW_ONLY = "downgrade_to_review_only_proof_support"
DECISION_REQUIRE_PROOF_REFRESH = "require_proof_refresh"
DECISION_REQUIRE_TRACE_REVALIDATION = "require_trace_revalidation"
DECISION_AMPLIFY_PROOF_CAVEATS = "amplify_proof_caveats"
DECISION_PRESERVE_NO_SAFE_VISIBILITY = "preserve_no_safe_visibility"
DECISION_ACCEPT_BOUNDED_FRESHNESS = "accept_bounded_freshness_with_caps"
DECISION_BLOCK_UNRESOLVED = "block_due_to_unresolved_freshness_conflict"

DECAY_FRESH = "fresh"
DECAY_BORDERLINE = "borderline"
DECAY_CAVEATED_FRESHNESS = "caveated_freshness"
DECAY_STALE = "stale"
DECAY_SEVERELY_STALE = "severely_stale"
DECAY_BLOCKED_BY_STALENESS = "blocked_by_staleness"

def open_proof_freshness_case(family: str, proof_refs: List[str]) -> ProofFreshnessCaseRecord:
    case_id = f"pfc_{uuid.uuid4().hex[:8]}"
    return ProofFreshnessCaseRecord(
        proof_freshness_case_id=case_id,
        case_family=family,
        input_proof_refs=proof_refs,
        input_catalog_refs=[],
        input_atlas_refs=[],
        input_trace_refs=[],
        decision_needed="decay_review",
        escalation_state="none",
        case_status=CASE_OPENED
    )

def collect_proof_freshness_evidence(case: ProofFreshnessCaseRecord, data: Dict[str, Any]) -> ProofFreshnessEvidenceRecord:
    case.case_status = CASE_COLLECTING_EVIDENCE
    return ProofFreshnessEvidenceRecord(
        evidence_id=f"ev_{uuid.uuid4().hex[:8]}",
        data=data
    )

def classify_proof_freshness_decay(evidence: List[ProofFreshnessEvidenceRecord]) -> str:
    # Logic to evaluate freshness. If no evidence -> severe
    if not evidence:
        return DECAY_SEVERELY_STALE
    has_recent = any(e.data.get("age_hours", 999) < 24 for e in evidence)
    if has_recent:
        return DECAY_FRESH
    return DECAY_STALE

def compute_freshness_decay_projection(decay: str) -> str:
    if decay == DECAY_FRESH:
        return DECAY_BORDERLINE
    return DECAY_SEVERELY_STALE

def resolve_proof_freshness_case(case: ProofFreshnessCaseRecord, evidence: List[ProofFreshnessEvidenceRecord], has_quorum: bool) -> ProofFreshnessDecisionRecord:
    decay_band = classify_proof_freshness_decay(evidence)

    # Rule: no quorum no strong freshness affirmation
    if not has_quorum:
        case.case_status = CASE_REVIEW_ONLY
        case.warnings.append("No quorum reached")
        return ProofFreshnessDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_DOWNGRADE_TO_REVIEW_ONLY
        )

    # Rule: stale proof evidence cannot produce strong approval
    if decay_band in [DECAY_STALE, DECAY_SEVERELY_STALE]:
        case.case_status = CASE_BLOCKED
        return ProofFreshnessDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_REQUIRE_PROOF_REFRESH
        )

    if decay_band == DECAY_BORDERLINE:
        case.case_status = CASE_DECIDED_WITH_CAVEATS
        return ProofFreshnessDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            decision_type=DECISION_AMPLIFY_PROOF_CAVEATS
        )

    case.case_status = CASE_DECIDED
    return ProofFreshnessDecisionRecord(
        decision_id=f"dec_{uuid.uuid4().hex[:8]}",
        decision_type=DECISION_ACCEPT_BOUNDED_FRESHNESS
    )

def apply_proof_freshness_decision(case: ProofFreshnessCaseRecord, decision: ProofFreshnessDecisionRecord):
    # Enforces decision on the case. In reality, it would update actual proof caps.
    pass

def explain_proof_freshness_outcome(case: ProofFreshnessCaseRecord, decision: ProofFreshnessDecisionRecord) -> str:
    return f"Case {case.proof_freshness_case_id} resolved with {decision.decision_type}. Status: {case.case_status}"

def record_proof_freshness_lineage(case: ProofFreshnessCaseRecord):
    pass

def summarize_proof_freshness_effects(case: ProofFreshnessCaseRecord) -> str:
    return f"Proof Case {case.proof_freshness_case_id} affected {len(case.input_proof_refs)} proofs."

def summarize_freshness_decay(decay: str) -> str:
    return f"Current decay band: {decay}"

def explain_decay_impacts(decay: str) -> str:
    if decay in [DECAY_STALE, DECAY_SEVERELY_STALE, DECAY_BLOCKED_BY_STALENESS]:
        return "Severe decay impact: Strong trace or narrative support blocked."
    return "Minimal decay impact."
