from typing import List, Dict, Any
import uuid
from .contracts import (
    ScaledHubRoutingMeshRecord, MeshTierRecord, MeshPartitionRecord, MeshPressureSegmentRecord
)

def build_mesh_partitions() -> List[MeshPartitionRecord]:
    return [
        MeshPartitionRecord(
            partition_id="part-bounded",
            scope_class="bounded",
            sovereignty_restriction_class="strict",
            pressure_class="low",
            route_limits={"max_routes": 100},
            active_routes=10,
            pressure_segments=[
                MeshPressureSegmentRecord(segment_id="seg-1", pressure_level="low", queue_depth=0, degradation_active=False)
            ]
        ),
        MeshPartitionRecord(
            partition_id="part-review-only",
            scope_class="review_only",
            sovereignty_restriction_class="moderate",
            pressure_class="high",
            route_limits={"max_routes": 500},
            active_routes=450,
            pressure_segments=[
                MeshPressureSegmentRecord(segment_id="seg-2", pressure_level="high", queue_depth=150, degradation_active=True)
            ]
        )
    ]

def build_scaled_mesh_topology(mesh_ref: str) -> ScaledHubRoutingMeshRecord:
    tiers = [
        MeshTierRecord(
            tier_id="tier-local",
            tier_family="local_tier",
            participating_hub_refs=["hub-local-1"],
            supported_exchange_scopes=["bounded"],
            route_capacity_class="high",
            health_policy_ref="pol-1",
            degradation_policy_ref="deg-1",
            warnings=[]
        )
    ]
    partitions = build_mesh_partitions()

    return ScaledHubRoutingMeshRecord(
        scaled_mesh_id=f"sm-{uuid.uuid4().hex[:8]}",
        mesh_ref=mesh_ref,
        tier_refs=tiers,
        partition_refs=partitions,
        route_class_refs=["low_pressure_bounded_route", "review_only_route"],
        capacity_refs=["cap-1"],
        pressure_segments=partitions[0].pressure_segments + partitions[1].pressure_segments,
        health_status="degraded" if any(p.pressure_class == "high" for p in partitions) else "healthy",
        warnings=["high_pressure_on_review_partition"] if any(p.pressure_class == "high" for p in partitions) else []
    )
