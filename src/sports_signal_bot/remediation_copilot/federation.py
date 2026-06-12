import uuid
from .contracts import PortablePlaybookRecord, PortablePlaybookParams


def build_portable_playbook_bundle(
    params: PortablePlaybookParams,
) -> PortablePlaybookRecord:
    return PortablePlaybookRecord(
        playbook_id=f"port_{uuid.uuid4().hex[:8]}",
        family=params.family,
        step_taxonomy=params.step_taxonomy,
        scope_constraints=params.scope_constraints,
        required_guards=params.required_guards,
        required_approvals=params.required_approvals,
        rehearsal_requirements=params.rehearsal_requirements,
        rollback_notes=params.rollback_notes,
        observability_expectations=params.observability_expectations,
        known_safe_subset_notes=params.known_safe_subset_notes,
        nonportable_step_markers=params.nonportable_step_markers,
        confidence_notes=params.confidence_notes,
    )
