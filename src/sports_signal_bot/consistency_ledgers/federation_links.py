from typing import List, Dict, Any, Optional
from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentCompilerFederationRecord,
    AlignmentFederationLinkRecord,
    FederationLinkStatus,
    FederatedAlignmentNodeRecord
)
from sports_signal_bot.consistency_ledgers.utils import generate_id

def add_alignment_federation_link(
    federation: AlignmentCompilerFederationRecord,
    source_node_ref: str,
    target_node_ref: str,
    status: FederationLinkStatus = FederationLinkStatus.LINK_CURRENT
) -> AlignmentFederationLinkRecord:
    """Adds a link between two nodes in the federation."""

    link = AlignmentFederationLinkRecord(
        link_id=generate_id("fed_link"),
        source_node_ref=source_node_ref,
        target_node_ref=target_node_ref,
        link_status=status,
        warnings=[]
    )

    federation.active_link_refs.append(link.link_id)
    return link

def validate_alignment_federation_link(
    link: AlignmentFederationLinkRecord,
    source_node: FederatedAlignmentNodeRecord,
    target_node: FederatedAlignmentNodeRecord
) -> AlignmentFederationLinkRecord:
    """Validates the link between two nodes. Downgrades link status if nodes are stale."""

    if source_node.currentness_state != "current" or target_node.currentness_state != "current":
        link.link_status = FederationLinkStatus.LINK_DEGRADED
        link.warnings.append("Link degraded due to stale node(s).")

    if "sovereignty_conflict" in source_node.warnings or "sovereignty_conflict" in target_node.warnings:
        link.link_status = FederationLinkStatus.LINK_BLOCKED
        link.warnings.append("Link blocked due to sovereignty conflict.")

    return link
