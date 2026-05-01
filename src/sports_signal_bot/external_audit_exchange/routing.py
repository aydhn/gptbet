from typing import List
from .contracts import ChallengeRoutingRecord, ChallengeExchangePacketRecord, ChallengeClusterRecord
import uuid

def route_challenge_packet(packet: ChallengeExchangePacketRecord, reputation: float) -> ChallengeRoutingRecord:
    priority = 50.0
    if packet.severity == "critical":
        priority = 90.0

    suggested_class = "standard"
    if priority > 80:
        suggested_class = "expert"

    return ChallengeRoutingRecord(
        routing_id=str(uuid.uuid4()),
        challenge_ref=packet.challenge_ref,
        suggested_responder_class=suggested_class,
        priority_score=priority
    )

def cluster_similar_challenges(packets: List[ChallengeExchangePacketRecord]) -> List[ChallengeClusterRecord]:
    clusters = {}
    for packet in packets:
        if packet.target_ref not in clusters:
            clusters[packet.target_ref] = []
        clusters[packet.target_ref].append(packet.challenge_ref)

    results = []
    for target_ref, refs in clusters.items():
        results.append(ChallengeClusterRecord(
            cluster_id=str(uuid.uuid4()),
            challenge_refs=refs,
            cluster_reason=f"Shared target_ref {target_ref}"
        ))
    return results

def score_challenge_priority(packet: ChallengeExchangePacketRecord) -> float:
    if packet.severity == "critical": return 95.0
    if packet.severity == "high": return 75.0
    return 50.0

def suggest_responder_classes(packet: ChallengeExchangePacketRecord) -> List[str]:
    if packet.severity == "critical":
        return ["expert", "verified_auditor"]
    return ["standard", "peer"]

def summarize_marketplace_readiness(routers: List[ChallengeRoutingRecord]) -> str:
    return f"Ready to route {len(routers)} challenges."
