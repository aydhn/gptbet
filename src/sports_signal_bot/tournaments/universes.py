from typing import List, Dict, Any, Tuple
from .contracts import TournamentUniverseRecord, TournamentCandidateRecord, TournamentWarningRecord
from ..simulation.contracts import ComparisonUniverseRecord, SimulationRunRecord

def build_tournament_universe(
    run_records: List[SimulationRunRecord],
    gate_profile: str = "default"
) -> Tuple[TournamentUniverseRecord, List[TournamentWarningRecord]]:
    """Builds a comparison universe from simulation run records."""
    if not run_records:
        raise ValueError("Cannot build universe from empty run records.")

    warnings = []

    first_run = run_records[0]
    if not first_run.comparison:
        raise ValueError("Simulation run missing comparison record.")

    universe_id = f"univ_base_{first_run.comparison.comparison_id}"
    base_target_sports = ["football"] # placeholder
    base_target_markets = ["O/U"] # placeholder

    universe = TournamentUniverseRecord(
        universe_id=universe_id,
        replay_window={"start": first_run.started_at, "end": first_run.completed_at or first_run.started_at},
        target_sports=base_target_sports,
        target_markets=base_target_markets,
        baseline_snapshot_id=first_run.comparison.baseline_snapshot_id,
        release_channel_base="main",
        gate_requirements_profile=gate_profile
    )

    for run in run_records[1:]:
        if not run.comparison:
            continue
        if run.comparison.baseline_snapshot_id != universe.baseline_snapshot_id:
            warnings.append(TournamentWarningRecord(
                warning_id="univ_mismatch",
                message=f"Run {run.run_id} uses different baseline snapshot.",
                severity="high"
            ))

    return universe, warnings

def validate_candidate_comparability(
    candidates: List[TournamentCandidateRecord],
    universe: TournamentUniverseRecord
) -> Tuple[bool, List[TournamentWarningRecord]]:
    """Validates if candidates are comparable within the given universe."""
    warnings = []

    if not candidates:
        return True, warnings

    target_family = candidates[0].target_component_family

    for candidate in candidates:
        if candidate.target_component_family != target_family:
            warnings.append(TournamentWarningRecord(
                warning_id="incomparable_target_family",
                message=f"Candidate {candidate.candidate_id} targets {candidate.target_component_family}, expected {target_family}",
                severity="critical"
            ))

    is_comparable = len([w for w in warnings if w.severity == "critical"]) == 0
    return is_comparable, warnings

def ensure_same_universe_for_batch(
    candidates: List[TournamentCandidateRecord],
    universe: TournamentUniverseRecord
) -> Tuple[List[TournamentCandidateRecord], List[TournamentCandidateRecord]]:
    """Splits candidates into comparable and incomparable lists."""
    comparable = []
    incomparable = []

    for candidate in candidates:
        is_comparable, _ = validate_candidate_comparability([candidates[0], candidate], universe)
        if is_comparable:
            comparable.append(candidate)
        else:
            incomparable.append(candidate)

    return comparable, incomparable

def detect_unfair_candidate_mix(candidates: List[TournamentCandidateRecord]) -> bool:
    if not candidates:
        return False
    target = candidates[0].target_component_family
    return any(c.target_component_family != target for c in candidates)

def summarize_tournament_scope(universe: TournamentUniverseRecord) -> str:
    return f"Universe {universe.universe_id}: {universe.target_sports} / {universe.target_markets}"
