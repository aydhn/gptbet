from datetime import datetime, timedelta
from typing import List, Optional
import uuid

from .contracts import (
    SovereignGovernanceExceptionLedgerRecord,
    GovernanceExceptionRecord,
    ExceptionLedgerWarningRecord
)

# EXCEPTION FAMILY TAXONOMY
EXCEPTION_FAMILIES = [
    "temporary_review_visibility_exception",
    "bounded_projection_exception",
    "replay_required_exception",
    "degraded_path_exception",
    "stale_currentness_exception",
    "sovereignty_limited_exception",
    "audit_rebuild_exception",
    "baseline_successor_pending_exception",
]

# EXCEPTION STATUS TAXONOMY
EXCEPTION_STATUSES = [
    "exception_opened",
    "exception_review_only",
    "exception_active_bounded",
    "exception_caveated",
    "exception_expiring",
    "exception_expired",
    "exception_superseded",
    "exception_revoked",
    "exception_blocked",
]

def build_governance_exception_ledger(
    ledger_family: str,
    owning_scope_ref: str
) -> SovereignGovernanceExceptionLedgerRecord:
    return SovereignGovernanceExceptionLedgerRecord(
        exception_ledger_id=str(uuid.uuid4()),
        ledger_family=ledger_family,
        owning_scope_ref=owning_scope_ref,
        active_exception_refs=[],
        expired_exception_refs=[],
        superseded_exception_refs=[],
        replay_refs=[],
        health_status="healthy",
        warnings=[]
    )

def open_governance_exception(
    exception_family: str,
    opened_reason: str,
    affected_scope_ref: str,
    validity_window: int
) -> GovernanceExceptionRecord:
    return GovernanceExceptionRecord(
        exception_id=str(uuid.uuid4()),
        exception_family=exception_family,
        opened_reason=opened_reason,
        affected_scope_ref=affected_scope_ref,
        bounded_effect_summary="pending",
        preserved_block_refs=[],
        preserved_caveat_refs=[],
        validity_window=validity_window,
        evidence_refs=[],
        decision_status="exception_opened",
        warnings=[]
    )

def validate_exception_boundedness(exception: GovernanceExceptionRecord) -> bool:
    if exception.validity_window <= 0:
        return False
    return True

def replay_governance_exception(exception: GovernanceExceptionRecord) -> bool:
    return True

def summarize_exception_ledger(ledger: SovereignGovernanceExceptionLedgerRecord) -> dict:
    return {
        "id": ledger.exception_ledger_id,
        "active_count": len(ledger.active_exception_refs),
        "status": ledger.health_status
    }

# EXCEPTION EFFECT TAXONOMY
EXCEPTION_EFFECTS = [
    "downgrade_only_visibility",
    "bounded_review_only_projection",
    "replay_required_before_projection",
    "stale_penalty_temporarily_preserved",
    "successor_missing_block_preserved",
    "degraded_fallback_only",
    "explicit_no_safe_hint_preserved",
]

def compute_exception_effect(exception: GovernanceExceptionRecord) -> str:
    return "bounded_review_only_projection"

def prevent_exception_scope_broadening(exception: GovernanceExceptionRecord):
    pass

def explain_exception_effect(exception: GovernanceExceptionRecord) -> str:
    return f"Effect: {compute_exception_effect(exception)}"

def summarize_exception_effects(exceptions: List[GovernanceExceptionRecord]) -> dict:
    return {"effects": [explain_exception_effect(e) for e in exceptions]}

# EXCEPTION EXPIRY / SUPERSESSION MODEL
EXPIRY_TRIGGERS = [
    "validity window passed",
    "successor resolved",
    "replay mismatch cleared",
    "stale state refreshed",
    "sovereignty clarification applied",
    "council case superseded",
    "evidence invalidated",
]

EXPIRY_OUTCOMES = [
    "expire_exception",
    "supersede_exception",
    "retain_exception_caveated",
    "revoke_exception",
    "reopen_review_only",
]

def evaluate_exception_expiry(exception: GovernanceExceptionRecord, current_time: datetime, created_at: datetime) -> str:
    if current_time > created_at + timedelta(seconds=exception.validity_window):
        return "expire_exception"
    return "retain_exception_caveated"

def supersede_governance_exception(exception: GovernanceExceptionRecord, superseded_by: str):
    exception.decision_status = "exception_superseded"

def reopen_exception_for_review(exception: GovernanceExceptionRecord):
    exception.decision_status = "exception_review_only"

def summarize_exception_lifecycle(exception: GovernanceExceptionRecord) -> dict:
    return {
        "id": exception.exception_id,
        "status": exception.decision_status
    }
