import typer
from rich.console import Console

# Import the new assurance_exchange CLI app
from sports_signal_bot.assurance_exchange.cli import app as assurance_exchange_app
from sports_signal_bot.cli_evidence_atlas import app as evidence_atlas_app
from sports_signal_bot.cli_hardening import app as hardening_app

from sports_signal_bot.cli_trace_routing import app as trace_routing_app

app = typer.Typer(help="Sports Signal Bot CLI")
console = Console()

app.add_typer(assurance_exchange_app, name="assurance-exchange", help="Assurance Exchange operations")
app.add_typer(evidence_atlas_app, name="evidence-atlas", help="Evidence Atlas operations")
app.add_typer(hardening_app, name="hardening", help="Hardening operations")

app.add_typer(trace_routing_app, name="trace-routing", help="Trace Routing operations")

@app.command("smoke-run")
def smoke_run():
    console.print("Smoke run ok.")

from sports_signal_bot.cli_proof_catalogs import app as proof_catalogs_app
app.add_typer(proof_catalogs_app, name="proof-catalogs", help="Phase 93: Proof Catalogs")

from sports_signal_bot.cli_context_assembly import app as context_assembly_app
app.add_typer(context_assembly_app, name="context-assembly", help="Phase 95: Context Assembly")

from sports_signal_bot.cli_coherence_scoring import app as coherence_scoring_app
app.add_typer(coherence_scoring_app, name="coherence-scoring", help="Phase 96: Coherence Scoring")

from sports_signal_bot.cli_alignment_compilers import app as alignment_compilers_app
app.add_typer(alignment_compilers_app, name="alignment-compilers", help="Phase 97: Alignment Compilers")




from sports_signal_bot.consistency_ledgers import cli as cli_consistency_ledgers
app.add_typer(cli_consistency_ledgers.app, name="consistency-ledgers")


from src.sports_signal_bot.cli_assurance_synthesizers import app as assurance_synthesizers_app
app.add_typer(assurance_synthesizers_app, name="assurance-synthesizers", help="Sovereign Governance Assurance Synthesizers (Phase 99)")


from sports_signal_bot.cli_end_state_review import app as end_state_review_app
from sports_signal_bot.cli_performance_hardening import app as performance_hardening_app
app.add_typer(performance_hardening_app, name="performance-hardening", help="Post-100 Hardening Pack 02 Commands")
app.add_typer(end_state_review_app, name="end-state-review", help="Phase 100: End State Review")

from sports_signal_bot.chaos_hardening.cli import app as chaos_hardening_app
app.add_typer(chaos_hardening_app, name="chaos-hardening", help="Post-100 Hardening Pack 04: Chaos Hardening")

from sports_signal_bot.cli_concurrency_hardening import app as concurrency_hardening_app
app.add_typer(concurrency_hardening_app, name="concurrency", help="Concurrency Hardening Pack 03")

from sports_signal_bot.cli_endurance_hardening import app as endurance_hardening_app
app.add_typer(endurance_hardening_app, name="endurance-hardening", help="Post-100 Hardening Pack 05: Endurance Hardening")

from sports_signal_bot.cli_operational_hardening import app as operational_hardening_app
app.add_typer(operational_hardening_app, name="operational-hardening", help="Post-100 Hardening Pack 06")


from sports_signal_bot.cli_migration_hardening import app as migration_hardening_app
app.add_typer(migration_hardening_app, name="migration-hardening", help="Post-100 Hardening Pack 07: Migration Hardening")

if __name__ == "__main__":
    app()


from sports_signal_bot.cli_hardening import app as hardening_app
app.add_typer(hardening_app, name="hardening", help="Post-100 Hardening Pack 01 Commands")
