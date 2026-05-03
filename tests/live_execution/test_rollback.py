from sports_signal_bot.live_execution.rollback_automata import build_lane_rollback_automaton, arm_rollback_automaton, trigger_rollback_automaton, execute_rollback
from sports_signal_bot.live_execution.contracts import RollbackStatus

def test_rollback_automaton():
    automaton = build_lane_rollback_automaton("lane_1")
    assert automaton.current_state == RollbackStatus.IDLE
    automaton = arm_rollback_automaton(automaton)
    assert automaton.current_state == RollbackStatus.ARMED
    automaton = trigger_rollback_automaton(automaton)
    assert automaton.current_state == RollbackStatus.TRIGGERED
    automaton = execute_rollback(automaton)
    assert automaton.current_state == RollbackStatus.COMPLETED_CLEAN
