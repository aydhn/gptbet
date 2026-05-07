import pytest
from sports_signal_bot.continuity_verification_hardening.observatory_federations import (
    build_observatory_federation,
    add_observatory_federation_link,
    verify_observatory_federation,
    compute_observatory_federation_agreement,
    summarize_observatory_federation
)
from sports_signal_bot.continuity_verification_hardening.contracts import (
    ObservatoryFederationFamily,
    ObservatoryFederationStatus,
    FederatedObservatoryNodeRecord,
    ObservatoryFederationLinkRecord
)

def test_build_observatory_federation():
    fed = build_observatory_federation("fed_test", ObservatoryFederationFamily.bounded_observatory_federation)
    assert fed.observatory_federation_id == "fed_test"
    assert fed.federation_family == ObservatoryFederationFamily.bounded_observatory_federation
    assert fed.federation_status == ObservatoryFederationStatus.federation_gapped

def test_verify_observatory_federation():
    fed = build_observatory_federation("fed_test", ObservatoryFederationFamily.bounded_observatory_federation)
    nodes = [
        FederatedObservatoryNodeRecord(node_id="node_1", node_family="scheduler_observatory_node", owner_ref="owner_1", is_stale=False),
        FederatedObservatoryNodeRecord(node_id="node_2", node_family="audit_visibility_observatory_node", owner_ref="owner_2", is_stale=True)
    ]
    verified_fed = verify_observatory_federation(fed, nodes)
    assert verified_fed.federation_status == ObservatoryFederationStatus.federation_review_only

def test_summarize_observatory_federation():
    fed = build_observatory_federation("fed_test", ObservatoryFederationFamily.bounded_observatory_federation)
    link = ObservatoryFederationLinkRecord(link_id="link_1", link_status="link_current", lag_ms=10)
    add_observatory_federation_link(fed, link)
    summary = summarize_observatory_federation(fed)
    assert summary["links"] == 1
    assert summary["status"] == ObservatoryFederationStatus.federation_gapped
