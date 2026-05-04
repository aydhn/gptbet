from sports_signal_bot.federation_ecosystem.strategies.base import BaseFederationEcosystemStrategy
from sports_signal_bot.federation_ecosystem.strategies.conservative import ConservativeFederationRegistryStrategy
from sports_signal_bot.federation_ecosystem.strategies.balanced_attestation_hub import BalancedAttestationHubStrategy
from sports_signal_bot.federation_ecosystem.strategies.baseline_catalog_first import BaselineCatalogFirstStrategy

AVAILABLE_STRATEGIES = {
    "conservative": ConservativeFederationRegistryStrategy(),
    "balanced": BalancedAttestationHubStrategy(),
    "baseline_first": BaselineCatalogFirstStrategy()
}
