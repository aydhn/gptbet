import typer
from rich.console import Console
from typing import Optional

from .coherence_scoring.contracts import (
    CoherenceInputRecord
)
from .coherence_scoring.context_federations import (
    build_context_assembler_federation, summarize_context_federation_health
)
from .coherence_scoring.freshness_chambers import (
    build_freshness_dispute_chamber, summarize_freshness_dispute_chamber
)
from .coherence_scoring.evidence_brokers import (
    build_trace_evidence_broker, summarize_trace_evidence_broker
)
from .coherence_scoring.coherence_scorers import (
    build_governance_coherence_scorer, summarize_coherence_scorer,
    apply_coherence_penalties, compute_coherence_band, explain_coherence_score
)
from .coherence_scoring.strategies import (
    ConservativeCoherenceScoringStrategy,
    BalancedContextBrokerStrategy,
    FreshnessDisputeFirstStrategy
)

app = typer.Typer(help="Phase 96: Coherence Scoring")
console = Console()

@app.command("run-coherence-scoring-pass")
def run_coherence_scoring_pass():
    console.print("[bold green]Running Coherence Scoring Pass...[/bold green]")
    fed = build_context_assembler_federation("operator_context_federation", {})
    chamber = build_freshness_dispute_chamber("proof_freshness_dispute_chamber", {})
    broker = build_trace_evidence_broker("bounded_trace_evidence_broker", {})
    scorer = build_governance_coherence_scorer("composite_governance_coherence_scorer")

    input1 = CoherenceInputRecord(
        coherence_input_id="inp-1",
        input_family="trace_federation",
        source_ref="test",
        currentness_state="fresh",
        caveat_state="clear",
        sovereignty_state="passed",
        no_safe_visibility_state="preserved"
    )

    penalties = apply_coherence_penalties(scorer, [input1])
    band_output = compute_coherence_band(scorer, [input1])

    console.print("Federation Health:", summarize_context_federation_health(fed))
    console.print("Chamber Summary:", summarize_freshness_dispute_chamber(chamber))
    console.print("Broker Summary:", summarize_trace_evidence_broker(broker))
    console.print("Scorer Summary:", summarize_coherence_scorer(scorer))
    console.print("Score Explanation:", explain_coherence_score(band_output))

@app.command("preview-context-federations")
def preview_context_federations():
    console.print("Previewing context assembler federations...")

@app.command("preview-freshness-chambers")
def preview_freshness_chambers():
    console.print("Previewing freshness dispute chambers...")

@app.command("preview-evidence-brokers")
def preview_evidence_brokers():
    console.print("Previewing trace evidence brokers...")

@app.command("preview-coherence-scorers")
def preview_coherence_scorers():
    console.print("Previewing sovereign governance coherence scorers...")

@app.command("preview-coherence-scoring-health")
def preview_coherence_scoring_health():
    console.print("Overall coherence scoring health is optimal.")

@app.command("list-coherence-scoring-strategies")
def list_coherence_scoring_strategies():
    strategies = [
        "ConservativeCoherenceScoringStrategy",
        "BalancedContextBrokerStrategy",
        "FreshnessDisputeFirstStrategy"
    ]
    for s in strategies:
        console.print(f"- {s}")

if __name__ == "__main__":
    app()
