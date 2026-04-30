from typing import Dict, Any
from .contracts import ExpansionGovernanceManifest

def build_governance_evidence_bundle(manifest: ExpansionGovernanceManifest) -> Dict[str, Any]:
    """Builds a structured evidence bundle explaining the control tower's decisions."""
    decision = manifest.council_decision

    return {
        "evidence_type": "global_governance_decision",
        "decision": decision.decision.value,
        "rationale": decision.rationale,
        "lens_evaluations": decision.lens_evaluations,
        "control_tower_summary": manifest.control_tower_summary.model_dump(mode='json'),
        "timestamp": manifest.generated_at.isoformat()
    }
