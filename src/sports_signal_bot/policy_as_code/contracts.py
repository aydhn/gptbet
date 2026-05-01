from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime

class PolicyDecisionStatus(str, Enum):
    PERMIT = "permit"
    DENY = "deny"
    HOLD = "hold"
    ESCALATE = "escalate"
    REQUIRE_REVIEW = "require_review"
    REQUIRE_APPROVAL = "require_approval"

class PolicyRuleSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    ADVISORY = "advisory"

class PolicyFailSafeMode(str, Enum):
    BLOCK_ON_ERROR = "block_on_error"
    ALLOW_ON_ERROR = "allow_on_error"
    ESCALATE_ON_ERROR = "escalate_on_error"
    ADVISE_ONLY = "advise_only"

class PolicyCompatibilityClass(str, Enum):
    COMPATIBLE = "compatible"
    COMPATIBLE_WITH_WARNINGS = "compatible_with_warnings"
    MIGRATION_REQUIRED = "migration_required"
    INCOMPATIBLE = "incompatible"

class PolicyReviewStatus(str, Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    REVIEW_APPROVED = "review_approved"
    REVIEW_REJECTED = "review_rejected"
    PROMOTION_READY = "promotion_ready"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"

class PolicyBundleRecord(BaseModel):
    policy_bundle_id: str
    bundle_name: str
    bundle_family: str
    version: str
    status: PolicyReviewStatus = PolicyReviewStatus.DRAFT
    scope: Dict[str, Any] = Field(default_factory=dict)
    parent_bundle_refs: List[str] = Field(default_factory=list)
    overlay_refs: List[str] = Field(default_factory=list)
    effective_from: Optional[datetime] = None
    immutable_hash_placeholder: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list) # IDs of rules included

class PolicyRuleRecord(BaseModel):
    rule_id: str
    rule_family: str
    title: str
    description: str
    priority: int
    enabled: bool = True
    scope: Dict[str, Any] = Field(default_factory=dict)
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    severity: PolicyRuleSeverity = PolicyRuleSeverity.MEDIUM
    fail_safe_mode: PolicyFailSafeMode = PolicyFailSafeMode.BLOCK_ON_ERROR
    review_required_for_change: bool = True
    warnings: List[str] = Field(default_factory=list)

class PolicyConditionRecord(BaseModel):
    condition_id: str
    namespace: str
    field: str
    operator: str
    value: Any

class PolicyActionRecord(BaseModel):
    action_id: str
    action_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class PolicyOverlayRecord(BaseModel):
    overlay_id: str
    base_bundle_id: str
    overlay_type: str
    scope: Dict[str, Any] = Field(default_factory=dict)
    added_rules: List[str] = Field(default_factory=list)
    removed_rules: List[str] = Field(default_factory=list)
    modified_rules: Dict[str, Any] = Field(default_factory=dict)
    expires_at: Optional[datetime] = None

class PolicyDecisionRecordV2(BaseModel):
    decision_id: str
    context_id: str
    decision_status: PolicyDecisionStatus
    blockers: List[str] = Field(default_factory=list)
    required_followups: List[str] = Field(default_factory=list)
    triggered_rules: List[str] = Field(default_factory=list)
    applied_bundle_refs: List[str] = Field(default_factory=list)
    overridden_rules: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    policy_explanation: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PolicyEvaluationRecord(BaseModel):
    evaluation_id: str
    context_data: Dict[str, Any]
    target_bundle_ids: List[str]
    decision: PolicyDecisionRecordV2
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)

class PolicyConflictRecord(BaseModel):
    conflict_id: str
    rule_ids: List[str]
    description: str
    resolution_strategy: str
    resolved_rule_id: Optional[str] = None

class PolicyPrecedenceRecord(BaseModel):
    precedence_id: str
    family_order: List[str]
    description: str

class PolicyChangeRequestRecord(BaseModel):
    request_id: str
    bundle_id: str
    proposed_changes: Dict[str, Any]
    status: str = "open"
    risk_level: str = "unknown"
    affected_scopes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PolicyDiffRecord(BaseModel):
    diff_id: str
    base_bundle_id: str
    target_bundle_id: str
    added_rules: List[str] = Field(default_factory=list)
    removed_rules: List[str] = Field(default_factory=list)
    changed_rules: Dict[str, Any] = Field(default_factory=dict)
    risk_hints: List[str] = Field(default_factory=list)
    human_readable_summary: str

class PolicyReviewRecord(BaseModel):
    review_id: str
    request_id: str
    reviewer_id: str
    checklist_results: Dict[str, bool] = Field(default_factory=dict)
    decision: str
    comments: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PolicyPromotionRecord(BaseModel):
    promotion_id: str
    bundle_id: str
    from_status: PolicyReviewStatus
    to_status: PolicyReviewStatus
    approved_by: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AppliedPolicyRecord(BaseModel):
    applied_id: str
    bundle_id: str
    bundle_hash: str
    evaluation_context_id: str
    active_overlays: List[str] = Field(default_factory=list)
    applied_at: datetime = Field(default_factory=datetime.utcnow)

class PolicyManifest(BaseModel):
    manifest_id: str
    active_bundles: List[str]
    active_overlays: List[str]
    pending_changes: int
    recent_conflicts: int
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class PolicyCompatibilityRecord(BaseModel):
    compatibility_id: str
    base_version: str
    target_version: str
    compatibility_class: PolicyCompatibilityClass
    warnings: List[str] = Field(default_factory=list)

class PolicyScopeRecordV2(BaseModel):
    scope_id: str
    dimensions: Dict[str, Any]

class PolicyWarningRecord(BaseModel):
    warning_id: str
    rule_id: str
    message: str
    severity: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PolicyAuditRecord(BaseModel):
    audit_id: str
    action: str
    target_id: str
    details: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PolicyConstraintRecord(BaseModel):
    constraint_id: str
    constraint_type: str
    parameters: Dict[str, Any]
