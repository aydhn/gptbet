from typing import List, Optional
import datetime
from .contracts import (
    NarrativeCompilerFederationRecord,
    FederatedNarrativeNodeRecord,
    NarrativeFederationLinkRecord,
    NarrativeFederationCurrentnessRecord,
    NarrativeFederationHealthRecord,
    NarrativeFederationLinkStatus,
    NarrativeFederationOutputStatus
)

def build_narrative_compiler_federation(federation_id: str, family: str) -> NarrativeCompilerFederationRecord:
    return NarrativeCompilerFederationRecord(
        narrative_federation_id=federation_id,
        federation_family=family,
        currentness_policy_ref="default_currentness_policy",
        audience_policy_ref="default_audience_policy",
        caveat_policy_ref="default_caveat_policy",
        health_status="initializing"
    )

def add_narrative_federation_link(
    federation: NarrativeCompilerFederationRecord,
    link: NarrativeFederationLinkRecord
) -> NarrativeCompilerFederationRecord:
    federation.active_link_refs.append(link.link_id)
    return federation

def validate_narrative_federation_link(link: NarrativeFederationLinkRecord) -> bool:
    if link.status in [NarrativeFederationLinkStatus.link_blocked, NarrativeFederationLinkStatus.link_expired, NarrativeFederationLinkStatus.link_superseded]:
        return False
    return True

def compute_federated_narrative_currentness(nodes: List[FederatedNarrativeNodeRecord]) -> NarrativeFederationCurrentnessRecord:
    is_current = all(node.currentness_state.is_current for node in nodes)
    stale_sections = []
    for node in nodes:
        if not node.currentness_state.is_current:
            stale_sections.extend(node.currentness_state.stale_sections)
    return NarrativeFederationCurrentnessRecord(
        is_current=is_current,
        stale_sections=stale_sections,
        last_refresh=datetime.datetime.now(datetime.UTC),
        expires_at=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    )

def summarize_narrative_federation_health(federation: NarrativeCompilerFederationRecord, nodes: List[FederatedNarrativeNodeRecord]) -> NarrativeFederationHealthRecord:
    currentness = compute_federated_narrative_currentness(nodes)
    is_healthy = currentness.is_current and not federation.warnings
    score = 1.0 if is_healthy else (0.5 if not currentness.is_current else 0.8)
    return NarrativeFederationHealthRecord(
        is_healthy=is_healthy,
        score=score,
        health_issues=currentness.stale_sections
    )

def aggregate_federated_narratives(nodes: List[FederatedNarrativeNodeRecord]) -> NarrativeFederationOutputStatus:
    currentness = compute_federated_narrative_currentness(nodes)
    if not currentness.is_current:
        return NarrativeFederationOutputStatus.federated_narrative_stale

    has_caveats = any(node.caveat_state for node in nodes)
    if has_caveats:
        return NarrativeFederationOutputStatus.federated_narrative_caveated

    return NarrativeFederationOutputStatus.federated_narrative_current_with_caps

def preserve_caveats_in_federation(nodes: List[FederatedNarrativeNodeRecord]) -> List[str]:
    caveats = []
    for node in nodes:
        for caveat in node.caveat_state:
            caveats.append(caveat.description)
    return caveats

def preserve_no_safe_sections_in_federation(nodes: List[FederatedNarrativeNodeRecord]) -> List[str]:
    no_safe_sections = []
    for node in nodes:
        for caveat in node.caveat_state:
            if caveat.requires_no_safe_visibility:
                no_safe_sections.append(f"Node {node.node_id}: {caveat.description}")
    return no_safe_sections

def explain_federated_narrative_output(status: NarrativeFederationOutputStatus, caveats: List[str]) -> str:
    return f"Status: {status.value}. Caveats: {', '.join(caveats)}"
