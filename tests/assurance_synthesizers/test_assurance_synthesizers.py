from src.sports_signal_bot.assurance_synthesizers.contracts import (
    FederatedConsistencyNodeRecord,
    ClearingExchangePacketRecord,
    CaseStatus,
    ExchangeStatus,
    AssuranceBand
)
from src.sports_signal_bot.assurance_synthesizers.consistency_federations import (
    build_consistency_ledger_federation,
    add_consistency_federation_link,
    compute_federated_consistency_currentness
)
from src.sports_signal_bot.assurance_synthesizers.route_councils import (
    build_tribunal_route_council,
    open_tribunal_route_case,
    resolve_tribunal_route_case
)
from src.sports_signal_bot.assurance_synthesizers.clearing_exchanges import (
    build_evidence_clearing_exchange,
    validate_clearing_exchange_packet
)
from src.sports_signal_bot.assurance_synthesizers.assurance_synthesizers import (
    build_governance_assurance_synthesizer,
    register_assurance_synthesis_input,
    compute_assurance_synthesis_band
)

def test_consistency_federation_caps_currentness_if_stale():
    fed = build_consistency_ledger_federation("governance", "ref", "ref", "ref")
    node_a = FederatedConsistencyNodeRecord(
        node_id="a", consistency_ledger_ref="l_a", ledger_family="f1",
        currentness_state="stale", contradiction_state="none", sovereignty_state="ok", node_status="active"
    )
    node_b = FederatedConsistencyNodeRecord(
        node_id="b", consistency_ledger_ref="l_b", ledger_family="f1",
        currentness_state="current", contradiction_state="none", sovereignty_state="ok", node_status="active"
    )
    add_consistency_federation_link(fed, node_a, node_b)
    currentness = compute_federated_consistency_currentness(fed, [node_a, node_b])
    assert currentness == "stale_currentness_capped"

def test_route_council_blocks_if_sovereignty_conflict():
    council = build_tribunal_route_council("bounded", "ref", "ref")
    case = open_tribunal_route_case("stale", ["trace_1"])
    decision = resolve_tribunal_route_case(case, has_sufficient_evidence=True, has_sovereignty_conflict=True)
    assert case.case_status == CaseStatus.case_blocked

def test_route_council_downgrades_if_insufficient_evidence():
    council = build_tribunal_route_council("bounded", "ref", "ref")
    case = open_tribunal_route_case("stale", ["trace_1"])
    decision = resolve_tribunal_route_case(case, has_sufficient_evidence=False, has_sovereignty_conflict=False)
    assert case.case_status == CaseStatus.case_review_only

def test_clearing_exchange_blocks_if_no_sovereignty():
    exchange = build_evidence_clearing_exchange("global", "1h")
    packet = ClearingExchangePacketRecord(
        clearing_exchange_packet_id="pkt_1", evidence_completeness="complete", scope_constraints="strict"
    )
    status = validate_clearing_exchange_packet(packet, sovereignty_allowed=False)
    assert status == ExchangeStatus.exchanged_blocked

def test_clearing_exchange_caveats_if_partial_evidence():
    exchange = build_evidence_clearing_exchange("global", "1h")
    packet = ClearingExchangePacketRecord(
        clearing_exchange_packet_id="pkt_1", evidence_completeness="partial", scope_constraints="strict"
    )
    status = validate_clearing_exchange_packet(packet, sovereignty_allowed=True)
    assert status == ExchangeStatus.exchanged_caveated

def test_assurance_synthesis_band_logic():
    synth = build_governance_assurance_synthesizer("context")
    inp = register_assurance_synthesis_input(synth, "context", "current", "ok", "visible")
    out = compute_assurance_synthesis_band(synth, [inp])
    assert out.band == AssuranceBand.strong_bounded_assurance

    # Stale caps to bounded with caveats
    synth2 = build_governance_assurance_synthesizer("context")
    inp2 = register_assurance_synthesis_input(synth2, "context", "stale", "ok", "visible")
    out2 = compute_assurance_synthesis_band(synth2, [inp2])
    assert out2.band == AssuranceBand.bounded_assurance_with_caveats

    # no_safe visibility failure caps to review_only
    synth3 = build_governance_assurance_synthesizer("context")
    inp3 = register_assurance_synthesis_input(synth3, "context", "current", "ok", "no_safe")
    out3 = compute_assurance_synthesis_band(synth3, [inp3])
    assert out3.band == AssuranceBand.review_only_assurance

    # sovereignty deny failure caps to critically fragile
    synth4 = build_governance_assurance_synthesizer("context")
    inp4 = register_assurance_synthesis_input(synth4, "context", "current", "deny", "visible")
    out4 = compute_assurance_synthesis_band(synth4, [inp4])
    assert out4.band == AssuranceBand.critically_fragile_assurance

def test_strategies():
    from src.sports_signal_bot.assurance_synthesizers.strategies.conservative import ConservativeAssuranceSynthesizerStrategy
    from src.sports_signal_bot.assurance_synthesizers.contracts import AssuranceSynthesisInputRecord, AssuranceBand

    strat = ConservativeAssuranceSynthesizerStrategy()
    inp_stale = AssuranceSynthesisInputRecord(
        assurance_input_id="1", input_family="context", source_ref="ref",
        currentness_state="stale", caveat_state="caveated", sovereignty_state="ok", no_safe_visibility_state="visible"
    )
    band = strat.evaluate([inp_stale])
    assert band == AssuranceBand.fragile_assurance
