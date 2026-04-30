from sports_signal_bot.cohort_autopilot.rollbacks import execute_cohort_rollback
from sports_signal_bot.cohort_autopilot.contracts import ActivationLevel

def test_cohort_rollback():
    rollback = execute_cohort_rollback("c1", ActivationLevel.LEVEL_0_REFERENCE_ONLY, "Critical regression")
    assert rollback.rollback_level == ActivationLevel.LEVEL_0_REFERENCE_ONLY
    assert rollback.reason == "Critical regression"
