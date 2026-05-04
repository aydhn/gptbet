import uuid
from typing import List

from .contracts import (
    BaselineRegistryFederationRecord, FederatedBaselineRegistryNodeRecord,
    BaselineFederationCurrentnessRecord, BaselineFederationLinkRecord
)

def build_baseline_registry_federation(family: str) -> BaselineRegistryFederationRecord:
    return BaselineRegistryFederationRecord(
        baseline_federation_id=f"fed_{uuid.uuid4().hex[:8]}",
        federation_family=family,
        member_registry_refs=[],
        active_link_refs=[],
        currentness_policy_ref="default_currentness",
        applicability_policy_ref="default_applicability",
        supersession_policy_ref="default_supersession",
        health_status="healthy",
        warnings=[]
    )

def add_baseline_federation_link(fed: BaselineRegistryFederationRecord, source: str, target: str) -> BaselineFederationLinkRecord:
    link = BaselineFederationLinkRecord(
        link_id=f"link_{uuid.uuid4().hex[:8]}",
        source_node_ref=source,
        target_node_ref=target,
        status="active"
    )
    fed.active_link_refs.append(link.link_id)
    return link

def project_baseline_currentness_across_federation(
    fed: BaselineRegistryFederationRecord, source_pointer: str, is_stale: bool, mismatch: bool
) -> BaselineFederationCurrentnessRecord:

    outcome = "projected_current"
    caveats = []

    if is_stale:
        outcome = "projected_stale_current"
        caveats.append("Stale federated baseline caps projection strength")
        fed.warnings.append("Stale baseline detected in federation")
        fed.health_status = "degraded"

    if mismatch:
        outcome = "projected_current_with_caveats" if not is_stale else "projected_stale_current"
        caveats.append("Applicability or sovereignty mismatch")

    return BaselineFederationCurrentnessRecord(
        currentness_id=f"curr_{uuid.uuid4().hex[:8]}",
        source_current_pointer=source_pointer,
        federated_current_projection=f"proj_{source_pointer}",
        successor_projection="none",
        applicability_projection="bounded",
        freshness_projection="stale" if is_stale else "fresh",
        replay_need=is_stale or mismatch,
        caveat_burden=caveats,
        federation_drift_status="drifted" if mismatch else "aligned",
        currentness_outcome=outcome
    )

def summarize_baseline_federation(fed: BaselineRegistryFederationRecord) -> str:
    return f"Federation {fed.baseline_federation_id} ({fed.federation_family}): Links={len(fed.active_link_refs)}, Health={fed.health_status}"
