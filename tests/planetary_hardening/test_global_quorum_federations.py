import pytest
from src.sports_signal_bot.planetary_hardening.quorum_federations import (
    build_global_quorum_federation,
    verify_global_quorum_federation,
    compute_quorum_federation_agreement
)
from src.sports_signal_bot.planetary_hardening.contracts import FederatedQuorumNodeRecord

def test_build_global_quorum_federation():
    fed = build_global_quorum_federation("test_fed", [FederatedQuorumNodeRecord(node_id="n1")])
    assert fed.federation_family == "test_fed"
    assert len(fed.member_quorum_refs) == 1

def test_verify_global_quorum_federation_fresh():
    fed = build_global_quorum_federation("test_fed", [FederatedQuorumNodeRecord(node_id="n1", is_stale=False)])
    fed = verify_global_quorum_federation(fed)
    assert fed.federation_status == "federation_verified"

def test_verify_global_quorum_federation_stale():
    fed = build_global_quorum_federation("test_fed", [FederatedQuorumNodeRecord(node_id="n1", is_stale=True)])
    fed = verify_global_quorum_federation(fed, cap_on_stale=True)
    assert fed.federation_status == "federation_caveated"

def test_compute_quorum_federation_agreement():
    fed = build_global_quorum_federation("test_fed", [FederatedQuorumNodeRecord(node_id="n1", is_stale=False)])
    fed = compute_quorum_federation_agreement(fed)
    assert fed.agreement_refs[0].agreement_band == "stable_agreement"
