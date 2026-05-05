import uuid
import datetime
from typing import Dict, Any, List, Optional
import random

from .contracts import (
    RaceProbeRunRecord, RaceProbeScenarioRecord, RaceProbeScheduleRecord,
    RaceProbeSignalRecord, RaceProbeViolationRecord, RaceProbeClusterRecord,
    RaceProbeRecoveryRecord, RaceProbeHealthRecord, RaceProbeManifestRecord,
    RaceProbeWarningRecord
)

def build_race_probe_run(
    scenario_family: str,
    schedule_seed: int,
    perturbation_strategy: str
) -> RaceProbeRunRecord:
    """Initializes a race probe run."""
    run_id = f"rpr_{uuid.uuid4().hex[:8]}"
    scenario_id = f"scn_{uuid.uuid4().hex[:8]}"
    schedule_id = f"sch_{uuid.uuid4().hex[:8]}"

    warnings = []

    # Basic validation
    if scenario_family not in [
        "simultaneous_read_write_probe", "duplicate_write_probe",
        "stale_read_probe", "invalidation_race_probe",
        "async_join_reorder_probe", "timeout_cancel_probe",
        "queue_pressure_probe", "hot_path_contention_probe"
    ]:
        warnings.append(
            RaceProbeWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Unknown scenario family: {scenario_family}",
                severity="medium"
            )
        )

    return RaceProbeRunRecord(
        run_id=run_id,
        scenario_ref=scenario_id,
        schedule_ref=schedule_id,
        run_status="race_clean", # optimistic start
        violations_detected=0,
        warnings=warnings
    )

def perturb_execution_schedule(operations: List[str], seed: int, strategy: str) -> List[str]:
    """Applies a perturbation strategy to a schedule of operations."""
    random.seed(seed)
    result = list(operations)

    if strategy == "random_shuffle":
        random.shuffle(result)
    elif strategy == "reverse":
        result.reverse()
    elif strategy == "interleave":
        # Simplified interleave: just swap adjacent pairs
        for i in range(0, len(result) - 1, 2):
            result[i], result[i+1] = result[i+1], result[i]

    return result

def detect_race_signals(run: RaceProbeRunRecord, expected_state: Any, actual_state: Any) -> Optional[RaceProbeViolationRecord]:
    """Detects race conditions by comparing expected and actual states after perturbation."""
    if expected_state == actual_state:
        return None

    run.run_status = "race_detected"
    run.violations_detected += 1

    return RaceProbeViolationRecord(
        violation_id=f"viol_{uuid.uuid4().hex[:8]}",
        description=f"State mismatch after perturbation. Expected {expected_state}, got {actual_state}"
    )

def cluster_race_violations(violations: List[RaceProbeViolationRecord]) -> List[RaceProbeClusterRecord]:
    """Clusters similar violations."""
    # Simplified clustering: group all together for now
    if not violations:
        return []

    cluster_id = f"clus_{uuid.uuid4().hex[:8]}"
    return [RaceProbeClusterRecord(
        cluster_id=cluster_id,
        violations=[v.violation_id for v in violations]
    )]

def summarize_race_probes(runs: List[RaceProbeRunRecord]) -> RaceProbeManifestRecord:
    """Summarizes race probe runs."""
    detected = sum(1 for r in runs if r.run_status == "race_detected")

    health = RaceProbeHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=detected == 0,
        status_summary=f"Found {detected} runs with detected races out of {len(runs)} total."
    )

    return RaceProbeManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        runs=runs,
        health=health
    )
