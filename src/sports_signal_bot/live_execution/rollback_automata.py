from .contracts import LaneRollbackAutomatonRecord, RollbackStatus

def build_lane_rollback_automaton(lane_ref: str) -> LaneRollbackAutomatonRecord:
    return LaneRollbackAutomatonRecord(
        automaton_id=f"rb_{lane_ref}",
        lane_ref=lane_ref,
        rollback_binding_ref="bind_1",
        current_state=RollbackStatus.IDLE,
        rollback_status=RollbackStatus.IDLE
    )

def arm_rollback_automaton(automaton: LaneRollbackAutomatonRecord) -> LaneRollbackAutomatonRecord:
    automaton.current_state = RollbackStatus.ARMED
    automaton.rollback_status = RollbackStatus.ARMED
    return automaton

def trigger_rollback_automaton(automaton: LaneRollbackAutomatonRecord) -> LaneRollbackAutomatonRecord:
    if automaton.current_state in [RollbackStatus.ARMED, RollbackStatus.READY]:
        automaton.current_state = RollbackStatus.TRIGGERED
        automaton.rollback_status = RollbackStatus.TRIGGERED
    return automaton

def execute_rollback(automaton: LaneRollbackAutomatonRecord) -> LaneRollbackAutomatonRecord:
    if automaton.current_state == RollbackStatus.TRIGGERED:
        automaton.current_state = RollbackStatus.COMPLETED_CLEAN
        automaton.rollback_status = RollbackStatus.COMPLETED_CLEAN
    return automaton
