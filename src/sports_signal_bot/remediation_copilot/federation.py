import uuid
from typing import List
from .contracts import PortablePlaybookRecord

def build_portable_playbook_bundle(
    family: str,
    step_taxonomy: List[str],
    scope_constraints: List[str],
    required_guards: List[str],
    required_approvals: List[str],
    rehearsal_requirements: List[str],
    rollback_notes: str,
    observability_expectations: List[str],
    known_safe_subset_notes: str,
    nonportable_step_markers: List[str],
    confidence_notes: str
) -> PortablePlaybookRecord:
    return PortablePlaybookRecord(
        playbook_id=f"port_{uuid.uuid4().hex[:8]}",
        family=family,
        step_taxonomy=step_taxonomy,
        scope_constraints=scope_constraints,
        required_guards=required_guards,
        required_approvals=required_approvals,
        rehearsal_requirements=rehearsal_requirements,
        rollback_notes=rollback_notes,
        observability_expectations=observability_expectations,
        known_safe_subset_notes=known_safe_subset_notes,
        nonportable_step_markers=nonportable_step_markers,
        confidence_notes=confidence_notes
    )
