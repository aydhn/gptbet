import pytest
from sports_signal_bot.stable_adoption.rollback import build_adoption_rollback_plan, execute_adoption_rollback
from sports_signal_bot.stable_adoption.contracts import RollbackType

def test_rollback_execution():
    plan = build_adoption_rollback_plan("adp_01", RollbackType.ROLLBACK_TO_PREVIOUS_STABLE, "snap_01", "verification failed")
    assert execute_adoption_rollback(plan) is True
