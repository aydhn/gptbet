from sports_signal_bot.handoff.readiness import compute_adoption_readiness
from sports_signal_bot.handoff.contracts import AdoptionReadinessStatus

def test_compute_adoption_readiness_ready():
    context = {
        "candidate_stable_across_channels": True,
        "monitoring_expectations_defined": True
    }
    record = compute_adoption_readiness("h1", context)
    assert record.status == AdoptionReadinessStatus.ACTIVATION_REVIEW_READY

def test_compute_adoption_readiness_blocked():
    context = {
        "candidate_stable_across_channels": False,
        "monitoring_expectations_defined": True
    }
    record = compute_adoption_readiness("h1", context)
    assert record.status == AdoptionReadinessStatus.BLOCKED_FOR_ACTIVATION
