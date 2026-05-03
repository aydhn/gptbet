from typing import List, Dict, Any
from .contracts import LiveExecutionEngineRecord

def build_execution_engine(engine_id: str, family: str) -> LiveExecutionEngineRecord:
    return LiveExecutionEngineRecord(
        engine_id=engine_id,
        engine_family=family,
        supported_lane_families=["refresh_freshness_metadata_lane", "reduce_replay_backlog_lane"],
        runtime_policy_ref=f"policy_{family}",
        renewal_policy_ref=f"renewal_{family}",
        rollback_policy_ref=f"rollback_{family}",
        closure_policy_ref=f"closure_{family}",
        active_status="active"
    )

def get_engine_families() -> List[str]:
    return [
        "bounded_lane_execution_engine",
        "rehearsal_aware_live_engine",
        "rollback_first_live_engine",
        "closure_supervised_engine",
        "review_bound_engine"
    ]
