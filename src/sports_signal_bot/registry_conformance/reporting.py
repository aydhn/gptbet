# reporting.py
from typing import Dict, List
from .contracts import (
    CorridorRegistryRecord,
    AttestationExchangePacketRecord,
    BenchmarkComparisonRecord,
    SovereignPolicyConformancePackRecord,
)


def generate_registry_conformance_summary(
    registries: List[CorridorRegistryRecord],
    exchanges: List[AttestationExchangePacketRecord],
    comparisons: List[BenchmarkComparisonRecord],
    packs: List[SovereignPolicyConformancePackRecord],
) -> Dict:

    registry_health_counts = {}
    for r in registries:
        h = r.health_status.status
        registry_health_counts[h] = registry_health_counts.get(h, 0) + 1

    exchange_status_counts = {}
    for e in exchanges:
        s = e.exchange_status
        exchange_status_counts[s] = exchange_status_counts.get(s, 0) + 1

    pack_status_counts = {}
    for p in packs:
        s = p.conformance_status
        pack_status_counts[s] = pack_status_counts.get(s, 0) + 1

    return {
        "summary": {
            "total_registries": len(registries),
            "registry_health_distribution": registry_health_counts,
            "total_exchanges": len(exchanges),
            "exchange_status_distribution": exchange_status_counts,
            "total_comparisons": len(comparisons),
            "total_packs": len(packs),
            "pack_status_distribution": pack_status_counts,
        }
    }
