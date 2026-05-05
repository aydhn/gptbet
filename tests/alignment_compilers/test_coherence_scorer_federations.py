import pytest
from sports_signal_bot.alignment_compilers.coherence_federations import (
    build_coherence_scorer_federation,
    add_coherence_federation_link,
    compute_federated_coherence_currentness,
    aggregate_federated_coherence_outputs,
    compute_coherence_federation_agreement
)

def test_build_coherence_federation():
    fed = build_coherence_scorer_federation("fed-1", "context_coherence_federation", "cur_pol_1", "ceil_pol_1", "agree_pol_1")
    assert fed.coherence_federation_id == "fed-1"
    assert fed.health_status == "initializing"

def test_add_federation_link():
    fed = build_coherence_scorer_federation("fed-1", "family", "pol", "pol", "pol")
    link = add_coherence_federation_link(fed, "source_1", "target_1", "link_current")
    assert link.status == "link_current"
    assert link.link_id in fed.active_link_refs

def test_compute_currentness():
    fed = build_coherence_scorer_federation("fed-1", "family", "pol", "pol", "pol")
    currentness = compute_federated_coherence_currentness(fed, {"node1": "current", "node2": "stale"})
    assert currentness.state == "stale"

def test_aggregate_outputs():
    fed = build_coherence_scorer_federation("fed-1", "family", "pol", "pol", "pol")
    band = aggregate_federated_coherence_outputs(fed, ["stale", "current"])
    assert band == "federated_coherence_stale"

    band = aggregate_federated_coherence_outputs(fed, ["current", "current"])
    assert band == "federated_coherence_current_with_caps"

def test_compute_agreement():
    agreement = compute_coherence_federation_agreement(["current", "stale"])
    assert agreement.agreement_band == "no_agreement"

    agreement = compute_coherence_federation_agreement(["stale", "stale"])
    assert agreement.agreement_band == "bounded_agreement"
