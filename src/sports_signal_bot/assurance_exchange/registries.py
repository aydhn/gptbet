from typing import List, Optional, Dict, Any
from .contracts import FederatedRegistryRecord, RegistryCapabilityRecord
from sports_signal_bot.assurance.contracts import ClaimFamily

def register_federated_registry(
    registry_id: str,
    registry_name: str,
    registry_family: str,
    trust_domain: str,
    supported_artifact_families: List[str],
    supported_claim_families: List[ClaimFamily],
    compatibility_profile: str,
    sync_mode: str
) -> FederatedRegistryRecord:
    """Registers a new federated registry."""
    return FederatedRegistryRecord(
        registry_id=registry_id,
        registry_name=registry_name,
        registry_family=registry_family,
        trust_domain=trust_domain,
        supported_artifact_families=supported_artifact_families,
        supported_claim_families=supported_claim_families,
        active_status=True,
        compatibility_profile=compatibility_profile,
        sync_mode=sync_mode,
        warnings=[]
    )

def validate_registry_capabilities(registry: FederatedRegistryRecord) -> bool:
    """Validates the capabilities of a federated registry."""
    if not registry.supported_artifact_families:
        registry.warnings.append("No supported artifact families defined")
        return False
    if not registry.supported_claim_families:
        registry.warnings.append("No supported claim families defined")
        return False
    return True

def summarize_registry_federation(registries: List[FederatedRegistryRecord]) -> Dict[str, Any]:
    active = sum(1 for r in registries if r.active_status)
    return {
        "total_registries": len(registries),
        "active_registries": active,
        "inactive_registries": len(registries) - active
    }
