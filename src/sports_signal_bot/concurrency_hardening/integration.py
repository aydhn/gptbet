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

def _process_guards() -> Any:
    guards = [
        build_concurrency_guard("shared_state_guard", "surface_1", {"type": "read_write"}, "owner_A", {"order": "strict"}, 5000, "abort"),
        build_concurrency_guard("async_join_guard", "surface_2", {"type": "merge"}, "owner_B", {"order": "relaxed"}, 35000, "drop") # will trigger warning
    ]
    return summarize_concurrency_guards(guards)

def _process_parallelism() -> Any:
    plans = [
        build_parallel_execution_plan("bounded_preview_parallelism", 4, 4, 100, "wait_all", 16, "drop"),
        build_parallel_execution_plan("trace_query_parallelism", 10, 20, 1000, "first_n", 128, "throttle") # will trigger warning
    ]
    return summarize_parallel_execution(plans)

def _process_ordering() -> Any:
    orderings = [
        build_async_ordering_graph("process_a", {"deterministic_merge": True, "expected_sequence": ["step1", "step2"]}),
        build_async_ordering_graph("process_b", {"expected_sequence": ["step1"]}) # missing deterministic_merge
    ]
    return summarize_async_ordering(orderings)

def _process_race_probes() -> Any:
    race_runs = [
        build_race_probe_run("simultaneous_read_write_probe", 42, "interleave"),
        build_race_probe_run("async_join_reorder_probe", 1337, "reverse")
    ]
    # simulate a race detection
    detect_race_signals(race_runs[1], "state_A", "state_B")
    return summarize_race_probes(race_runs)

def _process_shared_state() -> Any:
    states = [
        register_shared_state_surface("owner_C", "cache_ledger")
    ]
    conflicts = [StateConflictRecord(conflict_id=f"conf_{uuid.uuid4().hex[:8]}", description="concurrent write detected")]
    return summarize_shared_state_conflicts(states, conflicts)

def _process_idempotency() -> Any:
    idem_records = [
        build_idempotency_contract("side_effect_A", "key_123")
    ]
    duplicates = [DuplicateExecutionRecord(duplicate_id=f"dup_{uuid.uuid4().hex[:8]}", description="Duplicate write attempt caught")]
    return summarize_idempotency_health(idem_records, duplicates)

def _process_stale_reads() -> Any:
    stale_records = [
        StaleReadRecord(stale_read_id=f"sr_{uuid.uuid4().hex[:8]}", target_ref="query_1", drift_window_ref="dw_1", status="ok", warnings=[])
    ]
    return summarize_stale_read_risks(stale_records)

def _process_queues() -> Any:
    queue_disciplines = [
        build_queue_discipline("main_event_queue")
    ]
    return summarize_queue_health(queue_disciplines)

def _process_timeouts() -> Any:
    timeout_runs = [
        run_timeout_probe("worker_1", True)
    ]
    leaks = detect_cancellation_leaks([CancellationRunRecord(run_id="cr1", target_ref="w2", status="cancellation_simulated", warnings=[])])
    return summarize_timeout_and_cancellation(timeout_runs, leaks)

def _process_regressions() -> Any:
    baseline = ConcurrencyBaselineRecord(baseline_id="base1", metrics={"races": 0, "drift_ms": 10})
    current = ConcurrencyComparisonRecord(comparison_id="curr1", metrics={"races": 1, "drift_ms": 15})
    regressions = detect_concurrency_regressions(baseline, current)
    return summarize_concurrency_regressions(regressions)

def run_concurrency_hardening_pass(strategy_name: str = "ConservativeConcurrencyHardeningStrategy") -> Dict[str, Any]:
    """Runs a full concurrency hardening pass simulating all checks."""

    manifests = {
        "guards": _process_guards(),
        "parallelism": _process_parallelism(),
        "ordering": _process_ordering(),
        "race_probes": _process_race_probes(),
        "shared_state": _process_shared_state(),
        "idempotency": _process_idempotency(),
        "stale_reads": _process_stale_reads(),
        "queues": _process_queues(),
        "timeouts": _process_timeouts(),
        "regressions": _process_regressions()
    }

    health_report = build_overall_health_report(manifests)

    return {
        "manifests": {k: v.model_dump() for k, v in manifests.items()},
        "overall_health": health_report["overall_health"]
    }
