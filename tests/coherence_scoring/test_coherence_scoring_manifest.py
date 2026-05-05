import pytest
from sports_signal_bot.coherence_scoring.contracts import (
    ContextAssemblerFederationRecord,
    FreshnessDisputeChamberRecord,
    TraceEvidenceBrokerRecord,
    SovereignGovernanceCoherenceScorerRecord,
    CoherenceInputRecord,
    FederatedContextNodeRecord,
    ContextFederationBundleRecord,
    FreshnessDisputeCaseRecord,
    EvidenceBrokerListingRecord,
    EvidenceBrokerRequestRecord,
    EvidenceBrokerMatchRecord
)
from sports_signal_bot.coherence_scoring.context_federations import (
    build_context_assembler_federation,
    add_context_federation_link,
    compute_federated_context_currentness,
    FEDERATED_CONTEXT_STALE
)
from sports_signal_bot.coherence_scoring.freshness_chambers import (
    build_freshness_dispute_chamber,
    open_freshness_dispute_case,
    resolve_freshness_dispute_case,
    DOWNGRADE_TO_REVIEW_ONLY_SUPPORT,
    REQUIRE_REFRESH_EVIDENCE
)
from sports_signal_bot.coherence_scoring.evidence_brokers import (
    build_trace_evidence_broker,
    create_evidence_broker_listing,
    create_evidence_broker_request,
    select_broker_match,
    MATCHED_CAVEATED_EVIDENCE_ROUTE
)
from sports_signal_bot.coherence_scoring.coherence_scorers import (
    build_governance_coherence_scorer,
    compute_coherence_band,
    BOUNDED_COHERENCE_WITH_CAVEATS
)

def test_context_federation_staleness():
    fed = build_context_assembler_federation("test_family", {})
    node = FederatedContextNodeRecord(
        node_id="n1",
        context_assembler_ref="ref1",
        assembler_family="test",
        currentness_state="stale",
        caveat_state="clear",
        sovereignty_state="passed",
        node_status="active"
    )
    add_context_federation_link(fed, node)
    assert compute_federated_context_currentness(fed, [node]) == FEDERATED_CONTEXT_STALE

def test_freshness_dispute_downgrade():
    chamber = build_freshness_dispute_chamber("test", {})
    case = open_freshness_dispute_case(chamber, "test")
    # No refresh evidence provided
    decision = resolve_freshness_dispute_case(case, REQUIRE_REFRESH_EVIDENCE)
    assert decision == DOWNGRADE_TO_REVIEW_ONLY_SUPPORT

def test_broker_match_caveated():
    broker = build_trace_evidence_broker("test", {})
    listing = create_evidence_broker_listing(broker, "test")
    listing.evidence_completeness = "partial"
    request = create_evidence_broker_request(broker)
    match = select_broker_match(listing, request)
    assert match.outcome == MATCHED_CAVEATED_EVIDENCE_ROUTE

def test_coherence_band_caveats():
    scorer = build_governance_coherence_scorer("test")
    inp = CoherenceInputRecord(
        coherence_input_id="inp-1",
        input_family="test",
        source_ref="test",
        currentness_state="fresh",
        caveat_state="caveated",
        sovereignty_state="passed",
        no_safe_visibility_state="preserved"
    )
    out = compute_coherence_band(scorer, [inp])
    assert out.band == BOUNDED_COHERENCE_WITH_CAVEATS
