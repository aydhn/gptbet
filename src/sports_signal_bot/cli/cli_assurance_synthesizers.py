import typer
from rich.console import Console
from typing import Optional

from src.sports_signal_bot.assurance_synthesizers.contracts import (
    ConsistencyLedgerFederationRecord,
    FederatedConsistencyNodeRecord,
    TribunalRouteCouncilRecord,
    TribunalRouteCaseRecord,
    EvidenceClearingExchangeRecord,
    ClearingExchangePacketRecord,
    SovereignGovernanceAssuranceSynthesizerRecord
)
from src.sports_signal_bot.assurance_synthesizers.consistency_federations import (
    build_consistency_ledger_federation,
    add_consistency_federation_link,
    compute_federated_consistency_currentness,
    summarize_consistency_federation_health
)
from src.sports_signal_bot.assurance_synthesizers.route_councils import (
    build_tribunal_route_council,
    open_tribunal_route_case,
    resolve_tribunal_route_case,
    summarize_tribunal_route_council
)
from src.sports_signal_bot.assurance_synthesizers.clearing_exchanges import (
    build_evidence_clearing_exchange,
    validate_clearing_exchange_packet,
    summarize_clearing_exchange
)
from src.sports_signal_bot.assurance_synthesizers.assurance_synthesizers import (
    build_governance_assurance_synthesizer,
    register_assurance_synthesis_input,
    compute_assurance_synthesis_band,
    summarize_assurance_synthesizer
)

app = typer.Typer(help="Sovereign Governance Assurance Synthesizers operations (Phase 99)")
console = Console()

@app.command("run-assurance-synthesizers-pass")
def run_assurance_synthesizers_pass():
    """Runs a full assurance synthesis pass over federations, councils, and exchanges."""
    console.print("[bold green]Starting Assurance Synthesis Pass...[/bold green]")

    # 1. Consistency Federation
    fed = build_consistency_ledger_federation("governance_consistency_federation", "ref", "ref", "ref")
    node_a = FederatedConsistencyNodeRecord(
        node_id="node_a", consistency_ledger_ref="l_a", ledger_family="f1",
        currentness_state="current", contradiction_state="none", sovereignty_state="ok", node_status="active"
    )
    node_b = FederatedConsistencyNodeRecord(
        node_id="node_b", consistency_ledger_ref="l_b", ledger_family="f1",
        currentness_state="stale", contradiction_state="none", sovereignty_state="ok", node_status="active"
    )
    add_consistency_federation_link(fed, node_a, node_b)
    currentness = compute_federated_consistency_currentness(fed, [node_a, node_b])

    # 2. Tribunal Route Council
    council = build_tribunal_route_council("bounded_route_council", "ref", "ref")
    case = open_tribunal_route_case("stale_route_case", ["trace_1"])
    decision = resolve_tribunal_route_case(case, has_sufficient_evidence=False, has_sovereignty_conflict=False)

    # 3. Clearing Exchange
    exchange = build_evidence_clearing_exchange("global", "1h")
    packet = ClearingExchangePacketRecord(
        clearing_exchange_packet_id="pkt_1", evidence_completeness="partial", scope_constraints="strict"
    )
    validate_clearing_exchange_packet(packet, sovereignty_allowed=True)

    # 4. Assurance Synthesis
    synth = build_governance_assurance_synthesizer("context_assurance_synthesizer")
    inp = register_assurance_synthesis_input(synth, "context", currentness, "ok", "visible")
    out = compute_assurance_synthesis_band(synth, [inp])

    console.print(f"[bold]Federation:[/bold] {summarize_consistency_federation_health(fed)}")
    console.print(f"[bold]Council:[/bold] {summarize_tribunal_route_council(council)}")
    console.print(f"[bold]Exchange:[/bold] {summarize_clearing_exchange(exchange)}")
    console.print(f"[bold]Synthesis:[/bold] {summarize_assurance_synthesizer(synth, out)}")

    console.print("\n[bold green]Assurance Synthesis Pass Completed[/bold green]")

@app.command("preview-consistency-federations")
def preview_consistency_federations():
    """Preview current consistency federations."""
    console.print("Previewing consistency federations...")
    # Mock data output
    console.print("- Federation ID: fed_mock, Family: governance, Health: active, Members: 3, Stale: 1")

@app.command("preview-route-councils")
def preview_route_councils():
    """Preview tribunal route councils and active cases."""
    console.print("Previewing tribunal route councils...")
    console.print("- Council ID: council_mock, Family: bounded_route, Active Cases: 2")

@app.command("preview-clearing-exchanges")
def preview_clearing_exchanges():
    """Preview evidence clearing exchanges."""
    console.print("Previewing clearing exchanges...")
    console.print("- Exchange ID: exch_mock, Scope: global, Status: exchanged_caveated")

@app.command("preview-assurance-synthesizers")
def preview_assurance_synthesizers():
    """Preview assurance synthesizers and bands."""
    console.print("Previewing assurance synthesizers...")
    console.print("- Synthesizer ID: synth_mock, Family: context_assurance, Band: bounded_assurance_with_caveats")

@app.command("preview-assurance-synthesizers-health")
def preview_assurance_synthesizers_health():
    """Preview health of the assurance synthesizers layer."""
    console.print("Previewing assurance synthesizers health...")
    console.print("- Overall Health: Healthy, Stale suppressions: 4, Active warnings: 2")

@app.command("list-assurance-synthesizer-strategies")
def list_assurance_synthesizer_strategies():
    """List available assurance synthesizer strategies."""
    console.print("Available Assurance Synthesizer Strategies:")
    console.print("1. ConservativeAssuranceSynthesizerStrategy")
    console.print("2. BalancedCouncilClearingSynthesisStrategy")
    console.print("3. RouteIntegrityFirstStrategy")
    console.print("4. ClearingExchangeStrictStrategy")
    console.print("5. SovereigntyDominantAssuranceStrategy")

if __name__ == "__main__":
    app()
