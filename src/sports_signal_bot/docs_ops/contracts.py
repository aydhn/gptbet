import datetime
from enum import Enum
from pydantic import BaseModel, Field

class DocFamily(str, Enum):
    OVERVIEW = "overview"
    OPERATOR = "operator"
    RUNBOOK = "runbook"
    INCIDENT_PLAYBOOK = "incident_playbook"
    DEVELOPER = "developer"
    REFERENCE = "reference"
    GOVERNANCE = "governance"
    ONBOARDING = "onboarding"
    MAINTENANCE = "maintenance"

class DocStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class DocumentRecord(BaseModel):
    doc_id: str
    title: str
    doc_family: DocFamily
    path: str
    owner_role: str
    owner_component: str
    intended_audience: list[str] = Field(default_factory=list)
    status: DocStatus = DocStatus.ACTIVE
    last_updated_at: datetime.datetime | None = None
    last_reviewed_at: datetime.datetime | None = None
    freshness_window_days: int = 30
    linked_docs: list[str] = Field(default_factory=list)
    related_components: list[str] = Field(default_factory=list)
    related_cli_commands: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

class RunbookRecordV2(DocumentRecord):
    purpose: str = ""
    when_to_use: str = ""
    preconditions: list[str] = Field(default_factory=list)
    inputs_needed: list[str] = Field(default_factory=list)
    success_criteria: str = ""
    failure_branches: list[str] = Field(default_factory=list)
    escalation_path: str = ""

class PlaybookRecord(DocumentRecord):
    symptom_summary: str = ""
    severity_guidance: str = ""
    first_5_minutes: list[str] = Field(default_factory=list)
    unsafe_actions_to_avoid: list[str] = Field(default_factory=list)
    escalation_thresholds: list[str] = Field(default_factory=list)

class DocFreshnessRecord(BaseModel):
    doc_id: str
    is_stale: bool
    days_since_review: int | None
    days_overdue: int | None
    owner_role: str
    owner_component: str

class DocLintResultRecord(BaseModel):
    doc_id: str
    path: str
    issues: list[str] = Field(default_factory=list)
    passed: bool

class GlossaryTermRecord(BaseModel):
    term: str
    definition: str
    related_terms: list[str] = Field(default_factory=list)

class DecisionLogRecord(BaseModel):
    date: str
    decision_title: str
    context: str
    chosen_option: str
    rejected_alternatives: list[str] = Field(default_factory=list)
    consequences: str
    related_components: list[str] = Field(default_factory=list)

class DocCoverageRecord(BaseModel):
    component: str
    has_overview: bool
    has_runbook: bool
    has_playbook: bool
    has_operator_reference: bool
    has_cli_reference: bool
    coverage_score: float

class DocsOpsManifestRecord(BaseModel):
    total_docs_count: int
    docs_by_family: dict[str, int]
    stale_docs_count: int
    missing_coverage_components: list[str]
    total_lint_issues: int
    critical_runbooks_count: int
    incident_playbooks_count: int
    generated_at: datetime.datetime
