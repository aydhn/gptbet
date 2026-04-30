from sports_signal_bot.cohort_autopilot.growth import compute_growth_eligibility
from sports_signal_bot.cohort_autopilot.contracts import GrowthEligibilityStatus

def test_growth_eligibility_blocked():
    eligibility = compute_growth_eligibility("c1", ["Critical dispute"], 0.95)
    assert eligibility.status == GrowthEligibilityStatus.GROWTH_BLOCKED

def test_growth_eligibility_clean():
    eligibility = compute_growth_eligibility("c1", [], 0.95)
    assert eligibility.status == GrowthEligibilityStatus.ELIGIBLE_FOR_GROWTH
