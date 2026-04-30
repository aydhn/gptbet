from sports_signal_bot.cohort_autopilot.strategies.balanced import BalancedCohortAutopilotStrategy
from sports_signal_bot.cohort_autopilot.cohorts import create_adoption_cohort
from sports_signal_bot.cohort_autopilot.contracts import AutopilotAction

def test_manual_override_via_blockers():
    strategy = BalancedCohortAutopilotStrategy()
    cohort = create_adoption_cohort("c1", "a1", "fam", {}, "fam")
    decision = strategy.evaluate(cohort, {"blockers": ["Manual hold applied"]})
    assert decision.proposed_action == AutopilotAction.PAUSE_COHORT
