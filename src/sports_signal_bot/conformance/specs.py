from typing import List, Dict, Optional
from .contracts import GovernanceSpecRecord, SpecAssertionRecord, SpecFamily, SeverityLevel, AssertionType

class GovernanceSpecRegistry:
    def __init__(self):
        self.specs: Dict[str, GovernanceSpecRecord] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        # Default spec for policy
        policy_spec = GovernanceSpecRecord(
            spec_id="spec_policy_01",
            spec_family=SpecFamily.POLICY_SPEC,
            spec_name="Core Policy Conformance",
            scope="global",
            version="1.0",
            status="active",
            assertion_refs=["assert_policy_signed", "assert_policy_precedence"],
            severity_model="strict",
            owner_family="policy_as_code"
        )
        self.register_governance_spec(policy_spec)

    def register_governance_spec(self, spec: GovernanceSpecRecord):
        self.specs[spec.spec_id] = spec

    def get_spec(self, spec_id: str) -> Optional[GovernanceSpecRecord]:
        return self.specs.get(spec_id)

    def list_specs(self) -> List[GovernanceSpecRecord]:
        return list(self.specs.values())

class AssertionRegistry:
    def __init__(self):
        self.assertions: Dict[str, SpecAssertionRecord] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        a1 = SpecAssertionRecord(
            assertion_id="assert_policy_signed",
            assertion_family=AssertionType.INTEGRITY_ASSERTION,
            description="every critical active policy bundle must have signed applied snapshot",
            target_family="policy_bundle",
            assertion_type="signature_check",
            expected_condition="has_valid_signature",
            failure_severity=SeverityLevel.CRITICAL,
            remediation_hint_family="add_missing_signature"
        )
        a2 = SpecAssertionRecord(
            assertion_id="assert_policy_precedence",
            assertion_family=AssertionType.PRECEDENCE_ASSERTION,
            description="local plane cannot override higher-plane freeze",
            target_family="policy_evaluation",
            assertion_type="precedence_check",
            expected_condition="global_freeze_honored",
            failure_severity=SeverityLevel.CRITICAL,
            remediation_hint_family="narrow_scope_overlay"
        )
        self.register_assertion(a1)
        self.register_assertion(a2)

    def register_assertion(self, assertion: SpecAssertionRecord):
        self.assertions[assertion.assertion_id] = assertion

    def get_assertion(self, assertion_id: str) -> Optional[SpecAssertionRecord]:
        return self.assertions.get(assertion_id)

    def resolve_required_assertions(self, spec_id: str, spec_registry: GovernanceSpecRegistry) -> List[SpecAssertionRecord]:
        spec = spec_registry.get_spec(spec_id)
        if not spec:
            return []
        resolved = []
        for ref in spec.assertion_refs:
            a = self.get_assertion(ref)
            if a:
                resolved.append(a)
        return resolved

def map_specs_to_components(registry: GovernanceSpecRegistry) -> Dict[str, List[GovernanceSpecRecord]]:
    mapping = {}
    for spec in registry.list_specs():
        mapping.setdefault(spec.owner_family, []).append(spec)
    return mapping

def summarize_spec_coverage(registry: GovernanceSpecRegistry) -> Dict[str, int]:
    return {
        "total_specs": len(registry.specs),
        "by_family": {f.value: len([s for s in registry.list_specs() if s.spec_family == f]) for f in SpecFamily}
    }
