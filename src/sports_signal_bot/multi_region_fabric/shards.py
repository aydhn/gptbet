from typing import List
from sports_signal_bot.multi_region_fabric.contracts import BrokerShardRecord

SHARD_FAMILIES = [
    "execution_token_shard",
    "renewal_shard",
    "rollback_reserve_shard",
    "closure_shard",
    "review_scope_shard",
    "federated_adaptation_shard",
    "treaty_limited_shard"
]

def build_broker_shards(shard_id: str, family: str, region: str, cluster: str) -> BrokerShardRecord:
    return BrokerShardRecord(
        shard_id=shard_id,
        shard_family=family,
        owning_region_ref=region,
        owning_cluster_ref=cluster,
        token_family_scope=["*"],
        approval_domain_scope=["*"],
        failover_candidates=[],
        current_status="active"
    )

def validate_shard_single_owner(shard: BrokerShardRecord) -> bool:
    return bool(shard.owning_region_ref and shard.owning_cluster_ref)

def detect_cross_shard_lineage_conflicts(shard1: BrokerShardRecord, shard2: BrokerShardRecord) -> bool:
    return shard1.shard_id == shard2.shard_id and shard1.owning_region_ref != shard2.owning_region_ref

def require_snapshot_for_handoff(shard: BrokerShardRecord) -> bool:
    return True

def explain_shard_ownership_decision(shard: BrokerShardRecord) -> str:
    return f"Shard {shard.shard_id} owned by {shard.owning_region_ref}"
