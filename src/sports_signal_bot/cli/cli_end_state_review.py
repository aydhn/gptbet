import json
import typer
from rich.console import Console

from src.sports_signal_bot.end_state_review.contracts import EndStateReviewInputRecord, EndStateReviewPenaltyRecord
from src.sports_signal_bot.end_state_review.assurance_federations import build_assurance_synthesizer_federation, summarize_assurance_federation_health
from src.sports_signal_bot.end_state_review.closure_meshes import build_council_closure_mesh, summarize_closure_mesh_health
from src.sports_signal_bot.end_state_review.assurance_exchanges import build_evidence_assurance_exchange, summarize_assurance_exchange
from src.sports_signal_bot.end_state_review.review_compilers import (
    build_governance_end_state_review_compiler,
    register_end_state_review_input,
    apply_end_state_review_penalties,
    compute_end_state_review_band,
    summarize_end_state_review_compiler,
    explain_end_state_review_output
)

app = typer.Typer(help="Sovereign Governance End-State Review Compiler CLI")
console = Console()

@app.command("run-end-state-review-pass")
def run_end_state_review_pass():
    """Run the end state review pass."""
    console.print("[green]Running End-State Review Pass...[/green]")

    fed = build_assurance_synthesizer_federation("operator_assurance_federation", "default")
    mesh = build_council_closure_mesh("council_closure_mesh", "default")
    exchange = build_evidence_assurance_exchange("bounded_evidence_assurance_exchange")
    compiler = build_governance_end_state_review_compiler("composite_governance_end_state_review_compiler", "default")

    input1 = EndStateReviewInputRecord(
        review_input_id="inp-1",
        input_family="trace_federation",
        source_ref="test",
        currentness_state="fresh",
        caveat_state="clear",
        sovereignty_state="passed",
        no_safe_visibility_state="preserved"
    )

    register_end_state_review_input(compiler, input1)
    apply_end_state_review_penalties(compiler, [])
    band_output = compute_end_state_review_band(compiler)

    assurance_fed_health = summarize_assurance_federation_health(fed)
    closure_mesh_health = summarize_closure_mesh_health(mesh)
    assurance_exchange_summary = summarize_assurance_exchange(exchange)
    compiler_summary = summarize_end_state_review_compiler(compiler)
    explanation = explain_end_state_review_output(band_output)

    with open("assurance_federations.json", "w") as f:
        json.dump({"status": "ok", "health": assurance_fed_health}, f, indent=2)
    with open("closure_meshes.json", "w") as f:
        json.dump({"status": "ok", "health": closure_mesh_health}, f, indent=2)
    with open("assurance_exchanges.json", "w") as f:
        json.dump({"status": "ok", "summary": assurance_exchange_summary}, f, indent=2)
    with open("end_state_reviews.json", "w") as f:
        json.dump({"status": "ok", "compiler_summary": compiler_summary, "explanation": explanation}, f, indent=2)
    with open("end_state_review_health.json", "w") as f:
        json.dump({"status": "healthy"}, f, indent=2)

    console.print(f"Assurance Federation Health: {assurance_fed_health}")
    console.print(f"Closure Mesh Health: {closure_mesh_health}")
    console.print(f"Assurance Exchange Summary: {assurance_exchange_summary}")
    console.print(f"End State Review Compiler Summary: {compiler_summary}")
    console.print(f"End State Output Explanation: {explanation}")

    console.print("[green]Pass complete.[/green]")

@app.command("preview-assurance-federations")
def preview_assurance_federations():
    """Preview assurance federations."""
    try:
        with open("assurance_federations.json") as f:
            data = json.load(f)
            console.print(json.dumps(data, indent=2))
    except FileNotFoundError:
        console.print("[red]No report found. Run run-end-state-review-pass first.[/red]")

@app.command("preview-closure-meshes")
def preview_closure_meshes():
    """Preview closure meshes."""
    try:
        with open("closure_meshes.json") as f:
            data = json.load(f)
            console.print(json.dumps(data, indent=2))
    except FileNotFoundError:
        console.print("[red]No report found. Run run-end-state-review-pass first.[/red]")

@app.command("preview-assurance-exchanges")
def preview_assurance_exchanges():
    """Preview assurance exchanges."""
    try:
        with open("assurance_exchanges.json") as f:
            data = json.load(f)
            console.print(json.dumps(data, indent=2))
    except FileNotFoundError:
        console.print("[red]No report found. Run run-end-state-review-pass first.[/red]")

@app.command("preview-end-state-reviews")
def preview_end_state_reviews():
    """Preview end state reviews."""
    try:
        with open("end_state_reviews.json") as f:
            data = json.load(f)
            console.print(json.dumps(data, indent=2))
    except FileNotFoundError:
        console.print("[red]No report found. Run run-end-state-review-pass first.[/red]")

@app.command("preview-end-state-review-health")
def preview_end_state_review_health():
    """Preview end state review health."""
    try:
        with open("end_state_review_health.json") as f:
            data = json.load(f)
            console.print(json.dumps(data, indent=2))
    except FileNotFoundError:
        console.print("[red]No report found. Run run-end-state-review-pass first.[/red]")

@app.command("list-end-state-review-strategies")
def list_end_state_review_strategies():
    """List available strategies."""
    console.print("[blue]Available Strategies:[/blue]")
    console.print("- ConservativeEndStateReviewStrategy")
    console.print("- BalancedClosureExchangeFederationStrategy")
    console.print("- ClosureIntegrityFirstStrategy")
    console.print("- AssuranceExchangeStrictStrategy")
    console.print("- SovereigntyDominantEndStateStrategy")

if __name__ == "__main__":
    app()
