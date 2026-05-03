import uuid
from typing import List
from .contracts import PortablePlaybookRecord, PlaybookAdaptationRecord

def adapt_portable_playbook_to_local_policy(
    playbook: PortablePlaybookRecord,
    local_restrictions: List[str]
) -> PlaybookAdaptationRecord:

    outcome = "adapted_clean"
    warnings = []

    if "unsafe_semantic_widening" in local_restrictions:
        outcome = "quarantined_for_manual_mapping"
        warnings.append("Unsafe semantic widening detected.")
    elif local_restrictions:
        outcome = "adapted_with_restrictions"

    return PlaybookAdaptationRecord(
        adaptation_id=f"adapt_{uuid.uuid4().hex[:8]}",
        portable_playbook_ref=playbook.playbook_id,
        outcome=outcome,
        applied_local_restrictions=local_restrictions,
        warnings=warnings
    )
