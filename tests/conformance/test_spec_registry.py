import pytest
from sports_signal_bot.conformance.specs import GovernanceSpecRegistry, AssertionRegistry, map_specs_to_components, summarize_spec_coverage

def test_governance_spec_registry():
    registry = GovernanceSpecRegistry()
    assert len(registry.list_specs()) > 0
    spec = registry.get_spec("spec_policy_01")
    assert spec is not None
    assert spec.spec_family == "policy_spec"

def test_assertion_registry():
    registry = AssertionRegistry()
    assert len(registry.assertions) > 0

def test_map_and_summarize():
    reg = GovernanceSpecRegistry()
    mapping = map_specs_to_components(reg)
    assert "policy_as_code" in mapping
    summary = summarize_spec_coverage(reg)
    assert summary["total_specs"] > 0
