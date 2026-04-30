from .contracts import ExpansionControlStateRecord
from typing import Dict, Any

def run_governance_diagnostics(state: ExpansionControlStateRecord) -> Dict[str, Any]:
    return {
        "status": state.global_status.value,
        "frozen_families": state.family_freeze_states,
        "warning_count": len(state.warnings)
    }
