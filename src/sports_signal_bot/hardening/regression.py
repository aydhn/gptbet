"""
Regression harness logic.
"""
from typing import Dict, Any, List
from .contracts import RegressionCaseRecord

def build_regression_harness() -> Dict[str, Any]:
    return {"status": "initialized"}

def register_regression_fixture(fixture_id: str, data: Dict[str, Any]) -> str:
    return fixture_id

def run_regression_case(case_id: str, family: str, fixture_ref: str, golden_ref: str, actual_ref: str) -> RegressionCaseRecord:
    status = "matched" if golden_ref == actual_ref else "mismatched"
    return RegressionCaseRecord(
        regression_case_id=case_id,
        case_family=family,
        fixture_ref=fixture_ref,
        expected_golden_ref=golden_ref,
        actual_output_ref=actual_ref,
        diff_ref=f"diff_{case_id}",
        tolerance_ref="default_tolerance",
        result_status=status
    )

def diff_regression_outputs(expected: Dict[str, Any], actual: Dict[str, Any]) -> Dict[str, Any]:
    return {"diff": "No difference" if expected == actual else "Difference found"}

def summarize_regression_suite(cases: List[RegressionCaseRecord]) -> Dict[str, Any]:
    matched = sum(1 for c in cases if c.result_status == "matched")
    mismatched = sum(1 for c in cases if c.result_status == "mismatched")
    return {
        "total_cases": len(cases),
        "matched": matched,
        "mismatched": mismatched
    }
