from typing import List
from sports_signal_bot.multi_region_fabric.contracts import ShardRoutingDecisionRecord

ROUTING_OUTCOMES = [
    "routed_local_shard",
    "routed_local_shard_with_backpressure",
    "routed_treaty_permitted_external_shard",
    "routed_review_only_external_shard",
    "denied_by_sovereignty",
    "denied_by_treaty",
    "delayed_pending_failover",
    "delayed_pending_revalidation"
]

def route_token_request_to_shard(req_id: str, shard_id: str) -> ShardRoutingDecisionRecord:
    return ShardRoutingDecisionRecord(
        decision_id=f"rt_{req_id}",
        shard_id=shard_id,
        outcome="routed_local_shard",
        reasoning="Local region preference"
    )

def evaluate_shard_routing(req_id: str, shard_id: str, local: bool) -> str:
    return "routed_local_shard" if local else "denied_by_sovereignty"

def apply_region_and_treaty_constraints(shard_id: str) -> bool:
    return True

def compute_shard_backpressure(shard_id: str) -> float:
    return 0.1

def summarize_shard_routing(decisions: List[ShardRoutingDecisionRecord]) -> str:
    return f"Routed {len(decisions)} requests."
