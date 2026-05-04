import pytest
import datetime
from sports_signal_bot.evidence_atlas.contracts import (
    NarrativeFederationCurrentnessRecord,
    FederatedNarrativeNodeRecord,
    NarrativeFederationLinkRecord,
    NarrativeFederationLinkStatus,
    NarrativeFederationOutputStatus,
    NarrativeFederationCaveatRecord
)
from sports_signal_bot.evidence_atlas.narrative_federations import (
    build_narrative_compiler_federation,
    add_narrative_federation_link,
    validate_narrative_federation_link,
    compute_federated_narrative_currentness,
    aggregate_federated_narratives,
    preserve_caveats_in_federation,
    preserve_no_safe_sections_in_federation
)

def test_build_narrative_compiler_federation():
    fed = build_narrative_compiler_federation("fed_1", "operator_narrative_federation")
    assert fed.narrative_federation_id == "fed_1"
    assert fed.federation_family == "operator_narrative_federation"
    assert fed.health_status == "initializing"

def test_validate_link():
    good_link = NarrativeFederationLinkRecord(
        link_id="l1", source_node_ref="s1", target_node_ref="t1", status=NarrativeFederationLinkStatus.link_current
    )
    bad_link = NarrativeFederationLinkRecord(
        link_id="l2", source_node_ref="s2", target_node_ref="t2", status=NarrativeFederationLinkStatus.link_blocked
    )

    assert validate_narrative_federation_link(good_link) is True
    assert validate_narrative_federation_link(bad_link) is False

def test_aggregate_federated_narratives():
    good_node = FederatedNarrativeNodeRecord(
        node_id="n1", narrative_compiler_ref="c1", narrative_family="f1",
        currentness_state=NarrativeFederationCurrentnessRecord(
            is_current=True, last_refresh=datetime.datetime.now(datetime.UTC), expires_at=datetime.datetime.now(datetime.UTC)
        ),
        sovereignty_state="ok", node_status="active"
    )

    stale_node = FederatedNarrativeNodeRecord(
        node_id="n2", narrative_compiler_ref="c2", narrative_family="f1",
        currentness_state=NarrativeFederationCurrentnessRecord(
            is_current=False, stale_sections=["sec1"], last_refresh=datetime.datetime.now(datetime.UTC), expires_at=datetime.datetime.now(datetime.UTC)
        ),
        sovereignty_state="ok", node_status="active"
    )

    caveat_node = FederatedNarrativeNodeRecord(
        node_id="n3", narrative_compiler_ref="c3", narrative_family="f1",
        currentness_state=NarrativeFederationCurrentnessRecord(
            is_current=True, last_refresh=datetime.datetime.now(datetime.UTC), expires_at=datetime.datetime.now(datetime.UTC)
        ),
        caveat_state=[NarrativeFederationCaveatRecord(caveat_id="c1", description="test")],
        sovereignty_state="ok", node_status="active"
    )

    assert aggregate_federated_narratives([good_node]) == NarrativeFederationOutputStatus.federated_narrative_current_with_caps
    assert aggregate_federated_narratives([good_node, stale_node]) == NarrativeFederationOutputStatus.federated_narrative_stale
    assert aggregate_federated_narratives([good_node, caveat_node]) == NarrativeFederationOutputStatus.federated_narrative_caveated

def test_preserve_caveats():
    node = FederatedNarrativeNodeRecord(
        node_id="n1", narrative_compiler_ref="c1", narrative_family="f1",
        currentness_state=NarrativeFederationCurrentnessRecord(
            is_current=True, last_refresh=datetime.datetime.now(datetime.UTC), expires_at=datetime.datetime.now(datetime.UTC)
        ),
        caveat_state=[
            NarrativeFederationCaveatRecord(caveat_id="c1", description="Caveat A"),
            NarrativeFederationCaveatRecord(caveat_id="c2", description="Caveat B", requires_no_safe_visibility=True)
        ],
        sovereignty_state="ok", node_status="active"
    )

    caveats = preserve_caveats_in_federation([node])
    assert "Caveat A" in caveats
    assert "Caveat B" in caveats

    no_safe = preserve_no_safe_sections_in_federation([node])
    assert len(no_safe) == 1
    assert "Caveat B" in no_safe[0]
