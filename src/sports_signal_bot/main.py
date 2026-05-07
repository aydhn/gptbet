import typer
from rich.console import Console

# Import the new assurance_exchange CLI app
from src.sports_signal_bot.assurance_exchange.cli import app as assurance_exchange_app
from src.sports_signal_bot.cli_evidence_atlas import app as evidence_atlas_app
from src.sports_signal_bot.cli_hardening import app as hardening_app

from src.sports_signal_bot.cli_trace_routing import app as trace_routing_app

app = typer.Typer(help="Sports Signal Bot CLI")
console = Console()

app.add_typer(assurance_exchange_app, name="assurance-exchange", help="Assurance Exchange operations")
app.add_typer(evidence_atlas_app, name="evidence-atlas", help="Evidence Atlas operations")
app.add_typer(hardening_app, name="hardening", help="Hardening operations")

app.add_typer(trace_routing_app, name="trace-routing", help="Trace Routing operations")

@app.command("smoke-run")
def smoke_run():
    console.print("Smoke run ok.")

from src.sports_signal_bot.cli_proof_catalogs import app as proof_catalogs_app
app.add_typer(proof_catalogs_app, name="proof-catalogs", help="Phase 93: Proof Catalogs")

from src.sports_signal_bot.cli_context_assembly import app as context_assembly_app
app.add_typer(context_assembly_app, name="context-assembly", help="Phase 95: Context Assembly")

from src.sports_signal_bot.cli_coherence_scoring import app as coherence_scoring_app
app.add_typer(coherence_scoring_app, name="coherence-scoring", help="Phase 96: Coherence Scoring")

from src.sports_signal_bot.cli_alignment_compilers import app as alignment_compilers_app
app.add_typer(alignment_compilers_app, name="alignment-compilers", help="Phase 97: Alignment Compilers")




from src.sports_signal_bot.consistency_ledgers import cli as cli_consistency_ledgers
app.add_typer(cli_consistency_ledgers.app, name="consistency-ledgers")
from src.sports_signal_bot.deployment import cli as cli_deployment
app.add_typer(cli_deployment.app, name="deploy")


from src.sports_signal_bot.cli_assurance_synthesizers import app as assurance_synthesizers_app
app.add_typer(assurance_synthesizers_app, name="assurance-synthesizers", help="Sovereign Governance Assurance Synthesizers (Phase 99)")


from src.sports_signal_bot.cli_end_state_review import app as end_state_review_app
from src.sports_signal_bot.cli_performance_hardening import app as performance_hardening_app
app.add_typer(performance_hardening_app, name="performance-hardening", help="Post-100 Hardening Pack 02 Commands")
app.add_typer(end_state_review_app, name="end-state-review", help="Phase 100: End State Review")

from src.sports_signal_bot.chaos_hardening.cli import app as chaos_hardening_app
app.add_typer(chaos_hardening_app, name="chaos-hardening", help="Post-100 Hardening Pack 04: Chaos Hardening")

from src.sports_signal_bot.cli_concurrency_hardening import app as concurrency_hardening_app
app.add_typer(concurrency_hardening_app, name="concurrency", help="Concurrency Hardening Pack 03")

from src.sports_signal_bot.cli_endurance_hardening import app as endurance_hardening_app
app.add_typer(endurance_hardening_app, name="endurance-hardening", help="Post-100 Hardening Pack 05: Endurance Hardening")

from src.sports_signal_bot.cli_operational_hardening import app as operational_hardening_app
app.add_typer(operational_hardening_app, name="operational-hardening", help="Post-100 Hardening Pack 06")


from src.sports_signal_bot.cli_migration_hardening import app as migration_hardening_app
app.add_typer(migration_hardening_app, name="migration-hardening", help="Post-100 Hardening Pack 07: Migration Hardening")

from src.sports_signal_bot.cli_hardening import app as hardening_app
app.add_typer(hardening_app, name="hardening", help="Post-100 Hardening Pack 01 Commands")
from src.sports_signal_bot.regional_hardening_cli import app as regional_hardening_app
app.add_typer(regional_hardening_app, name="regional-hardening", help="Post-100 Hardening Pack 08: Regional Hardening")
from src.sports_signal_bot.cli_geo_hardening import app as geo_hardening_app
app.add_typer(geo_hardening_app, name="geo-hardening", help="Phase 109: Geo Hardening")


from src.sports_signal_bot.cli_geo_quorum_hardening import app as geo_quorum_hardening_app

app.add_typer(geo_quorum_hardening_app, name="geo-quorum-hardening", help="Post-100 Hardening Pack 10: Geo Quorum Hardening")

from src.sports_signal_bot.cli_global_hardening import app as global_hardening_app
app.add_typer(global_hardening_app, name="global-hardening", help="Post-100 Hardening Pack 11: Global Hardening")

# ==============================================================================
# Planetary Hardening Post-100 Pack 12
# ==============================================================================
import json
from src.sports_signal_bot.planetary_hardening.integration import PlanetaryHardeningIntegrator
from src.sports_signal_bot.planetary_hardening.strategies.conservative import ConservativePlanetaryHardeningStrategy
from src.sports_signal_bot.planetary_hardening.strategies.balanced_planetary_readiness import BalancedPlanetaryReadinessStrategy
from src.sports_signal_bot.planetary_hardening.strategies.lane_integrity_first import LaneIntegrityFirstStrategy
from src.sports_signal_bot.planetary_hardening.strategies.audit_pack_first import AuditPackFirstStrategy

planetary_app = typer.Typer(name="planetary-hardening", help="Post-100 Planetary Hardening Pack 12")
app.add_typer(planetary_app, name="planetary-hardening")
app.add_typer(planetary_app, name="planetary-hardening")

@planetary_app.command("run-hardening-pack-12")
def run_hardening_pack_12(strategy: str = "conservative"):
    typer.echo(f"Running Planetary Hardening Pack 12 with strategy: {strategy}")
    integrator = PlanetaryHardeningIntegrator(strategy_name=strategy)
    integrator.run_pass()
    summary = integrator.summarize()
    integrator.export_artifacts("artifacts/planetary_hardening")
    typer.echo(json.dumps(summary, indent=2))
    typer.echo("Artifacts exported to artifacts/planetary_hardening/")

@planetary_app.command("preview-planetary-coverage-calendar-report")
def preview_planetary_coverage_calendar_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["calendars"], indent=2))

@planetary_app.command("preview-intercontinental-recovery-report")
def preview_intercontinental_recovery_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["lanes"], indent=2))

@planetary_app.command("preview-global-quorum-federation-report")
def preview_global_quorum_federation_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["federations"], indent=2))

@planetary_app.command("preview-follow-the-sun-audit-report")
def preview_follow_the_sun_audit_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["audits"], indent=2))

@planetary_app.command("preview-planetary-hardening-health")
def preview_planetary_hardening_health():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["health"], indent=2))

@planetary_app.command("list-planetary-hardening-strategies")
def list_planetary_hardening_strategies():
    strats = [
        ConservativePlanetaryHardeningStrategy().name,
        BalancedPlanetaryReadinessStrategy().name,
        LaneIntegrityFirstStrategy().name,
        AuditPackFirstStrategy().name
    ]
    for s in strats:
        typer.echo(f"- {s}")
# ==============================================================================
# Planetary Hardening Post-100 Pack 12
# ==============================================================================
from src.sports_signal_bot.planetary_hardening.integration import PlanetaryHardeningIntegrator
from src.sports_signal_bot.planetary_hardening.strategies.conservative import ConservativePlanetaryHardeningStrategy
from src.sports_signal_bot.planetary_hardening.strategies.balanced_planetary_readiness import BalancedPlanetaryReadinessStrategy
from src.sports_signal_bot.planetary_hardening.strategies.lane_integrity_first import LaneIntegrityFirstStrategy
from src.sports_signal_bot.planetary_hardening.strategies.audit_pack_first import AuditPackFirstStrategy

planetary_app = typer.Typer(name="planetary-hardening", help="Post-100 Planetary Hardening Pack 12")
app.add_typer(planetary_app, name="planetary-hardening")

@planetary_app.command("run-hardening-pack-12")
def run_hardening_pack_12(strategy: str = "conservative"):
    typer.echo(f"Running Planetary Hardening Pack 12 with strategy: {strategy}")
    integrator = PlanetaryHardeningIntegrator(strategy_name=strategy)
    integrator.run_pass()
    summary = integrator.summarize()
    integrator.export_artifacts("artifacts/planetary_hardening")
    typer.echo(json.dumps(summary, indent=2))
    typer.echo("Artifacts exported to artifacts/planetary_hardening/")

@planetary_app.command("preview-planetary-coverage-calendar-report")
def preview_planetary_coverage_calendar_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["calendars"], indent=2))

@planetary_app.command("preview-intercontinental-recovery-report")
def preview_intercontinental_recovery_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["lanes"], indent=2))

@planetary_app.command("preview-global-quorum-federation-report")
def preview_global_quorum_federation_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["federations"], indent=2))

@planetary_app.command("preview-follow-the-sun-audit-report")
def preview_follow_the_sun_audit_report():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["audits"], indent=2))

@planetary_app.command("preview-planetary-hardening-health")
def preview_planetary_hardening_health():
    integrator = PlanetaryHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary["health"], indent=2))

@planetary_app.command("list-planetary-hardening-strategies")
def list_planetary_hardening_strategies():
    strats = [
        ConservativePlanetaryHardeningStrategy().name,
        BalancedPlanetaryReadinessStrategy().name,
        LaneIntegrityFirstStrategy().name,
        AuditPackFirstStrategy().name
    ]
    for s in strats:
        typer.echo(f"- {s}")

# Add it before __main__ block
if __name__ == "__main__":
    app()
    app()
