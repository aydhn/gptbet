from src.sports_signal_bot.planetary_mesh_hardening.simulation_federations import build_audit_simulation_federation, verify_audit_simulation_federation
from src.sports_signal_bot.planetary_mesh_hardening.contracts import FederationStatus

def test_audit_simulation_federation_asymmetry():
    # 5) Audit simulation federation asymmetry set
    fed = build_audit_simulation_federation("f_asym", "follow_the_sun_audit_federation")
    verify_audit_simulation_federation(fed)
    assert fed.federation_status == FederationStatus.FEDERATION_VERIFIED
