from typing import Dict, Any, List
from .contracts import (
    PartitionSliceRecord, SegmentAllocationRecord, RolloutPartitionPlanRecord
)

def build_rollout_partition(plan_id: str, cohort_id: str, slices: List[Dict[str, Any]]) -> RolloutPartitionPlanRecord:
    partition_slices = [
        PartitionSliceRecord(slice_id=f"{plan_id}_slice_{i}", scope_slice=s)
        for i, s in enumerate(slices)
    ]
    return RolloutPartitionPlanRecord(
        plan_id=plan_id,
        cohort_id=cohort_id,
        slices=partition_slices
    )

def assign_entities_to_cohort_slice(segment_id: str, ratio: float) -> SegmentAllocationRecord:
    return SegmentAllocationRecord(
        segment_id=segment_id,
        allocation_ratio=ratio
    )

def validate_partition_fairness(plan: RolloutPartitionPlanRecord) -> bool:
    return len(plan.slices) > 0

def summarize_partition_coverage(plan: RolloutPartitionPlanRecord) -> Dict[str, Any]:
    return {
        "plan_id": plan.plan_id,
        "total_slices": len(plan.slices)
    }
