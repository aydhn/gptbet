"""
Replay parity logic.
"""
from typing import Dict, Any, List
from .contracts import ReplayParityRunRecord

def run_replay_parity(fixture_id: str, expected_output: Dict[str, Any], actual_output: Dict[str, Any]) -> ReplayParityRunRecord:
    status = "matched"
    if expected_output != actual_output:
        status = "mismatched"
    return ReplayParityRunRecord(
        replay_run_id=f"replay_{fixture_id}",
        fixture_ref=fixture_id,
        parity_status=status
    )

def compare_replay_structures(struct1: Dict[str, Any], struct2: Dict[str, Any]) -> str:
    return "matched" if struct1 == struct2 else "mismatched"

def classify_replay_mismatch(mismatch_details: str) -> str:
    return "unexplained" if "unexplained" in mismatch_details else "explained"

def summarize_replay_parity(runs: List[ReplayParityRunRecord]) -> Dict[str, Any]:
    matched = sum(1 for r in runs if r.parity_status == "matched")
    mismatched = sum(1 for r in runs if r.parity_status == "mismatched")
    return {
        "total_runs": len(runs),
        "matched": matched,
        "mismatched": mismatched
    }
