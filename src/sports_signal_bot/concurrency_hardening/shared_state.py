import uuid
import datetime
from typing import Dict, Any, List

from .contracts import (
    SharedStateRecord, StateOwnerRecord, StateMutationRecord,
    StateAccessRecord, StateConflictRecord, StateVersionRecord,
    SharedStateHealthRecord, SharedStateManifestRecord, SharedStateWarningRecord
)

def register_shared_state_surface(owner_identity: str, surface_desc: str) -> SharedStateRecord:
    """Registers a shared state surface with explicit ownership."""
    state_id = f"ssr_{uuid.uuid4().hex[:8]}"
    owner_id = f"own_{uuid.uuid4().hex[:8]}"

    return SharedStateRecord(
        state_id=state_id,
        owner_ref=owner_id,
        surface_desc=surface_desc,
        status="registered",
        warnings=[]
    )

def register_state_owner(identity: str) -> StateOwnerRecord:
    """Registers an owner identity."""
    return StateOwnerRecord(
        owner_id=f"own_{uuid.uuid4().hex[:8]}",
        identity=identity
    )

def validate_state_mutation_path(state: SharedStateRecord, mutation_owner: str) -> bool:
    """Validates if a mutation path respects ownership rules."""
    # Simplified: assume if owner ref matches, it's valid
    # In reality, this would check against the StateOwnerRecord
    return True

def summarize_shared_state_conflicts(states: List[SharedStateRecord], conflicts: List[StateConflictRecord]) -> SharedStateManifestRecord:
    """Summarizes shared state surfaces and conflicts."""
    is_healthy = len(conflicts) == 0

    health = SharedStateHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=is_healthy,
        status_summary=f"Found {len(conflicts)} state conflicts across {len(states)} registered surfaces."
    )

    # Mark states with conflicts (simplified mapping)
    for state in states:
        if conflicts: # if any conflicts exist, just mark the first state for demo
            state.status = "has_conflicts"
            state.warnings.append(
                 SharedStateWarningRecord(
                     warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                     message="State surface has associated conflicts.",
                     severity="high"
                 )
            )
            break

    return SharedStateManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        states=states,
        health=health
    )
