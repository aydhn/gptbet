from sports_signal_bot.federated_governance.planes import compute_plane_health, compute_plane_trust
from sports_signal_bot.federated_governance.contracts import PlaneHealthBand, PlaneTrustBand

def test_compute_health_and_trust():
    health = compute_plane_health(escalation_rate=0.6, conflict_density=0.1)
    assert health == PlaneHealthBand.UNSTABLE

    trust = compute_plane_trust(health, budget_violations=0)
    assert trust == PlaneTrustBand.LOW

    health_good = compute_plane_health(0.05, 0.05)
    assert health_good == PlaneHealthBand.HEALTHY

    trust_good = compute_plane_trust(health_good, 0)
    assert trust_good == PlaneTrustBand.HIGH

    trust_violations = compute_plane_trust(health_good, 3)
    assert trust_violations == PlaneTrustBand.LOW
