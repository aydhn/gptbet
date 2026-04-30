from typing import Dict, Any, List
from .contracts import CandidatePatchRecord, PatchType, RiskLevel
import uuid

def build_candidate_patch(suggestion: Dict[str, Any]) -> CandidatePatchRecord:
    # Dummy logic to convert a suggestion dictionary into a CandidatePatchRecord
    risk_mapping = {
        "provider_priority": RiskLevel.HIGH,
        "reconciliation_conflict": RiskLevel.HIGH,
        "alias_memory": RiskLevel.LOW,
        "threshold_band": RiskLevel.MEDIUM,
        "no_bet_policy": RiskLevel.MEDIUM,
        "source_penalty": RiskLevel.MEDIUM,
        "dynamic_weighting": RiskLevel.HIGH,
        "monitoring_threshold": RiskLevel.LOW
    }
    family = suggestion.get("target_component_family", "unknown")
    risk_level = risk_mapping.get(family, RiskLevel.MEDIUM)

    return CandidatePatchRecord(
        patch_id=f"patch_{uuid.uuid4().hex[:8]}",
        suggestion_id=suggestion.get("suggestion_id", "sug_0"),
        target_component_family=family,
        target_config_family=suggestion.get("target_config_family", "unknown"),
        patch_type=PatchType(suggestion.get("patch_type", PatchType.CONFIG_VALUE_OVERRIDE.value)),
        patch_payload=suggestion.get("patch_payload", {}),
        scope=suggestion.get("scope", {}),
        sandbox_only=True,
        expiry_policy="transient",
        risk_level=risk_level,
        supporting_evidence_refs=suggestion.get("supporting_evidence_refs", []),
        warnings=[]
    )

def validate_patch_scope(patch: CandidatePatchRecord) -> bool:
    if not patch.scope:
        return False
    # Check bounds or specific keys
    return True

def render_patch_diff(patch: CandidatePatchRecord) -> str:
    return f"--- Before\n+++ After\n+{patch.patch_payload}"

def narrow_patch_scope(patch: CandidatePatchRecord, constraint: Dict[str, Any]) -> CandidatePatchRecord:
    patch.scope.update(constraint)
    return patch
