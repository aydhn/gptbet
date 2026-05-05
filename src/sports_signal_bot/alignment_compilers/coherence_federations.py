from typing import List, Dict, Optional
import datetime
from .contracts import (
    CoherenceScorerFederationRecord,
    FederatedCoherenceNodeRecord,
    CoherenceFederationWarningRecord,
    CoherenceFederationLinkRecord,
    CoherenceFederationCurrentnessRecord,
    CoherenceFederationAgreementRecord
)

def build_coherence_scorer_federation(
    federation_id: str,
    family: str,
    currentness_policy: str,
    ceiling_policy: str,
    agreement_policy: str
) -> CoherenceScorerFederationRecord:
    """Builds a new coherence scorer federation."""
    return CoherenceScorerFederationRecord(
        coherence_federation_id=federation_id,
        federation_family=family,
        member_scorer_refs=[],
        active_link_refs=[],
        currentness_policy_ref=currentness_policy,
        ceiling_policy_ref=ceiling_policy,
        agreement_policy_ref=agreement_policy,
        health_status="initializing",
        warnings=[],
        nodes=[]
    )

def add_coherence_federation_link(
    federation: CoherenceScorerFederationRecord,
    source_ref: str,
    target_ref: str,
    status: str
) -> CoherenceFederationLinkRecord:
    """Adds a link between nodes in the federation."""
    link = CoherenceFederationLinkRecord(
        link_id=f"link_{source_ref}_{target_ref}",
        source_ref=source_ref,
        target_ref=target_ref,
        status=status
    )
    federation.active_link_refs.append(link.link_id)
    return link

def validate_coherence_federation_link(link: CoherenceFederationLinkRecord) -> bool:
    """Validates the status of a federation link."""
    valid_statuses = [
        "link_current", "link_caveated", "link_review_only",
        "link_degraded", "link_blocked", "link_expired", "link_superseded"
    ]
    return link.status in valid_statuses

def compute_federated_coherence_currentness(
    federation: CoherenceScorerFederationRecord,
    node_currentness: Dict[str, str]
) -> CoherenceFederationCurrentnessRecord:
    """Computes the overall currentness of the federation."""
    state = "current"
    caveats = []

    for node_id, currentness in node_currentness.items():
        if currentness == "stale":
            state = "stale"
            caveats.append(f"Node {node_id} is stale")
            break
        elif currentness == "caveated":
            state = "caveated"
            caveats.append(f"Node {node_id} has currentness caveats")

    return CoherenceFederationCurrentnessRecord(
        state=state,
        last_updated=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        caveat_refs=caveats
    )

def summarize_coherence_federation_health(
    federation: CoherenceScorerFederationRecord
) -> Dict[str, str]:
    """Summarizes the health of the federation."""
    return {
        "federation_id": federation.coherence_federation_id,
        "status": federation.health_status,
        "nodes_count": str(len(federation.nodes)),
        "warnings_count": str(len(federation.warnings))
    }

def aggregate_federated_coherence_outputs(
    federation: CoherenceScorerFederationRecord,
    outputs: List[str]
) -> str:
    """Aggregates outputs from the federation, determining the overall band."""
    if not outputs:
         return "federated_coherence_blocked"

    if "stale" in outputs:
        return "federated_coherence_stale"
    if "blocked" in outputs:
        return "federated_coherence_blocked"
    if "degraded" in outputs:
        return "federated_coherence_degraded"
    if "review_only" in outputs:
        return "federated_coherence_review_only"
    if "caveated" in outputs:
        return "federated_coherence_caveated"

    return "federated_coherence_current_with_caps"

def preserve_penalties_and_ceilings_in_federation(
    federation: CoherenceScorerFederationRecord,
    penalties: List[str]
) -> List[str]:
    """Ensures penalties and ceilings are preserved."""
    return [p for p in penalties]

def preserve_no_safe_visibility_in_coherence_federation(
    federation: CoherenceScorerFederationRecord,
    no_safe_hints: List[str]
) -> List[str]:
    """Ensures no-safe visibility is preserved in the federation."""
    return [h for h in no_safe_hints]

def explain_federated_coherence_output(
    band: str,
    penalties: List[str],
    no_safe_hints: List[str]
) -> str:
    """Explains the reason for the federated output band."""
    return f"Band: {band}. Penalties: {len(penalties)}. No-Safe Hints: {len(no_safe_hints)}."

def compute_coherence_federation_agreement(
    outputs: List[str]
) -> CoherenceFederationAgreementRecord:
    """Computes the agreement band for the federation outputs."""
    # Simplified agreement calculation
    if not outputs:
        return CoherenceFederationAgreementRecord(agreement_band="no_agreement", score=0.0)

    unique_outputs = set(outputs)
    if len(unique_outputs) == 1:
        if "stale" in outputs or "blocked" in outputs or "degraded" in outputs:
            return CoherenceFederationAgreementRecord(agreement_band="bounded_agreement", score=0.5)
        return CoherenceFederationAgreementRecord(agreement_band="stable_agreement", score=1.0)
    elif len(unique_outputs) == len(outputs):
        return CoherenceFederationAgreementRecord(agreement_band="no_agreement", score=0.0)
    else:
        return CoherenceFederationAgreementRecord(agreement_band="weak_agreement", score=0.3)

def detect_agreement_instability(
    agreement: CoherenceFederationAgreementRecord
) -> bool:
    """Detects if the agreement is unstable."""
    return agreement.agreement_band in ["no_agreement", "weak_agreement"]

def summarize_federation_agreement(
    agreement: CoherenceFederationAgreementRecord
) -> str:
    """Summarizes the federation agreement."""
    return f"Agreement: {agreement.agreement_band} ({agreement.score})"

def explain_agreement_caps(
    agreement: CoherenceFederationAgreementRecord,
    staleness_present: bool
) -> str:
    """Explains why agreement is capped."""
    if staleness_present:
        return f"Agreement capped at {agreement.agreement_band} due to stale inputs."
    return f"Agreement capped at {agreement.agreement_band} due to divergent outputs."
