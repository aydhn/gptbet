# integration.py
from typing import Dict, List, Any
from datetime import datetime, timezone

from .contracts import (
    CorridorRegistryRecord,
    RegistryEntryRecord,
    AttestationExchangePacketRecord,
    TreatyBenchmarkBaselineRecord,
    BenchmarkComparisonRecord,
    SovereignPolicyConformancePackRecord,
    ConformancePackDimensionRecord,
)

from .registries import (
    build_corridor_registry,
    register_registry_entry,
    update_current_pointer,
)
from .entries import build_registry_entry
from .currentness import compute_currentness
from .exchanges import (
    build_attestation_exchange_packet,
    validate_attestation_for_exchange,
    apply_exchange_constraints,
)
from .comparisons import compare_treaty_to_baseline
from .packs import build_policy_conformance_pack


def build_registry_to_pack_flow(
    corridor_data: Dict[str, Any],
    treaty_data: Dict[str, Any],
    attestation_refs: List[str],
    baseline: TreatyBenchmarkBaselineRecord,
    required_dimensions: List[ConformancePackDimensionRecord],
    evidence: List[Any],
    valid_until: datetime,
) -> Dict[str, Any]:
    """End to end flow: registry -> exchange -> baseline -> pack -> update pointers."""

    registry = build_corridor_registry("sovereign_corridor_registry", "scope_global")

    corridor_entry = build_registry_entry(
        "corridor_entry", corridor_data.get("id", "c1"), "v1.0.0", None, valid_until
    )
    treaty_entry = build_registry_entry(
        "treaty_entry", treaty_data.get("id", "t1"), "v1.0.0", None, valid_until
    )

    registry = register_registry_entry(registry, corridor_entry)
    registry = register_registry_entry(registry, treaty_entry)

    registry = update_current_pointer(
        registry, "corridor_scope", corridor_entry.registry_entry_id
    )
    registry = update_current_pointer(
        registry, "treaty_scope", treaty_entry.registry_entry_id
    )

    packet = build_attestation_exchange_packet(
        source_registry_ref=registry.registry_id,
        attestation_refs=attestation_refs,
        corridor_refs=[corridor_entry.registry_entry_id],
        treaty_refs=[treaty_entry.registry_entry_id],
        scope="baseline_comparison_support",
        valid_until=valid_until,
    )

    exchange_decision = validate_attestation_for_exchange(packet)

    comparison = compare_treaty_to_baseline(
        treaty_entry.registry_entry_id, treaty_data, baseline
    )

    pack = build_policy_conformance_pack(
        target_scope_ref="target_region",
        required_dimensions=required_dimensions,
        evidence=evidence,
        valid_until=valid_until,
        corridor_refs=[corridor_entry.registry_entry_id],
        treaty_refs=[treaty_entry.registry_entry_id],
    )

    return {
        "registry": registry,
        "corridor_entry": corridor_entry,
        "treaty_entry": treaty_entry,
        "exchange_packet": packet,
        "exchange_decision": exchange_decision,
        "benchmark_comparison": comparison,
        "conformance_pack": pack,
    }
