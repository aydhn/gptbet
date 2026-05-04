from sports_signal_bot.federation_ecosystem.contracts import CorridorRegistryFederationRecord, FederationLinkRecord
from sports_signal_bot.federation_ecosystem.federations import build_registry_federation, add_federation_link, compute_federated_currentness

def test_federated_currentness():
    currentness = compute_federated_currentness("current", "linked_expired")
    assert currentness == "stale"

    currentness = compute_federated_currentness("current", "linked_caveated")
    assert currentness == "current_with_caveats"

def test_build_federation():
    fed = build_registry_federation("fed1", "sovereign_corridor_registry_federation", ["reg1"])
    assert fed.federation_id == "fed1"
