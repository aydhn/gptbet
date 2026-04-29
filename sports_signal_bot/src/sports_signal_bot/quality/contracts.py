from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class QualityContractBase(BaseModel):
    pass

class TestCaseRecord(QualityContractBase):
    test_id: str
    test_name: str
    test_layer: str
    component_family: str
    priority: str = "medium"
    deterministic: bool = True
    requires_fixture: bool = False
    expected_runtime_class: str = "fast"
    tags: List[str] = Field(default_factory=list)
    related_contracts: List[str] = Field(default_factory=list)
    enabled: bool = True

class TestSuiteRecord(QualityContractBase):
    suite_id: str
    suite_name: str
    tests: List[str] = Field(default_factory=list)
    description: str = ""

class GoldenDatasetRecord(QualityContractBase):
    dataset_id: str
    version: str
    description: str = ""
    records: List[Dict[str, Any]] = Field(default_factory=list)

class GoldenOutputRecord(QualityContractBase):
    output_id: str
    version: str
    timestamp: str
    data: Any

class ScenarioSpecRecord(QualityContractBase):
    scenario_id: str
    name: str
    description: str
    steps: List[str] = Field(default_factory=list)

class GatePolicyRecord(QualityContractBase):
    policy_id: str
    description: str = ""
    blocking: bool = True
    required_suites: List[str] = Field(default_factory=list)
    timeout_seconds: int = 300
    fail_fast: bool = False

class QualityGateRecord(QualityContractBase):
    gate_id: str
    name: str
    policies: List[GatePolicyRecord] = Field(default_factory=list)

class TestFailureRecord(QualityContractBase):
    test_id: str
    error_message: str
    stack_trace: Optional[str] = None
    flaky_suspicion: bool = False

class TestRunManifest(QualityContractBase):
    run_id: str
    timestamp: str
    gate_id: Optional[str] = None
    suite_ids: List[str] = Field(default_factory=list)
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    failures: List[TestFailureRecord] = Field(default_factory=list)

class RegressionCaseRecord(TestCaseRecord):
    bug_reference: Optional[str] = None
    historical_failure_date: Optional[str] = None

class SmokeSuiteRecord(TestSuiteRecord):
    max_runtime_seconds: int = 60

class ContractTestRecord(TestCaseRecord):
    schema_reference: str

class ScenarioAssertionRecord(QualityContractBase):
    assertion_id: str
    scenario_id: str
    description: str
    passed: bool
    details: Optional[Dict[str, Any]] = None

class GateResultRecord(QualityContractBase):
    gate_id: str
    run_id: str
    timestamp: str
    passed: bool
    blocking_failures: int = 0
    non_blocking_warnings: int = 0

class GateExecutionRecord(QualityContractBase):
    execution_id: str
    gate_id: str
    start_time: str
    end_time: Optional[str] = None
    status: str = "running"
    result: Optional[GateResultRecord] = None
