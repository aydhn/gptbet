from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SpecFamily(str, Enum):
    POLICY_SPEC = "policy_spec"
    INTEGRITY_SPEC = "integrity_spec"
    TRANSPARENCY_SPEC = "transparency_spec"
    WITNESS_SPEC = "witness_spec"
    PUBLICATION_SPEC = "publication_spec"
    PORTAL_SPEC = "portal_spec"
    CHALLENGE_INTAKE_SPEC = "challenge_intake_spec"
    FEDERATED_GOVERNANCE_SPEC = "federated_governance_spec"
    ADOPTION_ACTIVATION_SPEC = "adoption_activation_spec"
    EXCHANGE_NOTARIZATION_SPEC = "exchange_notarization_spec"


class AssertionType(str, Enum):
    STRUCTURE_ASSERTION = "structure_assertion"
    PRECEDENCE_ASSERTION = "precedence_assertion"
    COVERAGE_ASSERTION = "coverage_assertion"
    LIFECYCLE_ASSERTION = "lifecycle_assertion"
    INTEGRITY_ASSERTION = "integrity_assertion"
    REDACTION_ASSERTION = "redaction_assertion"
    FRESHNESS_ASSERTION = "freshness_assertion"
    TRUST_ASSERTION = "trust_assertion"
    QUORUM_ASSERTION = "quorum_assertion"
    PUBLICATION_ASSERTION = "publication_assertion"
    COMPATIBILITY_ASSERTION = "compatibility_assertion"
    DRIFT_ASSERTION = "drift_assertion"
    GATING_ASSERTION = "gating_assertion"


class RunMode(str, Enum):
    PRE_MERGE = "pre_merge"
    PRE_PROMOTION = "pre_promotion"
    PRE_ACTIVATION = "pre_activation"
    POST_ACTIVATION = "post_activation"
    NIGHTLY_AUDIT = "nightly_audit"
    RELEASE_READINESS = "release_readiness"
    EXTERNAL_PUBLICATION_CHECK = "external_publication_check"
    EMERGENCY_OVERRIDE_CHECK = "emergency_override_check"


class GateOutcome(str, Enum):
    PASS = "pass"
    PASS_WITH_WARNINGS = "pass_with_warnings"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    BLOCKED_CRITICAL = "blocked_critical"
    EXEMPTED_WITH_RECORD = "exempted_with_record"


class DriftOutcome(str, Enum):
    NO_DRIFT = "no_drift"
    TOLERATED_DRIFT = "tolerated_drift"
    WARNING_DRIFT = "warning_drift"
    BLOCKING_DRIFT = "blocking_drift"
    CRITICAL_DRIFT = "critical_drift"


class SpecAssertionRecord(BaseModel):
    assertion_id: str
    assertion_family: AssertionType
    description: str
    target_family: str
    assertion_type: str
    expected_condition: str
    failure_severity: SeverityLevel
    remediation_hint_family: str
    warnings: List[str] = Field(default_factory=list)


class GovernanceSpecRecord(BaseModel):
    spec_id: str
    spec_family: SpecFamily
    spec_name: str
    scope: str
    version: str
    status: str
    assertion_refs: List[str]
    severity_model: str
    owner_family: str
    warnings: List[str] = Field(default_factory=list)


class ConformanceSuiteRecord(BaseModel):
    suite_id: str
    suite_family: str
    suite_name: str
    included_specs: List[str]
    target_components: List[str]
    run_mode: RunMode
    gate_binding: str
    created_at: str
    warnings: List[str] = Field(default_factory=list)


class ConformanceCaseRecord(BaseModel):
    case_id: str
    suite_id: str
    spec_id: str
    assertion_id: str


class ConformanceResultRecord(BaseModel):
    case_id: str
    passed: bool
    details: str
    severity: Optional[SeverityLevel] = None


class ComplianceGateRecord(BaseModel):
    gate_id: str
    gate_family: str
    outcome: GateOutcome
    reason: str


class LintFindingRecord(BaseModel):
    finding_id: str
    lint_family: str
    severity: SeverityLevel
    description: str
    target: str


class PolicyLintRecord(BaseModel):
    lint_id: str
    findings: List[LintFindingRecord]
    passed: bool


class DriftDimensionRecord(BaseModel):
    dimension_id: str
    name: str


class DriftEvidenceRecord(BaseModel):
    baseline_ref: str
    current_ref: str
    diff_summary: str
    scope: str
    severity: SeverityLevel
    affected_gates: List[str]
    remediation_hint: str
    proof_refs: List[str] = Field(default_factory=list)


class DriftAttestationRecord(BaseModel):
    attestation_id: str
    dimension_id: str
    outcome: DriftOutcome
    evidence: DriftEvidenceRecord


class ExceptionRequestInputRecord(BaseModel):
    request_ref: str
    scope_desc: str
    expiry: str
    rationale: str
    owner: str


class ExceptionScopeRecord(BaseModel):
    scope_id: str
    description: str


class ExceptionExpiryRecord(BaseModel):
    expiry_time: str


class ExceptionApprovalRecord(BaseModel):
    approver_ref: str
    approval_time: str


class ComplianceExceptionRecord(BaseModel):
    exception_id: str
    request_ref: str
    scope: ExceptionScopeRecord
    expiry: ExceptionExpiryRecord
    rationale: str
    owner: str
    approval: ExceptionApprovalRecord
    affected_assertions: List[str]


class VerificationStageRecord(BaseModel):
    stage_name: str
    status: str
    details: str


class VerificationPipelineRunRecord(BaseModel):
    run_id: str
    run_mode: RunMode
    stages: List[VerificationStageRecord]
    final_outcome: GateOutcome


class ComplianceDecisionRecord(BaseModel):
    decision_id: str
    run_id: str
    outcome: GateOutcome
    rationale: str


class ComplianceManifest(BaseModel):
    manifest_id: str
    run_id: str
    decision: ComplianceDecisionRecord


class ComplianceSummaryRecord(BaseModel):
    summary_id: str
    run_id: str
    spec_count: int
    suite_pass_count: int
    suite_fail_count: int
    lint_findings_by_severity: Dict[str, int]
    drift_counts_by_severity: Dict[str, int]
    gate_outcomes: Dict[str, int]


class RemediationHintRecord(BaseModel):
    hint_id: str
    description: str
    target_action: str


class VerificationExceptionRecord(BaseModel):
    exception_id: str
    details: str


class ComplianceWarningRecord(BaseModel):
    warning_id: str
    message: str


class ContinuousVerificationAuditRecord(BaseModel):
    audit_id: str
    run_id: str
    timestamp: str


class GateEvaluationInput(BaseModel):
    gate_id: str
    gate_family: str
    conformance_results: List[ConformanceResultRecord]
    lint_record: Optional[PolicyLintRecord] = None
    drift_records: List[DriftAttestationRecord] = Field(default_factory=list)
