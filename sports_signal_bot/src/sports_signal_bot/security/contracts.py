from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SecretDefinitionRecord(BaseModel):
    secret_name: str
    secret_family: str
    required: bool = False
    default_allowed: bool = False
    resolution_order: List[str] = ["env", "dotenv"]
    redaction_policy: str = "full_mask"
    consumer_components: List[str] = []
    severity_if_missing: str = "error"
    allowed_sources: List[str] = ["env", "dotenv"]
    rotation_hint: Optional[str] = None
    warnings: List[str] = []

class SecretResolutionRecord(BaseModel):
    secret_name: str
    resolved_source: str
    resolved_value: Optional[str] = None
    is_placeholder: bool = False
    error: Optional[str] = None

class SensitiveFieldRecord(BaseModel):
    field_path: str
    family: str
    sensitivity_class: str
    allowed_in_plaintext: bool = False
    redaction_rule: str = "full_mask"
    audit_storage_policy: str = "mask"
    preview_policy: str = "mask"
    cli_visibility_policy: str = "mask"

class PrivilegeProfileRecord(BaseModel):
    profile_name: str
    allowed_network_domains: List[str] = []
    allowed_write_roots: List[str] = []
    allowed_command_families: List[str] = []
    secret_requirements: List[str] = []
    approval_requirements: List[str] = []

class SecurityManifest(BaseModel):
    run_id: str
    security_profile: str
    missing_secrets: List[str] = []
    unsafe_configs: List[str] = []
    redaction_violations: int = 0
    privilege_violations: int = 0
    path_audit_issues: int = 0
    endpoint_audit_issues: int = 0
    risky_command_gate_issues: int = 0
    dry_run_forced_decisions: int = 0
