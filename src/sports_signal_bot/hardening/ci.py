"""
CI Integration logic.
"""
from typing import List, Dict, Any

def evaluate_release_blockers(safety_summary: Dict[str, Any], flakiness_summary: Dict[str, Any]) -> List[str]:
    blockers = []
    if safety_summary.get("critical_violations", 0) > 0:
        blockers.append("critical_safety_violations")
    if flakiness_summary.get("status") == "flaky":
         blockers.append("flaky_critical_path")
    return blockers
