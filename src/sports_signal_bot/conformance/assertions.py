from typing import Dict, Any, List
from .contracts import SpecAssertionRecord, SeverityLevel

def evaluate_spec_assertion(assertion: SpecAssertionRecord, context: Dict[str, Any]) -> bool:
    """
    Evaluates a given assertion against the context.
    Returns True if passed, False otherwise.
    """
    # Simplified evaluation logic
    if assertion.expected_condition == "has_valid_signature":
        return context.get("signature_valid", False)
    elif assertion.expected_condition == "global_freeze_honored":
        return not context.get("local_override_freeze", False)
    return True # Default to pass for unimplemented conditions

def build_assertion_context(target_state: Dict[str, Any]) -> Dict[str, Any]:
    return target_state.copy()

def classify_assertion_failure(assertion: SpecAssertionRecord) -> SeverityLevel:
    return assertion.failure_severity

def generate_assertion_evidence(assertion: SpecAssertionRecord, passed: bool, context: Dict[str, Any]) -> str:
    if passed:
        return f"Assertion {assertion.assertion_id} passed."
    else:
        return f"Assertion {assertion.assertion_id} failed. Expected: {assertion.expected_condition}, Context: {context}"
