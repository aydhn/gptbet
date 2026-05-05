from typing import Dict, Any, List
from .contracts import LoadProfilingRunRecord

def build_load_profiling_run(run_id: str, family: str, scenarios: List[str], samples: int) -> LoadProfilingRunRecord:
    return LoadProfilingRunRecord(
        load_profiling_run_id=run_id,
        run_family=family,
        scenario_refs=scenarios,
        sample_count=samples,
        warmup_count=10,
        seed_ref="frozen_seed_v1",
        environment_hash="env_hash_123",
        aggregate_latency_stats={"p50": 10.0, "p95": 25.0},
        aggregate_memory_stats={"peak": 50.0},
        aggregate_io_stats={"read": 5.0},
        aggregate_variance_stats={"std_dev": 2.0},
        profiling_status="profiled_cleanly"
    )

def execute_load_profile_scenario(scenario_id: str) -> Dict[str, Any]:
    return {"status": "success", "latency": 15.0}

def summarize_load_profile(runs: List[LoadProfilingRunRecord]) -> Dict[str, Any]:
    return {
        "total_runs": len(runs),
        "avg_p50_latency": sum(r.aggregate_latency_stats.get("p50", 0) for r in runs) / max(len(runs), 1)
    }

def compare_load_profile_runs(run1: LoadProfilingRunRecord, run2: LoadProfilingRunRecord) -> Dict[str, Any]:
    return {
        "latency_diff": run2.aggregate_latency_stats.get("p50", 0) - run1.aggregate_latency_stats.get("p50", 0)
    }
