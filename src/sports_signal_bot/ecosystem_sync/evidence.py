# evidence.py - Logic to tie sync results to evidence bundles (mock)

from typing import Dict, Any

def explain_tradeoff_decision(trust_score: float, lag_seconds: int, outcome: str) -> str:
    """Provides evidence-backed explanation for a tradeoff decision."""
    return f"Chose '{outcome}' given trust={trust_score} and lag={lag_seconds}s. Justification: Policy thresholds met."
