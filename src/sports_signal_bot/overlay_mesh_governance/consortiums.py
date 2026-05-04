from typing import List, Dict, Any, Optional
from sports_signal_bot.overlay_mesh_governance.contracts import (
    BenchmarkSignalConsortiumRecord,
    ConsortiumLayerRecord,
    ConsortiumMemberRecord,
    ConsortiumHealthRecord
)

def build_benchmark_signal_consortium(
    consortium_id: str,
    consortium_family: str
) -> BenchmarkSignalConsortiumRecord:
    return BenchmarkSignalConsortiumRecord(
        consortium_id=consortium_id,
        consortium_family=consortium_family,
        layer_refs=[],
        member_refs=[],
        active_signal_refs=[],
        provenance_rules={},
        corroboration_rules={},
        suppression_rules={},
        health_status=ConsortiumHealthRecord(status="healthy", details={})
    )

def add_consortium_layer(consortium: BenchmarkSignalConsortiumRecord, layer: ConsortiumLayerRecord) -> BenchmarkSignalConsortiumRecord:
    if layer.layer_id not in consortium.layer_refs:
        consortium.layer_refs.append(layer.layer_id)
    return consortium

def register_consortium_member(consortium: BenchmarkSignalConsortiumRecord, member: ConsortiumMemberRecord) -> BenchmarkSignalConsortiumRecord:
    if member.member_id not in consortium.member_refs:
        consortium.member_refs.append(member.member_id)
    return consortium

def summarize_consortium_health(consortium: BenchmarkSignalConsortiumRecord) -> ConsortiumHealthRecord:
    if consortium.warnings:
        consortium.health_status.status = "degraded"
        consortium.health_status.details["warning_count"] = str(len(consortium.warnings))
    else:
        consortium.health_status.status = "healthy"
    return consortium.health_status
