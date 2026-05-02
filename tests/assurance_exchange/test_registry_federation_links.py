from sports_signal_bot.assurance_exchange.registries import register_federated_registry, validate_registry_capabilities
from sports_signal_bot.assurance.contracts import ClaimFamily

def test_register_federated_registry():
    reg = register_federated_registry(
        registry_id="partner_1",
        registry_name="Partner 1",
        registry_family="federated_partner_registry",
        trust_domain="external",
        supported_artifact_families=["proof_bundle"],
        supported_claim_families=[ClaimFamily.e2e_promotion_claim],
        compatibility_profile="strict",
        sync_mode="pull"
    )
    assert reg.registry_id == "partner_1"
    assert validate_registry_capabilities(reg) is True

def test_validate_registry_capabilities_missing():
    reg = register_federated_registry(
        registry_id="partner_1",
        registry_name="Partner 1",
        registry_family="federated_partner_registry",
        trust_domain="external",
        supported_artifact_families=[],
        supported_claim_families=[],
        compatibility_profile="strict",
        sync_mode="pull"
    )
    assert validate_registry_capabilities(reg) is False
