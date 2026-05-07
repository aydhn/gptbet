from dataclasses import dataclass
from typing import List
from .contracts import MeshFederationLinkRecord

@dataclass
class MeshFederationGapRecord:
    gap_id: str

@dataclass
class MeshFederationRollbackRecord:
    rollback_id: str

@dataclass
class MeshFederationAsymmetryRecord:
    asymmetry_id: str

@dataclass
class MeshFederationReplayRecord:
    replay_id: str

@dataclass
class MeshFederationHealthMarkerRecord:
    marker_id: str

@dataclass
class MeshFederationVoteLineageRecord:
    lineage_id: str

def detect_mesh_federation_asymmetry(links: List[MeshFederationLinkRecord]) -> List[MeshFederationAsymmetryRecord]:
    asymmetries = []
    # Basic logic: if we have links but they seem to imply an asymmetric relation, flag it.
    if len(links) % 2 != 0:
         asymmetries.append(MeshFederationAsymmetryRecord(asymmetry_id="asym-01"))
    return asymmetries

def classify_mesh_federation_agreement(links: List[MeshFederationLinkRecord]) -> str:
    if not links:
        return "no_agreement"
    stale_links = [l for l in links if l.is_stale]
    if stale_links:
        return "weak_agreement"
    return "stable_agreement"

def validate_mesh_federation_links(links: List[MeshFederationLinkRecord]) -> bool:
    return all(not l.is_stale for l in links) and len(links) > 0

def summarize_mesh_federation_links(links: List[MeshFederationLinkRecord]) -> dict:
    return {
        "total_links": len(links),
        "stale_links": sum(1 for l in links if l.is_stale)
    }
