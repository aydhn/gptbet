from sports_signal_bot.cohort_autopilot.cohorts import create_adoption_cohort
from sports_signal_bot.cohort_autopilot.partitions import build_rollout_partition, validate_partition_fairness
from sports_signal_bot.cohort_autopilot.contracts import ActivationLevel, CohortStatus

def test_create_cohort():
    cohort = create_adoption_cohort("c1", "a1", "provider_priority", {"sport": "football"}, "provider_priority")
    assert cohort.cohort_id == "c1"
    assert cohort.activation_level == ActivationLevel.LEVEL_0_REFERENCE_ONLY
    assert cohort.current_status == CohortStatus.COHORT_PLANNED

def test_build_partition():
    slices = [{"market": "ml"}, {"market": "spread"}]
    plan = build_rollout_partition("p1", "c1", slices)
    assert len(plan.slices) == 2
    assert validate_partition_fairness(plan) is True
