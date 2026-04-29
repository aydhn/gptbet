from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class CompatibilityResultStatus(str, Enum):
    FULLY_COMPATIBLE = "fully_compatible"
    BACKWARD_COMPATIBLE = "backward_compatible"
    FORWARD_COMPATIBLE_WITH_WARNINGS = "forward_compatible_with_warnings"
    MIGRATION_REQUIRED = "migration_required"
    INCOMPATIBLE_BREAKING = "incompatible_breaking"
    UNKNOWN_VERSION = "unknown_version"

class BreakingChangeType(str, Enum):
    REMOVED_REQUIRED_FIELD = "removed_required_field"
    RENAMED_WITHOUT_ALIAS = "renamed_without_alias"
    INCOMPATIBLE_TYPE_CHANGE = "incompatible_type_change"
    CHANGED_ENUM_MEANING = "changed_enum_meaning"
    CHANGED_PROBABILITY_ORDER_SEMANTICS = "changed_probability_order_semantics"
    CHANGED_SCALE_SEMANTICS = "changed_scale_semantics"
    REMOVED_SUPPORTED_STATUS = "removed_supported_status"
    MANIFEST_ENVELOPE_MISSING = "manifest_envelope_missing"
    CONTRACT_FAMILY_MISMATCH = "contract_family_mismatch"

class CompatibilityWarningRecord(BaseModel):
    field: str
    message: str

class CompatibilityResultRecord(BaseModel):
    status: CompatibilityResultStatus
    breaking_changes: List[BreakingChangeType] = Field(default_factory=list)
    warnings: List[CompatibilityWarningRecord] = Field(default_factory=list)
    is_compatible: bool

def check_backward_compatibility(old_def, new_def) -> CompatibilityResultRecord:
    # Basic implementation
    return CompatibilityResultRecord(status=CompatibilityResultStatus.FULLY_COMPATIBLE, is_compatible=True)

def check_forward_compatibility(old_def, new_def) -> CompatibilityResultRecord:
    # Basic implementation
    return CompatibilityResultRecord(status=CompatibilityResultStatus.FULLY_COMPATIBLE, is_compatible=True)

def classify_breaking_change(old_def, new_def) -> List[BreakingChangeType]:
    return []

def summarize_compatibility_risks(result: CompatibilityResultRecord) -> str:
    return f"Status: {result.status.value}, Warnings: {len(result.warnings)}"

def explain_compatibility_result(result: CompatibilityResultRecord) -> str:
    return f"Compatibility result is {result.status.value}."
