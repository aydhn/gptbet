from .contracts import IncrementalPlanRecord, RecomputeDecisionRecord
from typing import List

class IncrementalEngine:
    def __init__(self):
        pass

    def decide_full_vs_incremental(self, changeset_size: int, threshold: int) -> RecomputeDecisionRecord:
        if changeset_size > threshold:
            return RecomputeDecisionRecord(decision="full_rebuild", reason="changeset too large", cost_estimate=100.0)
        return RecomputeDecisionRecord(decision="incremental_append", reason="changeset within limits", cost_estimate=10.0)

    def build_incremental_recompute_plan(self, decision: RecomputeDecisionRecord, entities: List[str]) -> IncrementalPlanRecord:
        return IncrementalPlanRecord(
            plan_id="plan_001",
            strategy=decision.decision,
            affected_entities=entities,
            estimated_cost=decision.cost_estimate
        )

    def execute_incremental_recompute(self, plan: IncrementalPlanRecord):
        pass

def detect_changeset() -> List[str]:
    return ["fixture_123"]

def derive_incremental_scope(changes: List[str]) -> List[str]:
    return changes

def estimate_recompute_cost(scope: List[str]) -> float:
    return len(scope) * 1.5

def estimate_incremental_benefit(full_cost: float, inc_cost: float) -> float:
    return full_cost - inc_cost

def classify_recompute_strategy(decision: str) -> str:
    return decision

def explain_recompute_decision(decision: RecomputeDecisionRecord) -> str:
    return f"Decision: {decision.decision} due to {decision.reason} (cost: {decision.cost_estimate})"
