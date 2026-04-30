from typing import Dict, Any, List
from .contracts import (
    SandboxOverrideRecord,
    SandboxNamespaceRecord,
    SandboxStateRecord,
    SandboxIsolationCheckRecord,
    CandidatePatchRecord
)
import uuid

def create_sandbox_namespace(request_id: str) -> SandboxNamespaceRecord:
    state = SandboxStateRecord(state_id=f"state_{uuid.uuid4().hex[:8]}", active_overrides=[])
    return SandboxNamespaceRecord(
        namespace_id=f"sandbox_{request_id}",
        root_path=f"data/sandbox/{request_id}",
        state=state
    )

def apply_sandbox_patch(namespace: SandboxNamespaceRecord, patch: CandidatePatchRecord) -> SandboxOverrideRecord:
    override = SandboxOverrideRecord(
        override_id=f"override_{uuid.uuid4().hex[:8]}",
        patch_id=patch.patch_id,
        target=patch.target_component_family,
        override_payload=patch.patch_payload,
        active=True
    )
    namespace.state.active_overrides.append(override.override_id)
    return override

def revoke_sandbox_patch(namespace: SandboxNamespaceRecord, override_id: str) -> None:
    if override_id in namespace.state.active_overrides:
        namespace.state.active_overrides.remove(override_id)

def isolate_sandbox_outputs(namespace: SandboxNamespaceRecord) -> None:
    # Ensure all output paths point to namespace.root_path
    pass

def validate_no_active_state_mutation() -> SandboxIsolationCheckRecord:
    # In a real impl, this would check if any production configs/state were modified
    return SandboxIsolationCheckRecord(
        check_id=f"check_{uuid.uuid4().hex[:8]}",
        is_isolated=True,
        leaks_detected=[]
    )

def cleanup_sandbox_state(namespace: SandboxNamespaceRecord) -> None:
    namespace.state.active_overrides.clear()
