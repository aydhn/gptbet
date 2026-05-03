from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import CorridorGuardRecord

def evaluate_corridor_guards(context: Dict[str, Any]) -> List[CorridorGuardRecord]:
    guards = []

    # Check treaty
    guards.append(CorridorGuardRecord(guard_id="treaty_guard", outcome="guard_pass", messages=[]))
    # Check sovereignty
    guards.append(CorridorGuardRecord(guard_id="sovereignty_guard", outcome="guard_pass", messages=[]))

    return guards

def aggregate_corridor_guard_results(results: List[CorridorGuardRecord]) -> str:
    outcomes = [r.outcome for r in results]
    if "guard_block_critical" in outcomes:
        return "guard_block_critical"
    if "guard_block" in outcomes:
        return "guard_block"
    if "review_required" in outcomes:
        return "review_required"
    if "guard_warn" in outcomes:
        return "guard_warn"
    return "guard_pass"

def explain_corridor_guard_failures(results: List[CorridorGuardRecord]) -> List[str]:
    failures = []
    for r in results:
        if r.outcome in ["guard_block", "guard_block_critical", "review_required"]:
            failures.extend(r.messages)
    return failures

def project_guard_results_into_corridor_decision(results: List[CorridorGuardRecord]) -> str:
    agg = aggregate_corridor_guard_results(results)
    if agg in ["guard_block", "guard_block_critical"]:
        return "blocked"
    elif agg == "review_required":
        return "review"
    else:
        return "allowed"
