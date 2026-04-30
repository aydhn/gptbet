from typing import List, Dict, Any, Tuple
import uuid
from .contracts import (
    CircuitBreakerTriggerRecord, CircuitBreakerActionRecord, BreakerEvaluationRecord,
    ExpansionControlStateRecord
)

def evaluate_circuit_breakers(state: ExpansionControlStateRecord, metrics: Dict[str, Any]) -> BreakerEvaluationRecord:
    """Evaluates metrics against known circuit breaker rules to detect emergency conditions."""
    triggers = detect_breaker_triggers(metrics)
    actions = execute_breaker_actions(triggers)

    return BreakerEvaluationRecord(
        evaluation_id=f"eval_{uuid.uuid4().hex[:8]}",
        triggers_fired=triggers,
        actions_proposed=actions
    )

def detect_breaker_triggers(metrics: Dict[str, Any]) -> List[CircuitBreakerTriggerRecord]:
    """Examines raw global metrics to find crossed critical thresholds."""
    triggers = []

    # 1. Critical verification cluster
    if metrics.get('critical_verification_failures', 0) >= 3:
        triggers.append(CircuitBreakerTriggerRecord(
            trigger_id=f"trig_{uuid.uuid4().hex[:8]}",
            trigger_type="critical_verification_regression_cluster",
            threshold_exceeded=True,
            description="3 or more critical verification failures detected across active cohorts."
        ))

    # 2. Repeated rollbacks in short window
    if metrics.get('rollbacks_last_24h', 0) >= 2:
        triggers.append(CircuitBreakerTriggerRecord(
            trigger_id=f"trig_{uuid.uuid4().hex[:8]}",
            trigger_type="repeated_rollbacks_in_short_window",
            threshold_exceeded=True,
            description="Multiple rollbacks executed within 24 hours."
        ))

    # 3. Budget Saturation
    budget_usage = metrics.get('global_budget_usage_pct', 0.0)
    if budget_usage >= 0.95:
        triggers.append(CircuitBreakerTriggerRecord(
            trigger_id=f"trig_{uuid.uuid4().hex[:8]}",
            trigger_type="budget_saturation_critical",
            threshold_exceeded=True,
            description=f"Global budget usage is {budget_usage*100:.1f}%, exceeding 95% critical threshold."
        ))

    # 4. Dispute Burden
    if metrics.get('cross_family_dispute_rate', 0.0) >= 0.15:
        triggers.append(CircuitBreakerTriggerRecord(
            trigger_id=f"trig_{uuid.uuid4().hex[:8]}",
            trigger_type="dispute_burden_spike_across_families",
            threshold_exceeded=True,
            description="High cross-family adjudication dispute rate detected (>15%)."
        ))

    return triggers

def execute_breaker_actions(triggers: List[CircuitBreakerTriggerRecord]) -> List[CircuitBreakerActionRecord]:
    """Maps fired triggers to concrete emergency actions (e.g., pause, rollback)."""
    actions = []

    for t in triggers:
        if t.trigger_type == "critical_verification_regression_cluster":
            actions.append(CircuitBreakerActionRecord(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                trigger_id=t.trigger_id,
                action_type="global_pause",
                manual_ack_required=True
            ))
            actions.append(CircuitBreakerActionRecord(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                trigger_id=t.trigger_id,
                action_type="enter_recovery_monitoring_mode",
                manual_ack_required=False
            ))

        elif t.trigger_type == "repeated_rollbacks_in_short_window":
            actions.append(CircuitBreakerActionRecord(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                trigger_id=t.trigger_id,
                action_type="pause_wave",
                manual_ack_required=True
            ))

        elif t.trigger_type == "budget_saturation_critical":
            actions.append(CircuitBreakerActionRecord(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                trigger_id=t.trigger_id,
                action_type="shrink_multiple_cohorts",
                manual_ack_required=False
            ))

        elif t.trigger_type == "dispute_burden_spike_across_families":
            actions.append(CircuitBreakerActionRecord(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                trigger_id=t.trigger_id,
                action_type="freeze_family",
                manual_ack_required=True
            ))

    return actions

def summarize_breaker_impacts(evaluation: BreakerEvaluationRecord) -> Dict[str, Any]:
    """Generates a summary of breaker actions taken."""
    return {
        "triggers_fired": len(evaluation.triggers_fired),
        "actions_proposed": len(evaluation.actions_proposed),
        "requires_manual_ack": any(a.manual_ack_required for a in evaluation.actions_proposed),
        "action_types": list(set(a.action_type for a in evaluation.actions_proposed))
    }

def require_manual_ack_for_critical_breakers(actions: List[CircuitBreakerActionRecord]) -> bool:
    """Checks if any proposed action mandates human intervention before clearing."""
    return any(a.manual_ack_required for a in actions)
