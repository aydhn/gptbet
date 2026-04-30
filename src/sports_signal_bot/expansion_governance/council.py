from typing import List, Dict, Any, Tuple
import uuid
from datetime import datetime
from .contracts import (
    ExpansionCouncilRecord, CouncilDecision, ExpansionPressureRecord,
    ExpansionControlStateRecord, ExpansionBudgetRecord, CrossCohortConflictRecord,
    BreakerEvaluationRecord, ExpansionStatus, PressureBand
)

def evaluate_budget_lens(budgets: List[ExpansionBudgetRecord]) -> Dict[str, Any]:
    """Evaluates the budget aspect for the council."""
    critical_budgets = [b for b in budgets if b.budget_status == "critical" or b.budget_status == "exhausted"]
    exhausted_budgets = [b for b in budgets if b.budget_status == "exhausted"]

    status = "pass"
    if exhausted_budgets:
        status = "fail"
    elif critical_budgets:
        status = "warn"

    return {
        "status": status,
        "critical_count": len(critical_budgets),
        "exhausted_count": len(exhausted_budgets),
        "details": [f"{b.budget_family}: {b.budget_status}" for b in critical_budgets]
    }

def evaluate_pressure_lens(pressure: ExpansionPressureRecord) -> Dict[str, Any]:
    """Evaluates the overall system pressure for the council."""
    status = "pass"
    if pressure.pressure_band in [PressureBand.CRITICAL]:
        status = "fail"
    elif pressure.pressure_band in [PressureBand.SEVERE, PressureBand.HIGH]:
        status = "warn"

    return {
        "status": status,
        "band": pressure.pressure_band.value,
        "score": pressure.pressure_score
    }

def evaluate_conflict_lens(conflicts: List[CrossCohortConflictRecord]) -> Dict[str, Any]:
    """Evaluates cross-family and cross-cohort conflicts."""
    from .conflicts import classify_conflict_severity
    from .contracts import ConflictSeverity

    max_severity = classify_conflict_severity(conflicts)

    status = "pass"
    if max_severity == ConflictSeverity.CRITICAL:
        status = "fail"
    elif max_severity == ConflictSeverity.HIGH:
        status = "warn"

    return {
        "status": status,
        "max_severity": max_severity.value,
        "conflict_count": len(conflicts)
    }

def build_expansion_council_packet(
    state: ExpansionControlStateRecord,
    budgets: List[ExpansionBudgetRecord],
    pressure: ExpansionPressureRecord,
    conflicts: List[CrossCohortConflictRecord],
    breakers: BreakerEvaluationRecord
) -> Dict[str, Any]:
    """Compiles all lenses into a review packet for the council aggregator."""
    return {
        "state": state,
        "budget_lens": evaluate_budget_lens(budgets),
        "pressure_lens": evaluate_pressure_lens(pressure),
        "conflict_lens": evaluate_conflict_lens(conflicts),
        "breaker_lens": {
            "status": "fail" if breakers.triggers_fired else "pass",
            "triggers": len(breakers.triggers_fired)
        }
    }

def aggregate_expansion_council_decision(packet: Dict[str, Any]) -> ExpansionCouncilRecord:
    """Deterministic structured aggregator that replaces manual council review."""

    lenses = {
        "budget": packet["budget_lens"],
        "pressure": packet["pressure_lens"],
        "conflict": packet["conflict_lens"],
        "breaker": packet["breaker_lens"]
    }

    decision = CouncilDecision.CONTINUE_EXPANSION
    rationale = "All lenses passed or within acceptable warning limits."

    fail_count = sum(1 for v in lenses.values() if v["status"] == "fail")
    warn_count = sum(1 for v in lenses.values() if v["status"] == "warn")

    if lenses["breaker"]["status"] == "fail":
         decision = CouncilDecision.PAUSE_ALL_GROWTH
         rationale = "Circuit breaker triggered; immediate pause mandated."
    elif fail_count > 0:
        if lenses["budget"]["status"] == "fail" or lenses["conflict"]["status"] == "fail":
            decision = CouncilDecision.HOLD_NEW_GROWTH
            rationale = "Critical budget exhaustion or conflicts detected. Holding new growth."
        else:
            decision = CouncilDecision.THROTTLE_EXPANSION
            rationale = "Critical pressure detected. Throttling expansion."
    elif warn_count >= 2:
         decision = CouncilDecision.THROTTLE_EXPANSION
         rationale = f"Multiple warnings ({warn_count}) across lenses. Throttling applied."

    # Check if we are already in a paused/recovery state and shouldn't blindly continue
    state: ExpansionControlStateRecord = packet["state"]
    if decision == CouncilDecision.CONTINUE_EXPANSION and state.global_status in [
        ExpansionStatus.GLOBAL_EMERGENCY_PAUSE,
        ExpansionStatus.RECOVERY_MONITORING_MODE,
        ExpansionStatus.ROLLBACK_STABILIZATION_MODE
    ]:
         decision = CouncilDecision.HOLD_NEW_GROWTH
         rationale = f"Cannot continue expansion while in {state.global_status.value}."

    return ExpansionCouncilRecord(
        council_id=f"ccl_{uuid.uuid4().hex[:8]}",
        decision=decision,
        rationale=rationale,
        lens_evaluations=lenses
    )
