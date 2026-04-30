from datetime import datetime
from typing import Dict, Any, List
from .contracts import (
    AdoptionCohortRecord, CohortStatus, ActivationLevel,
    CohortMembershipRecord, CohortScopeRecord, CohortActivationRecord,
    CohortHealthRecord, CohortSummaryRecord
)

def create_adoption_cohort(
    cohort_id: str,
    adoption_id: str,
    cohort_family: str,
    scope: Dict[str, Any],
    target_component_family: str
) -> AdoptionCohortRecord:
    return AdoptionCohortRecord(
        cohort_id=cohort_id,
        adoption_id=adoption_id,
        cohort_family=cohort_family,
        scope=scope,
        target_component_family=target_component_family
    )

def assign_member_to_cohort(
    cohort_id: str,
    member_id: str,
    member_type: str
) -> CohortMembershipRecord:
    return CohortMembershipRecord(
        cohort_id=cohort_id,
        member_id=member_id,
        member_type=member_type
    )

def define_cohort_scope(cohort_id: str, scope_definition: Dict[str, Any]) -> CohortScopeRecord:
    return CohortScopeRecord(
        cohort_id=cohort_id,
        scope_definition=scope_definition
    )

def activate_cohort(cohort_id: str, level: ActivationLevel) -> CohortActivationRecord:
    return CohortActivationRecord(
        cohort_id=cohort_id,
        activation_level=level
    )

def record_cohort_health(cohort_id: str, health_score: float, issues: List[str]) -> CohortHealthRecord:
    return CohortHealthRecord(
        cohort_id=cohort_id,
        health_score=health_score,
        health_issues=issues
    )

def summarize_cohort(cohort: AdoptionCohortRecord, health_score: float) -> CohortSummaryRecord:
    return CohortSummaryRecord(
        cohort_id=cohort.cohort_id,
        current_level=cohort.activation_level,
        status=cohort.current_status,
        health_score=health_score
    )
