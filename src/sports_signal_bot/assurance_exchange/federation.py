from typing import List, Dict, Any
from .contracts import RegistryFederationLinkRecord, FederationTrustRecord
from sports_signal_bot.assurance.contracts import ClaimFamily

def build_registry_federation_link(
    link_id: str,
    source_registry: str,
    destination_registry: str,
    allowed_artifact_families: List[str],
    allowed_claim_families: List[ClaimFamily],
    translation_policy: str,
    trust_policy: str,
    notarization_policy: str,
    quarantine_rules: Dict[str, Any],
    sync_mode: str,
    approval_requirements: List[str]
) -> RegistryFederationLinkRecord:
    """Builds a new registry federation link."""
    return RegistryFederationLinkRecord(
        link_id=link_id,
        source_registry=source_registry,
        destination_registry=destination_registry,
        allowed_artifact_families=allowed_artifact_families,
        allowed_claim_families=allowed_claim_families,
        translation_policy=translation_policy,
        trust_policy=trust_policy,
        notarization_policy=notarization_policy,
        quarantine_rules=quarantine_rules,
        sync_mode=sync_mode,
        approval_requirements=approval_requirements,
        warnings=[]
    )

def resolve_federation_trust_policy(link: RegistryFederationLinkRecord) -> str:
    """Resolves the effective trust policy for a federation link."""
    return link.trust_policy

def evaluate_partner_registry_trust(registry_id: str, links: List[RegistryFederationLinkRecord]) -> str:
    """Evaluates the trust level of a partner registry based on existing links."""
    for link in links:
        if link.destination_registry == registry_id or link.source_registry == registry_id:
            return link.trust_policy
    return "untrusted"

def reduce_acceptance_due_to_low_trust(link: RegistryFederationLinkRecord) -> bool:
    """Determines if acceptance should be reduced due to low trust."""
    return link.trust_policy in ["quarantine_default_partner", "experimental_partner", "suspended_partner"]

def summarize_federation_trust_state(links: List[RegistryFederationLinkRecord]) -> Dict[str, Any]:
    return {
        "total_links": len(links),
        "trusted_partners": sum(1 for l in links if l.trust_policy == "trusted_federated_partner")
    }
