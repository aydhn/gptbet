import pytest
from sports_signal_bot.resilience_synthesis.compiler_federations import (
    build_health_compiler_federation,
    add_compiler_federation_link,
    validate_compiler_federation_link,
    compute_federated_compiler_currentness,
    summarize_compiler_federation_health
)
from sports_signal_bot.resilience_synthesis.contracts import FederatedCompilerNodeRecord, CompilerFederationCurrentnessRecord

def test_build_health_compiler_federation():
    fed = build_health_compiler_federation("f1", "review_only_health_federation")
    assert fed.compiler_federation_id == "f1"
    assert fed.federation_family == "review_only_health_federation"

def test_add_compiler_federation_link():
    fed = build_health_compiler_federation("f1", "review_only_health_federation")
    link = add_compiler_federation_link(fed, "n1", "n2")
    assert link.source_node_ref == "n1"
    assert link.target_node_ref == "n2"
    assert len(fed.federation_link_refs) == 1

def test_validate_compiler_federation_link():
    fed = build_health_compiler_federation("f1", "review_only_health_federation")
    link = add_compiler_federation_link(fed, "n1", "n2", status="link_blocked")
    assert not validate_compiler_federation_link(link)

    link2 = add_compiler_federation_link(fed, "n1", "n3", status="link_current")
    assert validate_compiler_federation_link(link2)

def test_compute_federated_compiler_currentness():
    n1 = FederatedCompilerNodeRecord(node_id="1", compiler_ref="c1", compiler_family="f1", currentness_state=CompilerFederationCurrentnessRecord(currentness_id="c1", evaluated_at="now", staleness_level="stale"), replay_state="", debt_state="", node_status="active")
    n2 = FederatedCompilerNodeRecord(node_id="2", compiler_ref="c2", compiler_family="f1", currentness_state=CompilerFederationCurrentnessRecord(currentness_id="c2", evaluated_at="now", staleness_level="fresh"), replay_state="", debt_state="", node_status="active")
    assert compute_federated_compiler_currentness([n1, n2]) == "stale"
