from typing import List, Dict
from .contracts import (
    FederatedObservatoryNodeRecord,
    ObservatoryFederationLinkRecord
)

class ObservatoryNodeFreshnessRecord:
    def __init__(self, node_id: str, is_fresh: bool):
        self.node_id = node_id
        self.is_fresh = is_fresh

def verify_observatory_node_freshness(nodes: List[FederatedObservatoryNodeRecord]) -> List[ObservatoryNodeFreshnessRecord]:
    return [ObservatoryNodeFreshnessRecord(n.node_id, not n.is_stale) for n in nodes]

def compute_observatory_link_lag(links: List[ObservatoryFederationLinkRecord]) -> int:
    return sum(l.lag_ms for l in links)

def detect_observatory_federation_gaps(nodes: List[FederatedObservatoryNodeRecord]) -> List[str]:
    return [n.node_id for n in nodes if not n.owner_ref]

def summarize_observatory_federation_links(links: List[ObservatoryFederationLinkRecord]) -> Dict[str, int]:
    return {
        "total_links": len(links),
        "blocked_links": sum(1 for l in links if l.is_blocked),
        "total_lag_ms": compute_observatory_link_lag(links)
    }
