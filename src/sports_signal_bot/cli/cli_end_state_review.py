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

    console.print("Assurance Federation Health: " + summarize_assurance_federation_health(fed))
    console.print("Closure Mesh Health: " + summarize_closure_mesh_health(mesh))
    console.print("Assurance Exchange Summary: " + summarize_assurance_exchange(exchange))
    console.print("End State Review Compiler Summary: " + summarize_end_state_review_compiler(compiler))
    console.print("End State Output Explanation: " + explain_end_state_review_output(band_output))

    console.print("[green]Pass complete.[/green]")

@app.command("preview-assurance-federations")
def preview_assurance_federations():
    """Preview assurance federations."""
    console.print("[blue]Previewing Assurance Federations...[/blue]")

@app.command("preview-closure-meshes")
def preview_closure_meshes():
    """Preview closure meshes."""
    console.print("[blue]Previewing Closure Meshes...[/blue]")

@app.command("preview-assurance-exchanges")
def preview_assurance_exchanges():
    """Preview assurance exchanges."""
    console.print("[blue]Previewing Assurance Exchanges...[/blue]")

@app.command("preview-end-state-reviews")
def preview_end_state_reviews():
    """Preview end state reviews."""
    console.print("[blue]Previewing End-State Reviews...[/blue]")

@app.command("preview-end-state-review-health")
def preview_end_state_review_health():
    """Preview end state review health."""
    console.print("[blue]Previewing End-State Review Health...[/blue]")

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
