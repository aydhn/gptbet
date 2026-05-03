from typing import Dict, Any

def generate_advisor_reporting_kpis() -> Dict[str, Any]:
    return {
        "advisory_recommendation_rate": 0.85,
        "pattern_match_quality_score": 0.75,
        "playbook_validation_success_rate": 0.90,
        "recovery_plan_readiness_rate": 0.80,
        "no_safe_advice_rate": 0.05,
        "pattern_memory_reuse_rate": 0.60
    }
