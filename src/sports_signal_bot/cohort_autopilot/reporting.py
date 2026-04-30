from typing import Dict, Any, List
from .contracts import CohortSummaryRecord

def generate_cohort_growth_rate(summaries: List[CohortSummaryRecord]) -> float:
    return 0.0 # Mock

def generate_pause_rate(summaries: List[CohortSummaryRecord]) -> float:
    return 0.0 # Mock

def generate_shrink_rate(summaries: List[CohortSummaryRecord]) -> float:
    return 0.0 # Mock

def generate_rollback_rate(summaries: List[CohortSummaryRecord]) -> float:
    return 0.0 # Mock

def generate_clean_verification_rate() -> float:
    return 1.0 # Mock

def generate_blocked_growth_rate() -> float:
    return 0.0 # Mock

def get_fleet_pressure_index() -> float:
    return 0.5 # Mock

def get_verification_regression_burden() -> float:
    return 0.1 # Mock
