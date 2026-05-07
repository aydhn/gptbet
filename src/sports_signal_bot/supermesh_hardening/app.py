import typer
import json
from .integration import SupermeshHardeningIntegrator
from .strategies.conservative import ConservativeSupermeshHardeningStrategy
from .strategies.balanced_supermesh_readiness import BalancedSupermeshReadinessStrategy
from .strategies.pulse_truth_first import PulseTruthFirstStrategy
from .strategies.observatory_integrity_first import ObservatoryIntegrityFirstStrategy

app = typer.Typer()

STRATEGIES = {
    "conservative": ConservativeSupermeshHardeningStrategy(),
    "balanced": BalancedSupermeshReadinessStrategy(),
    "pulse_truth_first": PulseTruthFirstStrategy(),
    "observatory_integrity_first": ObservatoryIntegrityFirstStrategy()
}

@app.command("run-hardening-pack-16")
def run_hardening_pack_16(strategy: str = "conservative"):
    typer.echo(f"Running Supermesh Hardening Pack 16 with strategy: {strategy}")
    strat = STRATEGIES.get(strategy, ConservativeSupermeshHardeningStrategy())
    integrator = SupermeshHardeningIntegrator(strat)
    integrator.run_pass()
    summary = integrator.summarize()
    integrator.export_artifacts("artifacts/supermesh_hardening")
    typer.echo(json.dumps(summary, indent=2))
    typer.echo("Artifacts exported to artifacts/supermesh_hardening/")

@app.command("preview-federation-bus-supermesh-report")
def preview_federation_bus_supermesh_report():
    integrator = SupermeshHardeningIntegrator(ConservativeSupermeshHardeningStrategy())
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary.get("supermesh_summary", {}), indent=2))

@app.command("preview-scheduler-cadence-fabric-report")
def preview_scheduler_cadence_fabric_report():
    integrator = SupermeshHardeningIntegrator(ConservativeSupermeshHardeningStrategy())
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary.get("fabric_summary", {}), indent=2))

@app.command("preview-global-audit-pulse-report")
def preview_global_audit_pulse_report():
    integrator = SupermeshHardeningIntegrator(ConservativeSupermeshHardeningStrategy())
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary.get("pulse_summary", {}), indent=2))

@app.command("preview-planetary-handoff-observatory-report")
def preview_planetary_handoff_observatory_report():
    integrator = SupermeshHardeningIntegrator(ConservativeSupermeshHardeningStrategy())
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps(summary.get("observatory_summary", {}), indent=2))

@app.command("preview-supermesh-hardening-health")
def preview_supermesh_hardening_health():
    integrator = SupermeshHardeningIntegrator(ConservativeSupermeshHardeningStrategy())
    integrator.run_pass()
    summary = integrator.summarize()
    typer.echo(json.dumps({"overall_readiness": summary.get("overall_readiness", "unknown")}, indent=2))

@app.command("list-supermesh-hardening-strategies")
def list_supermesh_hardening_strategies():
    for name in STRATEGIES.keys():
        typer.echo(f"- {name}")
