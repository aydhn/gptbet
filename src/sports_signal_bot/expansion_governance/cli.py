import typer
import json
from typing import Dict, Any
from .strategies.balanced_control_tower import BalancedControlTowerStrategy
from .evidence import build_governance_evidence_bundle
from .manifests import write_governance_manifest
from .reporting import extract_kpi_hooks

app = typer.Typer(help="Phase 51 Expansion Governance & Rollout Control")

def get_mock_metrics() -> Dict[str, Any]:
    return {
        "active_cohorts": ["cohort_1", "cohort_2", "cohort_3"],
        "active_waves": ["wave_1"],
        "budget_usage": 0.65,
        "growing_cohorts": 2,
        "conflict_burden": 0.2,
        "warning_density": 0.1,
        "review_backlog": 0.3,
        "dispute_burden": 0.05,
        "rollback_penalty": 0.0,
        "cohort_details": [
            {"cohort_id": "cohort_1", "cohort_family": "reconciliation"},
            {"cohort_id": "cohort_2", "cohort_family": "provider_priority"}
        ],
        "critical_verification_failures": 0,
        "rollbacks_last_24h": 0,
        "global_budget_usage_pct": 0.65,
        "cross_family_dispute_rate": 0.05
    }

@app.command()
def run_expansion_governance():
    """Run a global expansion governance cycle using the Balanced Control Tower strategy."""
    typer.echo("Starting Global Expansion Governance Cycle...")

    metrics = get_mock_metrics()
    strategy = BalancedControlTowerStrategy()

    manifest = strategy.evaluate_state(metrics)

    typer.echo("\n--- Control Tower Summary ---")
    summary = manifest.control_tower_summary
    typer.echo(f"Global Status: {summary.global_status}")
    typer.echo(f"Active Waves/Cohorts: {summary.active_waves} / {summary.active_cohorts}")
    typer.echo(f"Global Pressure: {summary.global_pressure_band}")
    typer.echo(f"Emergency Breaker State: {summary.emergency_breaker_state}")
    typer.echo("\nRecommended Actions:")
    for a in summary.recommended_actions:
        typer.echo(f"- {a}")

    path = write_governance_manifest(manifest)
    typer.echo(f"\nManifest written to: {path}")

@app.command()
def preview_control_tower():
    """Preview the Control Tower summary without saving artifacts."""
    metrics = get_mock_metrics()
    strategy = BalancedControlTowerStrategy()
    manifest = strategy.evaluate_state(metrics)

    typer.echo(json.dumps(manifest.control_tower_summary.model_dump(mode='json'), indent=2))

@app.command()
def preview_expansion_budgets():
    """Preview global expansion risk budget utilization."""
    metrics = get_mock_metrics()
    # Mocking high budget usage to show output
    metrics["budget_usage"] = 0.96
    metrics["global_budget_usage_pct"] = 0.96

    strategy = BalancedControlTowerStrategy()
    manifest = strategy.evaluate_state(metrics)

    typer.echo("Budget Utilization Warning:")
    typer.echo(json.dumps(manifest.control_tower_summary.budget_usage_summary, indent=2))

@app.command()
def preview_circuit_breakers():
    """Preview circuit breaker evaluations for a critical state."""
    metrics = get_mock_metrics()
    metrics["critical_verification_failures"] = 4

    strategy = BalancedControlTowerStrategy()
    manifest = strategy.evaluate_state(metrics)

    typer.echo("Circuit Breaker State:")
    typer.echo(manifest.control_tower_summary.emergency_breaker_state)
    typer.echo("Council Decision:")
    typer.echo(manifest.council_decision.decision.value)

@app.command()
def preview_family_freezes():
    """Preview family freeze actions."""
    from .strategies.family_first import FamilyFirstProtectionStrategy

    metrics = get_mock_metrics()
    metrics["cohort_details"] = [
        {"cohort_id": "c1", "cohort_family": "alias_memory"},
        {"cohort_id": "c2", "cohort_family": "alias_memory"}
    ]

    strategy = FamilyFirstProtectionStrategy()
    manifest = strategy.evaluate_state(metrics)

    typer.echo("Family Freezes:")
    typer.echo(json.dumps(manifest.control_tower_summary.family_freezes, indent=2))

@app.command()
def list_expansion_governance_strategies():
    """List available governance strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeExpansionGovernanceStrategy")
    typer.echo("- BalancedControlTowerStrategy (Default)")
    typer.echo("- FamilyFirstProtectionStrategy")
    typer.echo("- RecoverySensitiveStrategy")
    typer.echo("- ThroughputCappedStrategy")

if __name__ == "__main__":
    app()
