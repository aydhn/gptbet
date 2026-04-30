from typing import Dict, Any, List

def analyze_handoff_failure(context: Dict[str, Any]) -> List[str]:
    reasons = []
    if context.get("readiness_score", 0) < 0.7:
        reasons.append("Readiness score below minimum threshold.")
    if not context.get("approvals_complete", False):
        reasons.append("Missing required governance approvals.")
    return reasons
