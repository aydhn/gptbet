import json
import uuid
from typing import Dict, Any, List

from .guards import build_concurrency_guard, summarize_concurrency_guards
from .parallelism import build_parallel_execution_plan, summarize_parallel_execution
from .ordering import build_async_ordering_graph, detect_ordering_violation, summarize_async_ordering
from .race_probes import build_race_probe_run, perturb_execution_schedule, detect_race_signals, summarize_race_probes
from .shared_state import register_shared_state_surface, register_state_owner, summarize_shared_state_conflicts
from .idempotency import build_idempotency_contract, build_idempotency_key, summarize_idempotency_health
from .stale_reads import capture_freshness_snapshot, compare_read_versions, summarize_stale_read_risks
from .queues import build_queue_discipline, sample_queue_pressure, summarize_queue_health
from .timeouts import run_timeout_probe, detect_cancellation_leaks, summarize_timeout_and_cancellation
from .regressions import ConcurrencyBaselineRecord, ConcurrencyComparisonRecord, detect_concurrency_regressions, summarize_concurrency_regressions
from .manifests import build_overall_health_report

from .contracts import (
    StaleReadRecord, QueueDisciplineRecord, QueueSampleRecord,
    CancellationRunRecord, TimeoutRunRecord, StateConflictRecord,
    DuplicateExecutionRecord
)

def run_concurrency_hardening_pass(strategy_name: str = "ConservativeConcurrencyHardeningStrategy") -> Dict[str, Any]:
    """Runs a full concurrency hardening pass simulating all checks."""

    # 1. Guards
    guards = [
        build_concurrency_guard("shared_state_guard", "surface_1", {"type": "read_write"}, "owner_A", {"order": "strict"}, 5000, "abort"),
        build_concurrency_guard("async_join_guard", "surface_2", {"type": "merge"}, "owner_B", {"order": "relaxed"}, 35000, "drop") # will trigger warning
    ]
    guards_manifest = summarize_concurrency_guards(guards)

    # 2. Parallelism
    plans = [
        build_parallel_execution_plan("bounded_preview_parallelism", 4, 4, 100, "wait_all", 16, "drop"),
        build_parallel_execution_plan("trace_query_parallelism", 10, 20, 1000, "first_n", 128, "throttle") # will trigger warning
    ]
    parallelism_manifest = summarize_parallel_execution(plans)

    # 3. Ordering
    orderings = [
        build_async_ordering_graph("process_a", {"deterministic_merge": True, "expected_sequence": ["step1", "step2"]}),
        build_async_ordering_graph("process_b", {"expected_sequence": ["step1"]}) # missing deterministic_merge
    ]
    ordering_manifest = summarize_async_ordering(orderings)

    # 4. Race Probes
    race_runs = [
        build_race_probe_run("simultaneous_read_write_probe", 42, "interleave"),
        build_race_probe_run("async_join_reorder_probe", 1337, "reverse")
    ]
    # simulate a race detection
    detect_race_signals(race_runs[1], "state_A", "state_B")
    race_manifest = summarize_race_probes(race_runs)

    # 5. Shared State
    states = [
        register_shared_state_surface("owner_C", "cache_ledger")
    ]
    conflicts = [StateConflictRecord(conflict_id=f"conf_{uuid.uuid4().hex[:8]}", description="concurrent write detected")]
    state_manifest = summarize_shared_state_conflicts(states, conflicts)

    # 6. Idempotency
    idem_records = [
        build_idempotency_contract("side_effect_A", "key_123")
    ]
    duplicates = [DuplicateExecutionRecord(duplicate_id=f"dup_{uuid.uuid4().hex[:8]}", description="Duplicate write attempt caught")]
    idem_manifest = summarize_idempotency_health(idem_records, duplicates)

    # 7. Stale Reads
    stale_records = [
        StaleReadRecord(stale_read_id=f"sr_{uuid.uuid4().hex[:8]}", target_ref="query_1", drift_window_ref="dw_1", status="ok", warnings=[])
    ]
    stale_manifest = summarize_stale_read_risks(stale_records)

    # 8. Queues
    queue_disciplines = [
        build_queue_discipline("main_event_queue")
    ]
    queue_manifest = summarize_queue_health(queue_disciplines)

    # 9. Timeouts / Cancellations
    timeout_runs = [
        run_timeout_probe("worker_1", True)
    ]
    leaks = detect_cancellation_leaks([CancellationRunRecord(run_id="cr1", target_ref="w2", status="cancellation_simulated", warnings=[])])
    timeout_manifest = summarize_timeout_and_cancellation(timeout_runs, leaks)

    # 10. Regressions
    baseline = ConcurrencyBaselineRecord(baseline_id="base1", metrics={"races": 0, "drift_ms": 10})
    current = ConcurrencyComparisonRecord(comparison_id="curr1", metrics={"races": 1, "drift_ms": 15})
    regressions = detect_concurrency_regressions(baseline, current)
    regression_manifest = summarize_concurrency_regressions(regressions)


    # Overall Health
    manifests = {
        "guards": guards_manifest,
        "parallelism": parallelism_manifest,
        "ordering": ordering_manifest,
        "race_probes": race_manifest,
        "shared_state": state_manifest,
        "idempotency": idem_manifest,
        "stale_reads": stale_manifest,
        "queues": queue_manifest,
        "timeouts": timeout_manifest,
        "regressions": regression_manifest
    }

    health_report = build_overall_health_report(manifests)

    return {
        "manifests": {k: v.model_dump() for k, v in manifests.items()},
        "overall_health": health_report["overall_health"]
    }
