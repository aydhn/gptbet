from typing import List, Optional
from .contracts import (
    GovernanceRecoveryEscalatorRecord,
    EscalationStageRecord,
    EscalationTriggerRecord,
    EscalationCheckpointRecord,
    EscalationDecisionRecord,
    EscalationRecoveryPathRecord,
    EscalationBoundRecord,
    EscalationHealthRecord,
    EscalationManifestRecord,
    EscalationWarningRecord,
    EscalationStage,
    EscalationDecisionType
)

def build_governance_recovery_escalator(escalator_id: str, family: str) -> GovernanceRecoveryEscalatorRecord:
    health = EscalationHealthRecord(is_healthy=True, current_stage=EscalationStage.MONITORING)
    return GovernanceRecoveryEscalatorRecord(
        escalator_id=escalator_id,
        escalator_family=family,
        recovery_policy_ref="default_recovery",
        current_state=EscalationStage.MONITORING,
        health_status=health
    )

def evaluate_escalation_triggers(escalator: GovernanceRecoveryEscalatorRecord, triggers: List[EscalationTriggerRecord]) -> GovernanceRecoveryEscalatorRecord:
    if triggers:
        escalator.current_state = EscalationStage.CAUTION
        escalator.health_status.current_stage = EscalationStage.CAUTION
    return escalator

def advance_recovery_escalator(escalator: GovernanceRecoveryEscalatorRecord, next_stage: EscalationStage) -> GovernanceRecoveryEscalatorRecord:
    escalator.current_state = next_stage
    escalator.health_status.current_stage = next_stage
    return escalator

def verify_escalation_checkpoints(checkpoints: List[EscalationCheckpointRecord]) -> bool:
    return all(cp.passed for cp in checkpoints)

def summarize_escalator_state(escalator: GovernanceRecoveryEscalatorRecord) -> dict:
    return {"state": escalator.current_state}
