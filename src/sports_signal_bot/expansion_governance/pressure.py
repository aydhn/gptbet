from typing import List, Dict, Any
import uuid
from datetime import datetime
from .contracts import ExpansionPressureRecord, PressureBand

def compute_global_pressure(
    active_cohort_count: int,
    simultaneously_growing_cohort_count: int,
    family_conflict_burden: float,
    verification_warning_density: float,
    review_backlog_pressure: float,
    dispute_burden: float,
    rollback_recentness_penalty: float,
    budget_saturation: float
) -> ExpansionPressureRecord:
    """Computes a global pressure score based on various burden metrics."""

    # Weighting scheme for drivers
    drivers = {
        "active_cohorts": min(active_cohort_count * 0.05, 0.20),
        "growing_cohorts": min(simultaneously_growing_cohort_count * 0.10, 0.30),
        "family_conflict": family_conflict_burden * 0.15,
        "verification_density": verification_warning_density * 0.20,
        "review_backlog": review_backlog_pressure * 0.10,
        "dispute_burden": dispute_burden * 0.15,
        "rollback_penalty": rollback_recentness_penalty * 0.25,
        "budget_saturation": budget_saturation * 0.20
    }

    total_score = sum(drivers.values())

    # Cap total score at 1.0 for classification
    normalized_score = min(total_score, 1.0)
    band = classify_pressure_band(normalized_score)

    return ExpansionPressureRecord(
        pressure_id=f"pres_{uuid.uuid4().hex[:8]}",
        pressure_score=normalized_score,
        pressure_band=band,
        drivers=drivers
    )

def compute_family_pressure(family_name: str, cohort_count: int, warning_density: float, dispute_burden: float) -> float:
    """Computes a localized pressure score for a specific family."""
    score = (cohort_count * 0.1) + (warning_density * 0.4) + (dispute_burden * 0.5)
    return min(score, 1.0)

def classify_pressure_band(score: float) -> PressureBand:
    """Classifies a normalized pressure score (0.0 to 1.0) into a qualitative band."""
    if score >= 0.85:
        return PressureBand.CRITICAL
    elif score >= 0.70:
        return PressureBand.SEVERE
    elif score >= 0.50:
        return PressureBand.HIGH
    elif score >= 0.30:
        return PressureBand.MODERATE
    else:
        return PressureBand.LOW

def explain_pressure_drivers(record: ExpansionPressureRecord) -> List[str]:
    """Generates human-readable explanations of the primary drivers of pressure."""
    explanations = []

    # Sort drivers by contribution
    sorted_drivers = sorted(record.drivers.items(), key=lambda x: x[1], reverse=True)

    for driver_name, contribution in sorted_drivers:
        if contribution > 0.15:
             explanations.append(f"Major contributor: {driver_name} (+{contribution:.2f})")
        elif contribution > 0.05:
             explanations.append(f"Moderate contributor: {driver_name} (+{contribution:.2f})")

    if not explanations:
        explanations.append("Pressure is well distributed and overall low.")

    return explanations
