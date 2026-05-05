import uuid
from typing import List, Dict, Any
from .contracts import (
    FreshnessDisputeChamberRecord,
    FreshnessDisputeCaseRecord
)

# CHAMBER FAMILY TAXONOMY
PROOF_FRESHNESS_DISPUTE_CHAMBER = "proof_freshness_dispute_chamber"
SIGNAL_FRESHNESS_DISPUTE_CHAMBER = "signal_freshness_dispute_chamber"
CONTEXT_CURRENTNESS_DISPUTE_CHAMBER = "context_currentness_dispute_chamber"
TRACE_FRESHNESS_DISPUTE_CHAMBER = "trace_freshness_dispute_chamber"
SOVEREIGNTY_VISIBILITY_DISPUTE_CHAMBER = "sovereignty_visibility_dispute_chamber"
NO_SAFE_VISIBILITY_DISPUTE_CHAMBER = "no_safe_visibility_dispute_chamber"
COMPOSITE_FRESHNESS_DISPUTE_CHAMBER = "composite_freshness_dispute_chamber"

# CASE FAMILY TAXONOMY
STALE_VS_BORDERLINE_CASE = "stale_vs_borderline_case"
REFRESH_EVIDENCE_GAP_CASE = "refresh_evidence_gap_case"
TRACE_CURRENTNESS_CONFLICT_CASE = "trace_currentness_conflict_case"
SNAPSHOT_DRIFT_CASE = "snapshot_drift_case"
PROOF_SIGNAL_MISMATCH_CASE = "proof_signal_mismatch_case"
SOVEREIGNTY_VISIBILITY_FRESHNESS_CASE = "sovereignty_visibility_freshness_case"
NO_SAFE_VISIBILITY_FRESHNESS_CASE = "no_safe_visibility_freshness_case"
CONFLICTING_DECAY_CASE = "conflicting_decay_case"

# CASE STATUS MODELİ
CASE_OPENED = "case_opened"
CASE_COLLECTING_EVIDENCE = "case_collecting_evidence"
CASE_REPLAY_PENDING = "case_replay_pending"
CASE_QUORUM_PENDING = "case_quorum_pending"
CASE_DECIDED = "case_decided"
CASE_DECIDED_WITH_CAVEATS = "case_decided_with_caveats"
CASE_REVIEW_ONLY = "case_review_only"
CASE_BLOCKED = "case_blocked"
CASE_SUPERSEDED = "case_superseded"
CASE_ARCHIVED = "case_archived"

# FRESHNESS DISPUTE DECISION TAXONOMY
PRESERVE_EXISTING_FRESHNESS_CAP = "preserve_existing_freshness_cap"
DOWNGRADE_TO_REVIEW_ONLY_SUPPORT = "downgrade_to_review_only_support"
REQUIRE_REFRESH_EVIDENCE = "require_refresh_evidence"
REQUIRE_TRACE_REVALIDATION = "require_trace_revalidation"
AMPLIFY_FRESHNESS_CAVEATS = "amplify_freshness_caveats"
PRESERVE_NO_SAFE_VISIBILITY = "preserve_no_safe_visibility"
ACCEPT_BOUNDED_FRESHNESS_WITH_CAPS = "accept_bounded_freshness_with_caps"
BLOCK_DUE_TO_UNRESOLVED_FRESHNESS_DISPUTE = "block_due_to_unresolved_freshness_dispute"

# FRESHNESS DECAY MODEL
DECAY_FRESH = "fresh"
DECAY_BORDERLINE = "borderline"
DECAY_CAVEATED_FRESHNESS = "caveated_freshness"
DECAY_STALE = "stale"
DECAY_SEVERELY_STALE = "severely_stale"
DECAY_BLOCKED_BY_STALENESS = "blocked_by_staleness"


def build_freshness_dispute_chamber(family: str, policies: Dict[str, str]) -> FreshnessDisputeChamberRecord:
    return FreshnessDisputeChamberRecord(
        freshness_dispute_chamber_id=str(uuid.uuid4()),
        chamber_family=family,
        quorum_policy_ref=policies.get('quorum', 'default'),
        precedence_policy_ref=policies.get('precedence', 'default'),
        backlog_ref="default_backlog",
        health_status="active"
    )

def open_freshness_dispute_case(chamber: FreshnessDisputeChamberRecord, family: str) -> FreshnessDisputeCaseRecord:
    return FreshnessDisputeCaseRecord(
        freshness_dispute_case_id=str(uuid.uuid4()),
        case_family=family,
        decision_needed=True,
        escalation_state="none",
        case_status=CASE_OPENED
    )

def collect_freshness_dispute_evidence(case: FreshnessDisputeCaseRecord, evidence_refs: List[str]) -> None:
    case.case_status = CASE_COLLECTING_EVIDENCE
    case.input_proof_refs.extend(evidence_refs)

def resolve_freshness_dispute_case(case: FreshnessDisputeCaseRecord, decision: str) -> str:
    if decision == REQUIRE_REFRESH_EVIDENCE and not case.input_proof_refs:
        case.case_status = CASE_REVIEW_ONLY
        return DOWNGRADE_TO_REVIEW_ONLY_SUPPORT

    case.case_status = CASE_DECIDED
    return decision

def summarize_freshness_dispute_chamber(chamber: FreshnessDisputeChamberRecord) -> Dict[str, Any]:
    return {
        "id": chamber.freshness_dispute_chamber_id,
        "family": chamber.chamber_family,
        "health": chamber.health_status
    }

def apply_freshness_dispute_decision(case: FreshnessDisputeCaseRecord, decision: str) -> None:
    pass

def explain_freshness_dispute_outcome(case: FreshnessDisputeCaseRecord) -> str:
    return f"Case {case.freshness_dispute_case_id} resolved with status {case.case_status}"

def record_freshness_dispute_lineage(case: FreshnessDisputeCaseRecord) -> None:
    pass

def summarize_freshness_dispute_effects(case: FreshnessDisputeCaseRecord) -> Dict[str, Any]:
    return {"status": case.case_status, "escalation": case.escalation_state}

def classify_freshness_decay(age_seconds: int) -> str:
    if age_seconds < 3600: return DECAY_FRESH
    if age_seconds < 86400: return DECAY_BORDERLINE
    if age_seconds < 604800: return DECAY_STALE
    return DECAY_SEVERELY_STALE

def compute_dispute_decay_projection(case: FreshnessDisputeCaseRecord) -> str:
    return DECAY_BORDERLINE

def summarize_dispute_decay(case: FreshnessDisputeCaseRecord) -> Dict[str, Any]:
    return {"decay_projection": compute_dispute_decay_projection(case)}

def explain_decay_impacts(decay: str) -> str:
    return f"Decay level {decay} impacts bounded confidence."
