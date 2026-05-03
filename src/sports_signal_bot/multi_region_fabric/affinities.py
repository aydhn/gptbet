from typing import Optional
from sports_signal_bot.multi_region_fabric.contracts import RegionAffinityRecord

AFFINITY_TYPES = [
    "hard_local_affinity",
    "preferred_local_affinity",
    "treaty_transfer_affinity",
    "failover_affinity",
    "review_only_external_affinity",
    "no_external_affinity"
]

def resolve_region_affinity(affinity_id: str, a_type: str, target: Optional[str] = None) -> RegionAffinityRecord:
    if a_type not in AFFINITY_TYPES:
        raise ValueError(f"Unknown affinity: {a_type}")
    return RegionAffinityRecord(affinity_id=affinity_id, affinity_type=a_type, target_region=target)

def enforce_affinity_at_admission(affinity: RegionAffinityRecord, target_region: str) -> bool:
    if affinity.affinity_type == "hard_local_affinity":
        return False
    if affinity.affinity_type == "no_external_affinity":
        return False
    return True

def detect_affinity_conflicts(a1: RegionAffinityRecord, a2: RegionAffinityRecord) -> bool:
    return a1.affinity_type != a2.affinity_type

def summarize_affinity_pressure(affinities: list) -> str:
    return f"Evaluated {len(affinities)} affinities."
